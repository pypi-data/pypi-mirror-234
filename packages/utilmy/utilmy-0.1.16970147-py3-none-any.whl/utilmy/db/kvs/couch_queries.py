import zlib
import ujson as json
import msgpack
from collections import defaultdict
from simplek8s.config_reader import ConfigReader
from simplek8s.logger import Logger
from local.utils import rbset, rbset_to_bytes, rbset_from_bytes
from db.couch_conn import CouchConn as CC

class CouchQueries(object):
    def __init__(self,config_file_path=None):
        self.config = ConfigReader(config_file_path).config
        self.logger = Logger().logger
        self.couch_conn = CC(config_file_path)
        self.batch_size = 50
        self.ipl_version = self.config.get('environment','ipl_version')
        self.vran_pur_weight = float(self.config.get('siid_stats','vran_pur_weight'))
        self.vran_brw_weight = float(self.config.get('siid_stats','vran_brw_weight'))
        self.max_pur = float(self.config.get('siid_stats','max_pur'))
        self.max_pv = float(self.config.get('siid_stats','max_pv'))
        self.max_siid_adjust = float(self.config.get('siid_stats','max_siid_adjust'))
        self.default_item_cvr = float(self.config.get('siid_stats','default_item_cvr'))
        self.default_item_click = float(self.config.get('siid_stats','default_item_click'))
        self.pv_weight = float(self.config.get('siid_stats','pv_weight'))
        self.min_item_cvr = float(self.config.get('siid_stats','min_item_cvr')) 

    @property
    def zzz_version_id(self):
        """
        used to get part of the prefix for the cad keys of RPP
        """
        if not hasattr(self,'_zzz_version_id'):
            self.logger.info('getting api version id')
            control_conn = self.couch_conn.zzz_control_conn
            self._zzz_version_id = control_conn.get('zzz_cfg_pending').value
            self.logger.info('zzz_version_id = ' + self._zzz_version_id)
        return self._zzz_version_id

    def get_siid_to_title(self,siids):
        """
        try getting item titles from RPP couchbase
        many items might be missing so use cassandra for others
        """
        siid_to_title = dict()
        cad_map = self.get_siid_to_ad_data(siids,no_title=False)
        for siid, vals in cad_map.items():
            if len(vals) > 1:
                siid_to_title[siid] = vals[-1]
        return siid_to_title

    def get_siid_to_ad_data(self,siids,no_title=True):
        siids = list(siids)
        batch_size = self.batch_size
        prefix = 'cad_' + self.zzz_version_id + '_'
        siid_to_data = dict()
        self.gpath_index = 2
        self.cpc_index = -1
        for indx in range(0,len(siids),batch_size):
            c_keys = [prefix + str(siid) for siid in siids[indx:indx+batch_size]]
            c_data = self.couch_conn.zzz_control_conn.get_multi(c_keys,no_format=True)
            for c_key, c_val in c_data.items():
                try:
                    siid = c_key[len(prefix):]
                    if c_val.value == None:
                        siid_to_data[siid] = []
                        continue
                    vals = json.loads(zlib.decompress(c_val.value))
                    # fields that we need
                    # [shop,item,[genre_path],
                    postage = vals['postage_flg']
                    item_price = vals['item_price']
                    genre_path = [int(g) for g in vals['genre_id_list'].split('/') if len(g) == 6]
                    campaign_id = vals['campaign_id']
                    shop,item = [int(_) for _ in siid.split('_')]
                    asuraku = vals['asuraku_flg']
                    asuraku_closing = vals['asuraku_closing_time']
                    title = vals['item_name']
                    cpc = vals['click_price']
                    tags = vals['tags1']
                    ng_words = []
                    # note:  adding 1 below to signify rpp campaign type
                    if no_title:
                        siid_to_data[siid] = [shop,item,genre_path,item_price,postage,asuraku,asuraku_closing,campaign_id,1,tags,ng_words,cpc]
                    else:
                        siid_to_data[siid] = [shop,item,genre_path,item_price,postage,asuraku,asuraku_closing,campaign_id,1,tags,ng_words,cpc,title]
                except Exception as e:
                    self.logger.warn('error decompressing cad data: ' + c_key +  ' ' + str(e))
        return siid_to_data

    def get_ipl_data(self,siids):
        """
        @siids: any length set or list of siids
        returns:  {siid: [ran, series, sg, genre]}, missing_siids: set of siids without info
        """
        prefix = f'sivsg_{self.ipl_version}_'
        lprefix = len(prefix)
        batch_list = []
        ipl_map = dict()
        missing_siids = set()
        pcnt = 0
        for siid in siids:
            couch_key = f'{prefix}{siid}'
            batch_list.append(couch_key)
            pcnt += 1
            if len(batch_list) >= self.batch_size or pcnt >= len(siids):
                pdata = self.couch_conn.m2_search_conn.get_multi(batch_list,no_format=True)
                batch_list = []
                for ckey, pres in pdata.items():
                    siid = ckey[lprefix:]
                    if pres.value is None:
                        missing_siids.add(siid)
                    else:
                        ran,series, sg, genre = msgpack.loads(pres.value)
                        ipl_map[siid] = [ran,series,sg,genre]
        return ipl_map, missing_siids

    def set_ipl_data(self, siid_to_vsg_map, ipl_version=None):
        if ipl_version is None:
            ipl_version = self.ipl_version
        cnt = 0
        batch_map = dict()
        for siid, vsg in siid_to_vsg_map.items():
            ckey = f'sivsg_{ipl_version}_{siid}'
            value = msgpack.dumps(vsg)
            batch_map[ckey] = value
            cnt += 1
            if len(batch_map) >= self.batch_size or cnt >= len(siid_to_vsg_map):
                self.couch_conn.m2_search_conn.upsert_multi(batch_map,ttl=20*86400)
                batch_map.clear()
        return


    def get_siid_stats(self,siids):
        """
        [vran,pur,gms,min_price,max_price,pv,vpur,vmin_price,vmax_price,vavg_price,vpv]
        max_siid_ajust =1.
        max_pur = 100.
        vran_pur_weight = 0.1
        max_pv = 500.
        vran_brw_weight = 0.1
        pv_weight = 0.5
        stat_adjust = min(1., (pur+vran_pur_weight*vpur)/max_pur) + (brw+vran_brw_weight*vpv)/max_pv))
        """
        s_list = []
        s_map  = dict()
        prefix = 'siid_stats_'
        s_count = 0
        max_adjust = 0.
        bad_item_count = 0
        for siid in siids:
            s_list.append(siid)
            s_count += 1
            if len(s_list) > self.batch_size or s_count >= len(siids):
                s_keys = [f'{prefix}{s}' for s in s_list]
                s_data = self.couch_conn.m2_search_conn.get_multi(s_keys)
                for s_key, s_val in s_data.items():
                    siid_str = s_key[len(prefix):]
                    if s_val.value is None:
                        s_map[siid_str] = 0.
                        continue
                    else:
                        stat_vals = json.loads(zlib.decompress(s_val.value))
                        pur_score = ( stat_vals[1] + self.vran_pur_weight * stat_vals[6]) / self.max_pur
                        brw_score = self.pv_weight * ( stat_vals[5] + self.vran_brw_weight * stat_vals[10]) / self.max_pv
                        stat_score = min(self.max_siid_adjust, pur_score + brw_score)
                        pv = stat_vals[5]
                        pur = stat_vals[1]
                        cvr = (self.default_item_cvr*self.default_item_click + pur)/(self.default_item_click+pv)
                        if cvr < self.min_item_cvr:
                            stat_score = -10.  # debug later 2018-04-17
                            bad_item_count += 1
                        cvr = min(1.,cvr)
                        #stat_score += self.max_siid_adjust*(cvr - self.default_item_cvr)/(cvr+self.default_item_cvr)
                        s_map[siid_str] = stat_score
                        if stat_score > max_adjust:
                            max_adjust = stat_score
                s_list = []
        return s_map

    def set_siid_to_qhashes(self, siid_to_queries):
        """
        @siid_to_queries:  dict( siid, qhashes)  for each siid provide all possible SQIP query hashes
                           that can be generated from the title
        """
        batch_map = dict()
        i_count = 0
        prefix = f's2q_{self.ipl_version}_'
        for siid, queries in siid_to_queries.items():
            i_count +=1
            ckey = prefix + siid
            batch_map[ckey] = zlib.compress(json.dumps(queries).encode('utf8'))
            if len(batch_map) >= self.batch_size or i_count >= len(siid_to_queries):
                self.couch_conn.zzz_search_conn.upsert_multi(batch_map,ttl=20*86400)
                batch_map.clear()
        self.logger.info(f'inserted raw queries for {len(siid_to_queries)} siids')
        return

    def get_siid_to_qhashes_new(self, siids):
        """
        using qhashes produced by v15+
        @siids:  list of f'{shop_id}_{item_id}'
        returns siid_to_queries:   dict( siid, qhashes ) for each siid provide all possible SQIP query hashes
                           that can be generated from the title
        """
        siid_to_queries = self.get_siid_to_qhashes(siids) #defaultdict(list)
        siid_list = list()
        prefix = f's2q_{self.ipl_version}_'
        s_count = 0
        self.logger.debug(f'checking {len(siids)} siids for existing queries')
        for siid in siids:
            s_count += 1
            if not siid in siid_to_queries:
                siid_list.append(siid)
            if len(siid_list) > self.batch_size or s_count >= len(siids):
                s_keys = [f'{prefix}{s}' for s in siid_list]
                if len(s_keys) < 1:
                  continue
                s_data =  self.couch_conn.zzz_search_conn.get_multi(s_keys,no_format=True)
                for s_key, s_val in s_data.items():
                    if s_val.value is None:
                        continue
                    siid_str = s_key[len(prefix):]
                    siid_to_queries[siid_str] = set(json.loads(zlib.decompress(s_val.value)))
                siid_list = []
        self.logger.debug(f'{len(siid_to_queries)} siids already had queries stored')
        return siid_to_queries

    def get_siid_to_qhashes(self, siids):
        """
        @siids:  list of f'{shop_id}_{item_id}'
        returns siid_to_queries:   dict( siid, qhashes ) for each siid provide all possible SQIP query hashes
                           that can be generated from the title
        """
        siid_to_queries = defaultdict(list)
        siid_list = list()
        prefix = f'zzz_s2q_v12_' # debug{self.ipl_version}_'
        s_count = 0
        self.logger.debug(f'checking {len(siids)} siids for existing queries')
        for siid in siids:
            s_count += 1
            siid_list.append(siid)
            if len(siid_list) > self.batch_size or s_count >= len(siids):
                s_keys = [f'{prefix}{s}' for s in siid_list]
                s_data =  self.couch_conn.zzz_search_conn.get_multi(s_keys,no_format=True)
                for s_key, s_val in s_data.items():
                    if s_val.value is None:
                        continue
                    siid_str = s_key[len(prefix):]
                    siid_to_queries[siid_str] = set(json.loads(zlib.decompress(s_val.value)))
                siid_list = []
        self.logger.debug(f'{len(siid_to_queries)} siids already had queries stored')
        return siid_to_queries

    def set_vran_to_querydist(self, vran_to_querydist):
        """
        sqip data aggregated to vran, query
        vran_to_querydist[vran] = [(query_score, query_hash)]
        """
        ttl = 20*86400
        prefix = f'sqr_v2q_{self.ipl_version}_'
        batch_map= dict()
        cnt = 0
        for vran, query_list in vran_to_querydist.items():
            ckey = f'{prefix}{vran}'
            cnt += 1
            batch_map[ckey] = zlib.compress(json.dumps(query_list).encode('utf8'))
            if len(batch_map) >= self.batch_size or cnt >= len(vran_to_querydist):
                self.couch_conn.zzz_search_conn.upsert_multi(batch_map,ttl=ttl)
                batch_map.clear()
        return

    def get_vran_to_querydist(self, vrans):
        """
        for each vran in @vrans, return list (query_score, query)
        returns vran_to_querydist[vran] : [(qscore1,query1),(qscore2,query2)]
        """
        prefix = f'sqr_v2q_{self.ipl_version}_'
        lprefix = len(prefix)
        batch_list = []
        vran_to_querydist = dict()
        cnt = 0
        for vran in vrans:
            batch_list.append(f'{prefix}{vran}')
            cnt += 1
            if len(batch_list) >= self.batch_size or cnt >= len(vrans):
                cdata = self.couch_conn.zzz_search_conn.get_multi(batch_list,no_format=True)
                for ckey, v in cdata.items():
                    key = int(ckey[lprefix:])
                    vran_to_querydist[key] = []
                    if v.value != None:
                        vran_to_querydist[key] = json.loads(zlib.decompress(v.value))
                batch_list = []
        return vran_to_querydist

    def set_qhash_to_vrandist(self, qhash_to_vranscore):
        """
        sqip data aggregated to query-vran level
        qhash_to_genres[query_hash] : [(qscore1,vran1),(qscore2,vran2),...]
        """
        ttl = 20*86400
        prefix = f'sqr_q2v_{self.ipl_version}_'
        batch_map = dict()
        cnt = 0
        for qhash, vranlist in qhash_to_vranscore.items():
            ckey = f'{prefix}{qhash}'
            cnt += 1
            vranlist.sort(reverse=True)
            batch_map[ckey] = zlib.compress(json.dumps(vranlist).encode('utf8'))
            if len(batch_map) >= self.batch_size or cnt >= len(qhash_to_vranscore):
                self.couch_conn.zzz_search_conn.upsert_multi(batch_map,ttl=ttl)
                batch_map.clear()
        return

    def get_qhash_to_vrandist(self, qhashes):
        """
        returns qhash_to_vranlist[qhash] -->  [(qscore1,vran1),(qscore2,vran2),...]
        """
        prefix = f'sqr_q2v_{self.ipl_version}_'
        lprefix = len(prefix)
        batch_list = []
        qhash_to_vrandist = dict()
        cnt = 0
        for qhash in qhashes:
            batch_list.append(f'{prefix}{qhash}')
            cnt += 1
            if len(batch_list) >= self.batch_size or cnt >= len(qhashes):
                cdata = self.couch_conn.zzz_search_conn.get_multi(batch_list,no_format=True)
                for ckey, v in cdata.items():
                    key = ckey[lprefix:]
                    qhash_to_vrandist[key] = []
                    if v.value != None:
                        qhash_to_vrandist[key] = json.loads(zlib.decompress(v.value))
                batch_list = []
        return qhash_to_vrandist


    def set_qhash_to_genredist(self, qhash_to_genrescore):
        """
        sqip data aggregated to query-genre level
        qhash_to_genres[(query_hash,query_total_score)] : { genre_to_score[genre_id] : score}
        """
        ttl = 20*86400
        prefix = f'qstat_{self.ipl_version}_'
        batch_map = dict()
        cnt = 0
        for (qhash,query_score), genre_score_map in qhash_to_genrescore.items():
            ckey = f'{prefix}{qhash}'
            qlist = [(genre_id,genre_score) for genre_id, genre_score in genre_score_map.items()]
            batch_map[ckey] = zlib.compress(json.dumps([query_score,qlist]).encode('utf8'))
            if len(batch_map) >= self.batch_size or cnt >= len(qhash_to_genrescore):
                self.couch_conn.zzz_search_conn.upsert_multi(batch_map,ttl=ttl)
                batch_map.clear()
        return

    def get_qhash_to_genredist(self, qhashes):
        """
        @qhashes:  list of  sqip_item.get_token_hash(query)
        returns qhash_to_genredist[qhash] -->  [query_total_score, [(genre1,score1),(genre2,score2),....]]
        """
        prefix = f'qstat_{self.ipl_version}_'
        cnt = 0
        lprefix = len(prefix)
        batch_list = []
        qhash_to_genredist = dict()
        for qhash in qhashes:
            cnt += 1
            batch_list.append(f'{prefix}{qhash}')
            if len(batch_list) >= self.batch_size or cnt >= len(qhashes):
                cdata = self.couch_conn.cpc_search_conn.get_multi(batch_list,no_format=True)
                for ckey, v in cdata.items():
                    key = int(ckey[lprefix:])
                    qhash_to_genredist[key] = []
                    if v.value != None:
                        qhash_to_genredist[key] = json.loads(zlib.decompress(v.value))
                batch_list = []
        return qhash_to_genredist

    def set_qhash_to_queries(self, qmap):
        """
        qmap[query_hash] --> set(keywords)  utf8 encoded
        inserts the map into couchbase, adds to existing data
        """
        ttl = 20*86400
        prefix = f'qh2q_{self.ipl_version}'
        batch_map = dict()
        batch_keys = []
        cnt = 0
        for qh, queries in qmap.items():
            ckey = f'{prefix}_{qh}'
            batch_keys.append(ckey)
            cnt += 1
            batch_map[ckey] = zlib.compress(json.dumps(list(queries)).encode('utf8'))
            if len(batch_keys) >= self.batch_size or cnt >= len(qmap):
                old_data = self.couch_conn.cpc_search_conn.get_multi(batch_keys,no_format=True)
                for k, v in old_data.items():
                    if v.value is None:
                        continue
                    try:
                        old_list = json.loads(zlib.decompress(v.value))
                        new_list = json.loads(zlib.decompress(batch_map[k]))
                        new_list = list(set(old_list+new_list))
                        batch_map[k] = zlib.compress(json.dumps(new_list).encode('utf8'))
                    except Exception as e:
                        self.logger.warning(f'error loading qh to queries: ckey={k} error={e}')
                retry = 0
                while retry < 3:
                    try:
                        self.couch_conn.cpc_search_conn.upsert_multi(batch_map,ttl=ttl)
                        break
                    except Exception as couch_error:
                        self.logger.warning(f'error with set_qhash_to_queries: retry={retry} {couch_error}')
                        time.sleep(5 + retry*5)
                        continue
                batch_keys = []
                batch_map.clear()
        return

    def get_qhash_to_queries(self, qhashes):
        """
        @qhashes:  iterable of int(qhash)  64bit mmh3 hashes of query tokens
        return qmap[int(qhash)] : [queries]   utf8 enocded queries 
        """
        qmap = dict()
        cnt = 0
        prefix = f'qh2q_{self.ipl_version}'
        batch_list = []       
        for qh in qhashes:
            cnt += 1
            batch_list.append(f'{prefix}_{qh}')
            if len(batch_list) >= self.batch_size or cnt >= len(qhashes):
                cdata = self.couch_conn.cpc_search_conn.get_multi(batch_list,no_format=True)
                for k,v in cdata.items():
                    try:
                        qh = int(k.split('_')[-1])
                        if v.value is None:
                            # debug:  let's not put anything and let the client deal with no data for the query qmap[qh] = None
                            continue
                        qmap[qh] = set(json.loads(zlib.decompress(v.value)))
                    except Exception as e:
                        self.logger.warning(f'error getting queries for qh:{k}  {e}')
                batch_list = []
        return qmap 

    def set_qh32_to_qhashes(self, qh32toqhashes):
        """
        intermediate data for indexing sqip queries
        used to resolve collisions from 64bit hash to 32bit
        @qh32toqhashes[qh32] : {qhash64,}
        """
        ttl = 20*86400
        prefix = f'qh32toqh_{self.ipl_version}'
        batch_map = dict()
        batch_keys = []
        cnt = 0
        for qh32, qhashes in qh32toqhashes.items():
            ckey = f'{prefix}_{qh32}'
            batch_keys.append(ckey)
            cnt += 1
            batch_map[ckey] = zlib.compress(json.dumps(list(qhashes)).encode('utf8'))
            if len(batch_keys) >= self.batch_size or cnt >= len(qh32toqhashes):
                old_data = self.couch_conn.cpc_search_conn.get_multi(batch_keys,no_format=True)
                for k, v in old_data.items():
                    if v.value is None:
                        continue
                    try:
                        old_list = json.loads(zlib.decompress(v.value))
                        new_list = json.loads(zlib.decompress(batch_map[k]))
                        new_list = list(set(old_list+new_list))
                        batch_map[k] = zlib.compress(json.dumps(new_list).encode('utf8'))
                    except Exception as e:
                        self.logger.warning(f'error loading qh32 to qhashes: ckey={k} error={e}')
                retry = 0
                while retry < 3:
                    retry += 1
                    try:
                        self.couch_conn.cpc_search_conn.upsert_multi(batch_map,ttl=ttl)
                        break
                    except Exception as couch_error:
                        self.logger.warning(f'error with set_qh32_to_qhashes: retry={retry} {couch_error}')
                        time.sleep(5 + retry*5)
                        continue
                batch_keys = []
                batch_map.clear()
        return

    def get_qh32_to_qhashes(self, qh32s):
        """
        find all the 64bit hashes associated with the 32bit hash
        @qh32s:   iteratable of 32bit ints
        """
        qmap = dict()
        cnt = 0
        prefix = f'qh32toqh_{self.ipl_version}'
        batch_list = []
        for qh32 in qh32s:
            cnt += 1
            batch_list.append(f'{prefix}_{qh32}')
            if len(batch_list) >= self.batch_size or cnt >= len(qh32s):
                cdata = self.couch_conn.cpc_search_conn.get_multi(batch_list,no_format=True)
                for k,v in cdata.items():
                    try:
                        qh32 = k.split('_')[-1]
                        if v.value is None:
                            qmap[qh32] = set()
                            continue
                        qlist = json.loads(zlib.decompress(v.value))
                        #qlist = json.loads(v.value)
                        qmap[qh32] = set(qlist)
                    except Exception as e:
                        self.logger.warning(f'error getting queries for qh32:{k}  {e}')
                batch_list = []
        return qmap

    def set_htkn_to_qh32s(self, htoq32s):
        """
        for every uhash64(token) store the corresponding uhash32(sqip_query) of all sqip queries
        that contain the token or its translation
        @htoq32s[uhash64(token)]: roaringbitmap{uhash32(query),...}
        """
        ttl = 20*86400
        prefix = f'ht2q32_{self.ipl_version}'
        batch_map = dict()
        cnt = 0
        for htkn, qh32s in htoq32s.items():
            ckey = f'{prefix}_{htkn}'
            cnt += 1
            if len(qh32s) > 1000000:
                self.logger.warning(f'htkn has too many associated queries: {htkn} {len(qh32s)} queries')
                continue
            batch_map[ckey] = rbset_to_bytes(qh32s) 
            if len(batch_map) >= self.batch_size or cnt >= len(htoq32s):
                retry = 0
                while retry < 3:
                    retry += 1
                    try:
                        self.couch_conn.cpc_search_conn.upsert_multi(batch_map,ttl=ttl)
                        batch_map.clear()
                        break
                    except Exception as couch_error:
                        self.logger.warning(f'error set_htkn_to_qh32: retry {retry}  {couch_error}')
                        time.sleep(5 + retry * 5)
        return

    def get_htkn_to_qh32s(self, htkns):
        """
        for every uhash64(token) store the corresponding uhash32(sqip_query) of all sqip queries
        that contain the token or its translation
        @htknns   iterable of uhash64(token)
        """
        cnt = 0
        batch_size = 8 # some tokens have too many queries
        batch_list = []
        prefix = f'ht2q32_{self.ipl_version}'
        qmap = dict()
        for htkn in htkns:
            cnt += 1
            batch_list.append(f'{prefix}_{htkn}')
            if len(batch_list) >= batch_size or cnt >= len(htkns):
                hdata = self.couch_conn.cpc_search_conn.get_multi(batch_list,no_format=True)
                batch_list = []
                for k,v in hdata.items():
                    try:
                        ht = int(k.split('_')[-1])
                        if v.value is None:
                            qmap[ht] = rbset()
                            continue
                        qmap[ht] = rbset_from_bytes(v.value)
                    except Exception as e:
                        self.logger.warning(f'error getting qh32s for htkn: {k}')
        return qmap


    def set_vrans_to_items(self, vran_to_items_map, ipl_version=None):
        if ipl_version is None:
            ipl_version = self.ipl_version
        batch_map = dict()
        cnt = 0
        ttl = 20*86400
        for vran, items in vran_to_items_map.items():
            ckey = f'v2s_{ipl_version}_{vran}'
            value = msgpack.dumps(list(items))
            cnt += 1
            batch_map[ckey] = value
            if len(batch_map) >= self.batch_size or cnt >=len(vran_to_items_map):
                self.couch_conn.m3_sqipl_conn.upsert_multi(batch_map,ttl=ttl)
                batch_map.clear()
        return

    def get_vrans_to_items(self, vrans, ipl_version=None):
        if ipl_version is None:
            ipl_version = self.ipl_version
        batch_list = []
        prefix = f'v2s_{ipl_version}_'
        lprefix = len(prefix)
        vran_to_items = dict()
        cnt = 0
        for vran in vrans:
            cnt += 1
            if int(vran) < 0:
                sv = str(vran)
                shop = sv[-6:]
                item = sv[1:-6]
                vran_to_items[sv] = [[int(shop),int(item)],]
            else:
                cass_key = f'{prefix}{vran}'
                batch_list.append(cass_key)
            if len(batch_list)>=self.batch_size or (len(batch_list) > 0 and cnt >= len(vrans)):
                vdata = self.couch_conn.m3_sqipl_conn.get_multi(batch_list,no_format=True)
                for k,v in vdata.items():
                    vrn = k.split('_')[-1]
                    if v.value is None:
                        vran_to_items[vrn] = []
                    else:
                        vran_to_items[vrn] = msgpack.loads(v.value)
                batch_list = []
        return vran_to_items

    def set_h32vrans(self, h32_vran_map, ipl_version=None):
        if ipl_version is None:
            ipl_version = self.ipl_version
        batch_map = dict()
        cnt = 0
        ttl = 20*86400
        for h32, vrans in h32_vran_map.items():
            ckey = f'h32v_{ipl_version}_{h32}'
            value = msgpack.dumps(list(vrans))
            cnt += 1
            batch_map[ckey] = value
            if len(batch_map) >= self.batch_size or cnt >=len(h32_vran_map):
                self.couch_conn.m3_sqipl_conn.upsert_multi(batch_map,ttl=ttl)
                batch_map.clear()
        return

    def get_h32vrans(self, h32s, ipl_version=None):
        if ipl_version is None:
            ipl_version = self.ipl_version
        batch_list = []
        prefix = f'h32v_{ipl_version}_'
        lprefix = len(prefix)
        h32_vrans = dict()
        cnt = 0
        for h32 in h32s:
            cass_key = f'{prefix}{h32}'
            batch_list.append(cass_key)
            cnt += 1
            if len(batch_list)>=self.batch_size or cnt >= len(h32s):
                vdata = self.couch_conn.m3_sqipl_conn.get_multi(batch_list,no_format=True)
                for k,v in vdata.items():
                    hash32 = k.split('_')[-1]
                    if v is None:
                        h32_vrans[hash32] = []
                    else:
                        h32_vrans[hash32] = msgpack.loads(v.value)
                batch_list = []
        return h32_vrans

    def set_h64_to_h32s(self, h64_to_h32s_map, ipl_version=None):
        """
        used by vran IPL similarity for CA and BTA
        @h64_to_h32s_map[hash64(token)] --> set(hash32(vran))
        what vrans contain word 'token'
        """
        if ipl_version is None:

            ipl_version = self.ipl_version
        batch_map = dict()
        cnt = 0
        ttl = 20*86400
        for h64, h32s in h64_to_h32s_map.items():
            ckey = f'hto32_{ipl_version}_{h64}'
            value = rbset_to_bytes(h32s)
            cnt += 1
            batch_map[ckey] = value
            if len(batch_map) >= self.batch_size or cnt >=len(h64_to_h32s_map):
                self.couch_conn.m3_sqipl_conn.upsert_multi(batch_map,ttl=ttl)
                batch_map.clear()
        return

    def get_h64_to_h32s(self, h64s, ipl_version=None):
        """
        used by vran IPL similarity for CA, CPA and BTA
        @h64s -->  set(uhash64(token))
        returns map   h64[uhash64(token)] =  rbset( uhash32(vran))
        """
        if ipl_version is None:
            ipl_version = self.ipl_version
        batch_list = []
        prefix = f'hto32_{ipl_version}_'
        lprefix = len(prefix)
        h64_h32s = dict()
        cnt = 0
        batch_size = 5
        for h64 in h64s:
            cass_key = f'{prefix}{h64}'
            batch_list.append(cass_key)
            cnt += 1
            if len(batch_list)>=batch_size or cnt >= len(h64s):
                vdata = self.couch_conn.m3_sqipl_conn.get_multi(batch_list,no_format=True)
                for k,v in vdata.items():
                    htkn = k.split('_')[-1]
                    if v is None:
                        h64_h32s[htkn] = []
                    else:
                        h64_h32s[htkn] = rbset_from_bytes(v.value)
                batch_list = []
        return h64_h32s


