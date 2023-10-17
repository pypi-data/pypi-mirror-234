# -*- coding: utf-8 -*-
""" Top-k retrieval vectors for Rec
Doc::



"""
import os, glob, sys, math, time, json, functools, random, yaml, gc, copy, pandas as pd, numpy as np
import datetime
from box import Box

import warnings ;warnings.filterwarnings("ignore")
from warnings import simplefilter  ; simplefilter(action='ignore', category=FutureWarning)
with warnings.catch_warnings():
    pass


from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob


#### Optional imports
try :
    import faiss
    import diskcache
except:
    print('pip install faiss-cpu')



from utilmy.deeplearning.util_embedding import (
    embedding_extract_fromtransformer,
    embedding_load_pickle,
    embedding_load_parquet,
    embedding_load_word2vec,
    embedding_torchtensor_to_parquet,
    embedding_rawtext_to_parquet,


    db_load_dict,
    np_norm_l2,
    np_matrix_to_str,
    np_str_to_array,
    np_array_to_str,
    np_matrix_to_str2,
    np_matrix_to_str3,
    np_matrix_to_str_sim

)


#############################################################################################
from utilmy import log, log2, os_module_name

def help():
    """function help        """
    from utilmy import help_create
    print( help_create(__file__) )



#############################################################################################
def test_all() -> None:
    """ python  $utilmy/deeplearning/util_topk.py test_all         """
    log(os_module_name(__file__))
    ztest2()

   


def ztest2():
  """  tests
  Docs ::
  
        Test Cases  pd_add_onehot_encoding
        Test Cases  embedding_cosinus_scores_pairwise
        Test Cases  KNNClassifierFAISS
        Test Cases  faiss_create_index
        Test Cases  topk_calc
        Test Cases  faiss_topk_calc

  """
  dd = ztest_create_fake_df(dirout="./")
  
  emb_list = []
  for i in range(4):
      emb_list.append( ','.join([str(x) for x in np.random.random(200)]))

  res = pd.DataFrame({'id': [1, 2, 3, 4] * 5,
                      'gender': [0, 1, 0, 1] * 5,
                      'masterCategory': [2, 1, 3, 4] * 5,
                      'emb': emb_list * 5})

  labels_dict = {'gender' : [0,1],
                  'masterCategory' : [3,1,2],
  }

  path = './temp/tem/'
  os.makedirs(path, exist_ok=True)
  trial = [res.to_csv(f'{path}{str(i)}.csv', index=False) for i in range(1, 4)]

  log('######### pd_to_onehot #####################')
  df = pd_to_onehot(res,  labels_dict=labels_dict )

  log('######### embedding cosinus #####################')
  embedding_cosinus_scores_pairwise(embs=np.random.random((5,5)), word_list=np.array([1,2,3,4,5]))


  log("#########  faiss_KNNClassifier ################################")
  model = faiss_KNNClassifier()
  model.fit(np.random.random((5,5)), np.array([0,1,2,3,4]))


  log("#########  faiss_create_index  ################################")
  faiss_create_index(df_or_path=f'{path}1.csv',
                     faiss_nlist=10, faiss_M=4, faiss_nbits=2, faiss_hnsw_m=32)

  log("#########  faiss_topk_calc  ##################################")
  faiss_topk_calc(df=f'{path}1.csv', root=path,
                      colid='id',   colemb='emb',  ### id --> emb
                      colkey='idx', colval='id',  ### dict map idx --> id
                      faiss_index="./temp/faiss/faiss_trained_20.index", dirout=path,
                      npool=1,
                      faiss_nlist=4, M=4, nbits=2, hnsw_m=32)

  log("#########  faiss_topk_calc parallel  ##################################")
  #### bug In github action, too long to run...
  #faiss_topk_calc(df=f'{path}*', root=path,
  #                colid='id',   colemb='emb',  ### id --> emb
  #                colkey='idx', colval='id',  ### dict map idx --> id
  #                faiss_index="./temp/faiss/faiss_trained_20.index", dirout='./temp/result/',
  #                npool=2, chunk=10)

  log("#########  topk_calc  #########################################")
  topk_calc(diremb=f'{path}1.csv', nrows=40)



########################################################################################################
######## Top-K retrieval ###############################################################################
class TOPK(object):
    """  Generic interface for topk



    """
    def init(self, modelname='faiss', **kw):
        self.name = modelname
        self.pars = kw

    def index_load(self, dirin, **kw):
        if self.name == 'faiss':
            faiss_load_index(self.dirin, **kw)

    def index_fit(sel):
        pass

    def index_save(sel):
        pass

    def topk(self):
        pass


    def topk_batch(self):
        pass



def topk_nearest_vector(x0:np.ndarray, vector_list:list, topk=3, engine='faiss', engine_pars:dict=None) :
   """
    Retrieve top k nearest vectors using FAISS, raw retrieval
    Doc::

        x0 (np.array)      : Input data shape (n_samples, n_features)
        vector_list (list) : Input data shape  (n_samples, n_features)
        topk (int)         : Number of nearest neighbors to fetch

        Returns
        dist (list): shape = [n_samples, k]
            The distances between the query and each sample in the region of
            competence. The vector is ordered in an ascending fashion.
        idice (list): shape = [n_samples, k]
            Indices of the instances belonging to the region of competence of
            the given query sample.
   """

   if 'faiss' in engine:
       # cc = engine_pars
       import faiss
       index = faiss.index_factory(x0.shape[1], 'Flat')
       index.add(vector_list)
       dist, indice = index.search(x0, topk)
       return dist, indice



def topk_calc(diremb="", dirout="", topk=100,  idlist=None, nrows=10, emb_dim=200, tag=None, debug=True):
    """
    Get Topk vector per each element vector of dirin.
    Doc::

        diremb (str)  : Input data path.
        dirout (str)  : Results path
        topk (int)    : Number of nearest neighbors to fetch. (Default = 100)
        nrows (int)   : Sample size of input data. (Default = 10)
        idlist (list) : Input data
        emb_dim (int) : Embedding dimension (Default = 200)

        Return  pd.DataFrame( columns=[  'id', 'emb', 'topk', 'dist'  ] )
         id :   id of the emb
         emb :  [342,325345,343]   X0 embdding
         topk:  2,5,6,5,6
         distL:  0,3423.32424.,

       python $utilmy/deeplearning/util_topk.py  topk_calc   --diremb     --dirout

    """
    from utilmy import pd_read_file

    ##### Load emb data  ###############################################
    flist    = glob_glob(diremb)
    df       = pd_read_file(  flist , n_pool=10 )
    df.index = np.arange(0, len(df))
    df = df.iloc[:nrows, :]
    log(df)
    assert len(df[['id', 'emb' ]]) > 0


    ##### Element X0 ####################################################
    vectors = np_str_to_array(df['emb'].values,  mdim= emb_dim)
    llids   = df['id'].values        if idlist is None  else idlist
    del df ; gc.collect()

    dfr = [] 
    for ii in range(0, len(llids)) :        
        x0      = vectors[ii]
        xname   = llids[ii]
        log(xname)
        x0         = x0.reshape(1, -1).astype('float32')  
        dist, rank = topk_nearest_vector(x0, vectors, topk= topk) 
        
        ss_rankid = np_array_to_str( llids[ rank[0] ] )
        ss_distid = np_array_to_str( dist[0]  )

        dfr.append([  xname, x0,  ss_rankid,  ss_distid  ])   

    dfr = pd.DataFrame( dfr, columns=[  'id', 'emb', 'topk', 'dist'  ] )
    pd_read_file( dfr, dirout + f"/topk_{tag}.parquet"  )




########################################################################################################
######## Top-K retrieval Faiss #########################################################################
# 2 checks to always ensure while creating index
# emb_dim % faiss_M == 0 and emb_dim / faiss_M >= 2^(faiss_nbits)

FAISS_CONFIG = Box({
   #### Faiss constraints: emb_dim % faiss_M == 0 and emb_dim / faiss_M >= 2^(faiss_nbits)

   'size_10m':  {'faiss_nlist': 6000, 'faiss_M': 40, 'faiss_nbits': 8, 'faiss_hnsw_m': 32
    },


   'size_100k': {'faiss_nlist': 1000, 'faiss_M': 40, 'faiss_nbits': 4, 'faiss_hnsw_m': 32
    },


   'size_10k': {'faiss_nlist': 100, 'faiss_M': 40, 'faiss_nbits': 4, 'faiss_hnsw_m': 32
    },


})


def faiss_create_index(df_or_path=None, col='emb', dirout=None,  db_type = "IVF4096,Flat", nfile=1000, emb_dim=200,
                       nrows=-1, faiss_nlist=6000, faiss_M=40, faiss_nbits=8, faiss_hnsw_m=32):
    """ Create Large scale Index
    Docs::

        Faiss constraints: emb_dim % faiss_M == 0 and emb_dim / faiss_M >= 2^(faiss_nbits)

        df_or_path (str)   : Path or dataframe df[['id', 'embd' ]]
        col (str)          : Column name for embedding. (Default = 'emb')
        dirout (str)       : Results path.
        nrows (int)        : Sample size of input data. (Default = 10)
        nfile (int)        : Number of files to process. (Default = 1000)
        emb_dim (int)      : Embedding dimension. (Default = 200)
        faiss_nlist        : Param of IVF, Number of cells (space partition). Typical value is sqrt(N). (Default = 6000)
        faiss_M (int)      : The number of sub-vector. Typically this is 8, 16, 32, etc. (Default = 40)
        faiss_nbits (int)  : Bits per sub-vector. This is typically 8, so that each sub-vec is encoded by 1 byte. (Default = 8)
        faiss_hnsw_m (int) : Param of HNSW Number of neighbors for HNSW. This is typically 32. (Default = 32)

        return strs (path to faiss index)
        python util_topk.py   faiss_create_index    --df_or_path myemb/

    """
    import faiss

    assert(emb_dim % faiss_M == 0 and emb_dim / faiss_M >= math.pow(2, faiss_nbits)), " Failed faiss conditions"
    
    dirout    =  "/".join( os.path.dirname(df_or_path).split("/")[:-1]) + "/faiss/" if dirout is None else dirout
    os.makedirs(dirout, exist_ok=True)
    log('dirout', dirout)
    log('dirin',  df_or_path)
    
    if isinstance(df_or_path, str) :      
       flist = sorted(glob.glob(df_or_path  ))[:nfile] 
       log('Loading', df_or_path) 
       df = pd_read_file(flist, n_pool=20, verbose=False)
    else :
       df = df_or_path

    df  = df.iloc[:nrows, :]   if nrows>0  else df
    log(df)
        
    tag = f"_" + str(len(df))    
    df  = df.sort_values('id')    
    df[ 'idx' ] = np.arange(0,len(df))
    pd_to_file( df[[ 'idx', 'id' ]], 
                dirout + f"/map_idx{tag}.parquet", show=1)   #### Keeping maping faiss idx, item_tag
    

    log("#### Convert parquet to numpy   ", dirout)
    X  = np.zeros((len(df), emb_dim  ), dtype=np.float32 )    
    vv = df[col].values
    del df; gc.collect()
    for i, r in enumerate(vv) :
        try :
          vi      = [ float(v) for v in r.split(',')]        
          X[i, :] = vi
        except Exception as e:
          log(i, e)
            
    log("#### Preprocess X")
    faiss.normalize_L2(X)  ### Inplace L2 normalization
    log( X ) 
    
    nt = min(len(X), int(max(400000, len(X) *0.075 )) )
    Xt = X[ np.random.randint(len(X), size=nt),:]
    log('Nsample training', nt)

    ####################################################    
    D = emb_dim  ###   actual  embedding size
    N = len(X)   ##### 1000000

    # Param of PQ for 1 billion
    M      = faiss_M # 16  ###  200 / 5 = 40  The number of sub-vector. Typically this is 8, 16, 32, etc.
    nbits  = faiss_nbits   ###  bits per sub-vector. This is typically 8, so that each sub-vec is encoded by 1 byte
    nlist  = faiss_nlist   ###  Param of IVF,  Number of cells (space partition). Typical value is sqrt(N)
    hnsw_m = faiss_hnsw_m  ###  Param of HNSW Number of neighbors for HNSW. This is typically 32

    # Setup  distance -> similarity in uncompressed space is  dis = 2 - 2 * sim, https://github.com/facebookresearch/faiss/issues/632
    quantizer = faiss.IndexHNSWFlat(D, hnsw_m)
    index     = faiss.IndexIVFPQ(quantizer, D, nlist, M, nbits)
    
    log('###### Train indexer')
    index.train(Xt)      # Train
    
    log('###### Add vectors')
    index.add(X)        # Add

    log('###### Test values ')
    index.nprobe = 8  # Runtime param. The number of cells that are visited for search.
    dists, ids = index.search(x=X[:3], k=4 )  ## top4
    log(dists, ids)
    
    log("##### Save Index    ")
    dirout2 = dirout + f"/faiss_trained{tag}.index" 
    log( dirout2 )
    faiss.write_index(index, dirout2 )
    return dirout2
        


def faiss_load_index(path_or_faiss_index=None, colkey='id', colval='idx'):
    """ load index + mapping
    Doc::

        path_or_faiss_index (str): Path
        colkey (str): map_idx.parquet id col. (Default = 'id')
        colval (str): map_idx.parquet idx col. (Default = 'idx')

        return faiss_index, mapping
        https://www.programcreek.com/python/example/112280/faiss.read_index
    """
    faiss_index = path_or_faiss_index
    faiss_index = ""  if faiss_index is None  else faiss_index
    if isinstance(faiss_index, str) :
        faiss_path  = faiss_index
        faiss_index = faiss.read_index(faiss_path)

    faiss_index.nprobe = 12  # Runtime param. The number of cells that are visited for search.
    log('Faiss Index: ', faiss_index)

    try :
       dirmap       = faiss_path.replace("faiss_trained", "map_idx").replace(".index", '.parquet')
       map_idx_dict = db_load_dict(dirmap,  colkey = colkey, colval = colval )
    except:
       map_idx_dict = {}

    return faiss_index, map_idx_dict



def faiss_topk_calc(df=None, root=None, colid='id', colemb='emb',
                    faiss_index: str = "", topk=200, dirout=None, npool=1, nrows=10 ** 7, nfile=1000,
                    colkey='idx', colval='id', chunk=200000,
                    return_simscore=False, return_dist=False,
                    **kw

                    ):
    """Calculate top-k for each 'emb' vector of dataframe in parallel batch.
    Doc::

         df (str)                  : Path to DF   df[['id', 'embd' ]]
         colid (str)               : Column name for id. (Default = 'id')
         colemb (str)              : Column name for embedding. (Default = 'emb')
         faiss_index (str)         : Path to index. (Default = "")
         topk (int)                : Number of nearest neighbors to fetch. (Default = 200)
         dirout (str)              : Results path.
         npool (int)               : num_cores for parallel processing. (Default = 1)
         nfile (int)               : Number of files to process. (Default = 1000)
         colkey (str)              : map_idx.parquet id col. (Default = 'id')
         colval (str)              : map_idx.parquet idx col. (Default = 'idx')
         return_simscore (boolean) : If True, score will returned. (Defaults to False.)
         return_dist(boolean)      : If True, distances will returned. (Defaults to False.)
         return results path, id, topk : word id, topk of id

         -- Parallel mode, ONLY in CLI (Jupyter cannot)
             python util_topk.py faiss_topk_calc2 --df './temp/tem/*' --faiss_index './temp/faiss/faiss_trained_40.index' --dirout './temp/result/' --npool 2 --chunks 20

         -- Faiss params
             https://github.com/facebookresearch/faiss/issues/632
             dis = 2 - 2 * sim

         -- Code
             faiss_topk_calc(df=f'{path}1.csv', root=path,
                              colid='id', colemb='emb',  ### id --> emb
                              colkey='idx', colval='id',  ### dict map idx --> id
                              faiss_index="./temp/faiss/faiss_trained_40.index", dirout=path,
                              npool=1,
                              faiss_nlist=4, M=4, nbits=2, hnsw_m=32)

    """

    faiss_index = "" if faiss_index is None else faiss_index
    if isinstance(faiss_index, str):
        faiss_path = faiss_index
        faiss_index, map_idx_dict = faiss_load_index(path_or_faiss_index=faiss_index)
    faiss_index.nprobe = 12  # Runtime param. The number of cells that are visited for search.
    log('Faiss Index: ', faiss_index)

    ########################################################################
    if isinstance(df, list):  ### Multi processing part
        if len(df) < 1: return 1
        flist = df[0]
        root = os.path.abspath(os.path.dirname(flist[0]))  ### bug in multipro
        dirin = root + "/df/"
        dir_out = dirout

    elif isinstance(df, str):  ### df == string path
        root = df
        dirin = root
        dir_out = dirout
        flist = sorted(glob.glob(dirin))
    else:
        raise Exception('Unknonw path')

    log('dir_in',  dirin)
    log('dir_out', dir_out)
    flist = flist[:nfile]
    if len(flist) < 1: return 1
    log('Nfile', len(flist), flist)

    ####### Parallel Mode ################################################
    if npool > 1 and len(flist) > npool:
        log('Parallel mode')
        from utilmy.parallel  import multiproc_run, multiproc_tochunk
        ll_list = multiproc_tochunk(flist, npool=npool)
        multiproc_run(faiss_topk_calc, ll_list, npool, verbose=True, start_delay=5,
                      input_fixed={'faiss_index': faiss_path, 'dirout': dirout}, )

        return 1

    ####### Single Mode #################################################
    dirmap = faiss_path.replace("faiss_trained", "map_idx").replace(".index", '.parquet')
    map_idx_dict = db_load_dict(dirmap, colkey=colkey, colval=colval)

    chunk = chunk
    kk = 0
    os.makedirs(dir_out, exist_ok=True)
    dirout2 = dir_out
    flist = [t for t in flist if len(t) > 8]
    log('\n\nN Files', len(flist), str(flist)[-100:])
    for fi in flist:
        if os.path.isfile(dir_out + "/" + fi.split("/")[-1]): continue
        # nrows= 5000
        df = pd_read_file(fi, n_pool=1)
        df = df.iloc[:nrows, :]
        log(fi, df.shape)
        df = df.sort_values('id')

        dfall = pd.DataFrame();
        nchunk = int(len(df) // chunk)
        for i in range(0, nchunk + 1):
            if i * chunk >= len(df): break
            i2 = i + 1 if i < nchunk else 3 * (i + 1)

            x0 = np_str_to_array(df[colemb].iloc[i * chunk:(i2 * chunk)].values)
            log('X topk')
            topk_dist, topk_idx = faiss_index.search(x0, topk)
            log('X', topk_idx.shape)

            dfi = df.iloc[i * chunk:(i2 * chunk), :][[colid]]
            dfi[f'{colid}_list'] = np_matrix_to_str3(topk_idx, map_idx_dict)  ### to actual id
            if return_dist:     dfi[f'dist_list'] = np_matrix_to_str(topk_dist)
            if return_simscore: dfi[f'sim_list'] = np_matrix_to_str_sim(topk_dist)

            dfall = pd.concat((dfall, dfi))

        dirout2 = dir_out + "/" + fi.split("/")[-1]

        pd_to_file(dfall, dirout2, show=1)
        kk = kk + 1
        if kk == 1: dfall.iloc[:100, :].to_csv(dirout2.replace(".parquet", ".csv"), sep="\t")

    log('All finished')
    return os.path.dirname(dirout2)


class faiss_KNNClassifier:
    """ Scikit-learn wrapper interface for Faiss KNN.
    Docs::

        n_neighbors : int (Default = 5)
                    Number of neighbors used in the nearest neighbor search.
        n_jobs : int (Default = None)
                 The number of jobs to run in parallel for both fit and predict.
                  If -1, then the number of jobs is set to the number of cores.
        algorithm : {'brute', 'voronoi'} (Default = 'brute')
            Algorithm used to compute the nearest neighbors:
                - 'brute' will use the :class: `IndexFlatL2` class from faiss.
                - 'voronoi' will use :class:`IndexIVFFlat` class from faiss.
                - 'hierarchical' will use :class:`IndexHNSWFlat` class from faiss.
            Note that selecting 'voronoi' the system takes more time during
            training, however it can significantly improve the search time
            on inference. 'hierarchical' produce very fast and accurate indexes,
            however it has a higher memory requirement. It's recommended when
            you have a lots of RAM or the dataset is small.
            For more information see: https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index
        n_cells : int (Default = 100)
            Number of voronoi cells. Only used when algorithm=='voronoi'.
        n_probes : int (Default = 1)
            Number of cells that are visited to perform the search. Note that the
            search time roughly increases linearly with the number of probes.
            Only used when algorithm=='voronoi'.
        References
        ----------
        Johnson Jeff, Matthijs Douze, and Hervé Jégou. "Billion-scale similarity
        search with gpus." arXiv preprint arXiv:1702.08734 (2017).
    """

    def __init__(self,
                 n_neighbors=5,
                 n_jobs=None,
                 algorithm='brute',
                 n_cells=100,
                 n_probes=1):

        self.n_neighbors = n_neighbors
        self.n_jobs = n_jobs
        self.algorithm = algorithm
        self.n_cells = n_cells
        self.n_probes = n_probes

        import faiss
        self.faiss = faiss

    def predict(self, X):
        """Predict the class label for each sample in X.
        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input data.
        Returns
        -------
        preds : array, shape (n_samples,)
                Class labels for samples in X.
        """
        idx = self.get_topk(X, self.n_neighbors, return_distance=False)
        class_idx = self.y_[idx]
        counts = np.apply_along_axis(
            lambda x: np.bincount(x, minlength=self.n_classes_), axis=1,
            arr=class_idx.astype(np.int16))
        preds = np.argmax(counts, axis=1)
        return preds

    def get_topk(self, X, n_neighbors=None, return_distance=True):
        """Finds the K-neighbors of a point.
        Docs::

            X : array of shape (n_samples, n_features)
                The input data.
            n_neighbors : int
                Number of neighbors to get (default is the value passed to the
                constructor).
            return_distance : boolean, optional. Defaults to True.
                If False, distances will not be returned
            Returns
            -------
            dists : list of shape = [n_samples, k]
                The distances between the query and each sample in the region of
                competence. The vector is ordered in an ascending fashion.
            idx : list of shape = [n_samples, k]
                Indices of the instances belonging to the region of competence of
                the given query sample.
        """
        if n_neighbors is None:
            n_neighbors = self.n_neighbors

        elif n_neighbors <= 0:
            raise ValueError("Expected n_neighbors > 0."
                             " Got {}" .format(n_neighbors))
        else:
            if not np.issubdtype(type(n_neighbors), np.integer):
                raise TypeError(
                    "n_neighbors does not take {} value, "
                    "enter integer value" .format(type(n_neighbors)))

        from sklearn.utils.validation import check_is_fitted
        check_is_fitted(self, 'index_')

        X = np.atleast_2d(X).astype(np.float32)
        dist, idx = self.index_.search(X, n_neighbors)
        if return_distance:
            return dist, idx
        else:
            return idx

    def predict_proba(self, X):
        """Estimates the posterior probabilities for sample in X.
        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input data.
        Returns
        -------
        preds_proba : array of shape (n_samples, n_classes)
                          Probabilities estimates for each sample in X.
        """
        idx = self.get_topk(X, self.n_neighbors, return_distance=False)
        class_idx = self.y_[idx]
        counts = np.apply_along_axis(
            lambda x: np.bincount(x, minlength=self.n_classes_), axis=1,
            arr=class_idx.astype(np.int16))

        preds_proba = counts / self.n_neighbors

        return preds_proba

    def fit(self, X, y):
        """Fit the model according to the given training data.
        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            Data used to fit the model.
        y : array of shape (n_samples)
            class labels of each example in X.
        """
        X = np.atleast_2d(X).astype(np.float32)
        X = np.ascontiguousarray(X)
        d = X.shape[1]  # dimensionality of the feature vector
        self._prepare_knn_algorithm(X, d)
        self.index_.add(X)
        self.y_ = y
        self.n_classes_ = np.unique(y).size
        return self

    def _prepare_knn_algorithm(self, X, d):
        if self.algorithm == 'brute':
            self.index_ = self.faiss.IndexFlatL2(d)
        elif self.algorithm == 'voronoi':
            quantizer = self.faiss.IndexFlatL2(d)
            self.index_ = self.faiss.IndexIVFFlat(quantizer, d, self.n_cells)
            self.index_.train(X)
            self.index_.nprobe = self.n_probes
        elif self.algorithm == 'hierarchical':
            self.index_ = self.faiss.IndexHNSWFlat(d, 32)
            self.index_.hnsw.efConstruction = 40
        else:
            raise ValueError("Invalid algorithm option."
                             " Expected ['brute', 'voronoi', 'hierarchical'], "
                             "got {}" .format(self.algorithm))



#########################################################################################################
############## Loader of embeddings #####################################################################
def embedding_cosinus_scores_pairwise(embs:np.ndarray, word_list:list=None, is_symmetric=False):
    """ Pairwise Cosinus Sim scores
    Doc::

           embs   = np.random.random((10,200))
           idlist = [str(i) for i in range(0,10)]
           df = sim_scores_fast(embs:np, idlist, is_symmetric=False)
           df[[ 'id1', 'id2', 'sim_score'  ]]

    """
    import copy, numpy as np
    # from sklearn.metrics.pairwise import cosine_similarity
    n= len(embs)
    word_list = np.arange(0, n) if word_list is None else word_list
    dfsim = []
    for i in  range(0, len(word_list) - 1) :
        vi = embs[i,:]
        normi = np.sqrt(np.dot(vi,vi))
        for j in range(i+1, len(word_list)) :
            # simij = cosine_similarity( embs[i,:].reshape(1, -1) , embs[j,:].reshape(1, -1)     )
            vj = embs[j,:]
            normj = np.sqrt(np.dot(vj, vj))
            simij = np.dot( vi ,  vj  ) / (normi * normj)
            dfsim.append([ word_list[i], word_list[j],  simij   ])
            # dfsim2.append([ nwords[i], nwords[j],  simij[0][0]  ])

    dfsim  = pd.DataFrame(dfsim, columns= ['id1', 'id2', 'sim_score' ] )

    if is_symmetric:
        ### Add symmetric part
        dfsim3 = copy.deepcopy(dfsim)
        dfsim3.columns = ['id2', 'id1', 'sim_score' ]
        dfsim          = pd.concat(( dfsim, dfsim3 ))
    return dfsim







########################################################################################################
if 'custom_code':
    def ztest_create_fake_df(dirout="./ztmp/", nrows=100):
        """ Creates a fake embeddingdataframe
        """
        res  = Box({})
        n    = nrows
        mdim = 50

        #### Create fake user ids
        word_list = [ 'a' + str(i) for i in range(n)]
        emb_list  = []
        for i in range(n):
            emb_list.append( ','.join([str(x) for x in np.random.random(mdim) ])  )

        df = pd.DataFrame()
        df['id']  = word_list
        df['emb'] = emb_list
        res.df    = df

        #### export on disk
        res.dir_parquet = dirout + "/emb_parquet/db_emb.parquet"
        pd_to_file(df, res.dir_parquet , show=1)

        #### Write on text:
        res.dir_text   = dirout + "/word2vec_export.vec"
        log( res.dir_text )
        with open(res.dir_text, mode='w') as fp:
            fp.write("word2vec\n")
            for i,x in df.iterrows():
              emb  = x['emb'].replace(",", "")
              fp.write(  f"{x['id']}  {emb}\n")

        return res


    def pd_to_onehot(dflabels: pd.DataFrame, labels_dict: dict = None) -> pd.DataFrame:
        """ Label INTO 1-hot encoding   {'gender': ['one', 'two']  }
        Docs::

            dflabels (pd.dataframe): The input data. df[['id', 'gender']]
            labels_dict (dict) : key is column name, value categorical data. {'gender': ['one', 'two']  }

            return dataframe df[['id', 'gender', 'gender_onehot']]
    
        """
        if labels_dict is not None:
            for ci, catval in labels_dict.items():
                dflabels[ci] = pd.Categorical(dflabels[ci], categories=catval)
    
        labels_col = labels_dict.keys()
    
        for ci in labels_col:
            dfi_1hot = pd.get_dummies(dflabels, columns=[ci])  ### OneHot
            dfi_1hot = dfi_1hot[[t for t in dfi_1hot.columns if ci in t]]  ## keep only OneHot
            dflabels[ci + "_onehot"] = dfi_1hot.apply(lambda x: ','.join([str(t) for t in x]), axis=1)
            #####  0,0,1,0 format   log(dfi_1hot)
        return dflabels



    def topk_custom(topk=100, dirin=None, pattern="df_*", filter1=None):
        """  python prepro.py  topk    |& tee -a  /data/worpoch_261/topk/zzlog.py


        """
        from utilmy import pd_read_file
        import cv2

        filter1 = "all"    #### "article"

        dirout  = dirin + "/topk/"
        os.makedirs(dirout, exist_ok=True)
        log(dirin)

        #### Load emb data  ###############################################
        df        = pd_read_file(  dirin + f"/{pattern}.parquet", n_pool=10 )
        log(df)
        df['id1'] = df['id'].apply(lambda x : x.split(".")[0])


        #### Element X0 ######################################################
        colsx = [  'masterCategory', 'subCategory', 'articleType' ]  # 'gender', , 'baseColour' ]
        df0   = df.drop_duplicates( colsx )
        log('Reference images', df0)
        llids = list(df0.sample(frac=1.0)['id'].values)


        for idr1 in llids :
            log(idr1)
            #### Elements  ####################################################
            ll = [  (  idr1,  'all'     ),
                    # (  idr1,  'article' ),
                    (  idr1,  'color'   )
            ]


            for (idr, filter1) in ll :
                dfi     = df[ df['id'] == idr ]
                log(dfi)
                if len(dfi) < 1: continue
                x0      = np.array(dfi['pred_emb'].values[0])
                xname   = dfi['id'].values[0]
                log(xname)

                #### 'gender',  'masterCategory', 'subCategory',  'articleType',  'baseColour',
                g1 = dfi['gender'].values[0]
                g2 = dfi['masterCategory'].values[0]
                g3 = dfi['subCategory'].values[0]
                g4 = dfi['articleType'].values[0]
                g5 = dfi['baseColour'].values[0]
                log(g1, g2, g3, g4, g5)

                xname = f"{g1}_{g4}_{g5}_{xname}".replace("/", "-")

                if filter1 == 'article' :
                    df1 = df[ (df.articleType == g4) ]

                if filter1 == 'color' :
                    df1 = df[ (df.gender == g1) & (df.subCategory == g3) & (df.articleType == g4) & (df.baseColour == g5)  ]
                else :
                    df1 = copy.deepcopy(df)
                    #log(df)

                ##### Setup Faiss queey ########################################
                x0      = x0.reshape(1, -1).astype('float32')
                vectors = np.array( list(df1['pred_emb'].values) )
                log(x0.shape, vectors.shape)

                dist, rank = topk_nearest_vector(x0, vectors, topk= topk)
                # print(dist)
                df1              = df1.iloc[rank[0], :]
                df1['topk_dist'] = dist[0]
                df1['topk_rank'] = np.arange(0, len(df1))
                log( df1 )
                df1.to_csv( dirout + f"/topk_{xname}_{filter1}.csv"  )

                img_list = df1['id'].values
                log(str(img_list)[:30])

                log('### Writing images on disk  ###########################################')
                import diskcache as dc
                db_path = "/dev/shm/train_npz/small//img_tean_nobg_256_256-1000000.cache"
                cache   = dc.Cache(db_path)
                print('Nimages', len(cache) )

                dir_check = dirout + f"/{xname}_{filter1}/"
                os.makedirs(dir_check, exist_ok=True)
                for i, key in enumerate(img_list) :
                    if i > 15: break
                    img  = cache[key]
                    img  = img[:, :, ::-1]
                    key2 = key.split("/")[-1]
                    cv2.imwrite( dir_check + f"/{i}_{key2}"  , img)
                log( dir_check )


    
    

################################################################################################################




    
 
    
###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()





def zz_faiss_topk_calc_old(df=None, root=None, colid='id', colemb='emb',
                        faiss_index:str="", topk=200, dirout=None, npool=1, nrows=10**7, nfile=1000,
                        colkey='idx', colval='id',
                        return_simscore=False, return_dist=False,
                        **kw

                        ):

   """Calculate top-k for each 'emb' vector of dataframe in parallel batch.
   Doc::

        df (str or pd.dataframe)  : Path or DF   df[['id', 'embd' ]]
        colid (str)               : Column name for id. (Default = 'id')
        colemb (str)              : Column name for embedding. (Default = 'emb')
        faiss_index (str)         : Path to index. (Default = "")
        topk (int)                : Number of nearest neighbors to fetch. (Default = 200)
        dirout (str)              : Results path.
        npool (int)               : num_cores for parallel processing. (Default = 1)
        nfile (int)               : Number of files to process. (Default = 1000)
        colkey (str)              : map_idx.parquet id col. (Default = 'id')
        colval (str)              : map_idx.parquet idx col. (Default = 'idx')
        return_simscore (boolean) : optional  If True, score will returned. (Defaults to False.)
        return_dist(boolean)      : optional If True, distances will returned. (Defaults to False.)
        https://github.com/facebookresearch/faiss/issues/632
        dis = 2 - 2 * sim
   """

   faiss_index = ""  if faiss_index is None  else faiss_index
   if isinstance(faiss_index, str) :
        faiss_path  = faiss_index
        faiss_index = faiss_load_index(db_path=faiss_index)
   faiss_index.nprobe = 12  # Runtime param. The number of cells that are visited for search.
   log('Faiss Index: ', faiss_index)


   ########################################################################
   if isinstance(df, list):    ### Multi processing part
        if len(df) < 1 : return 1
        flist = df[0]
        root     = os.path.abspath( os.path.dirname( flist[0] + "/../../") )  ### bug in multipro
        dirin    = root + "/df/"
        dir_out  = dirout

   elif isinstance(df, str) : ### df == string path
        root    = df
        dirin   = root
        dir_out = dirout
        flist   = sorted(glob.glob(dirin))
   else :
       raise Exception('Unknonw path')

   log('dir_in',  dirin)
   log('dir_out', dir_out)
   flist = flist[:nfile]
   if len(flist) < 1: return 1
   log('Nfile', len(flist), flist )


   ####### Parallel Mode ################################################
   if npool > 1 and len(flist) > npool :
        log('Parallel mode')
        from utilmy.parallel  import multiproc_run, multiproc_tochunk
        ll_list = multiproc_tochunk(flist, npool = npool)
        multiproc_run(faiss_topk_calc_old, ll_list, npool, verbose=True, start_delay= 5,
                      input_fixed = { 'faiss_index': faiss_path }, )
        return 1


   ####### Single Mode #################################################
   dirmap       = faiss_path.replace("faiss_trained", "map_idx").replace(".index", '.parquet')
   map_idx_dict = db_load_dict(dirmap,  colkey = colkey, colval = colval )

   chunk  = 200000
   kk     = 0
   os.makedirs(dir_out, exist_ok=True)
   dirout2 = dir_out
   flist = [ t for t in flist if len(t)> 8 ]
   log('\n\nN Files', len(flist), str(flist)[-100:]  )
   for fi in flist :
       if os.path.isfile( dir_out + "/" + fi.split("/")[-1] ) : continue
       # nrows= 5000
       df = pd_read_file( fi, n_pool=1  )
       df = df.iloc[:nrows, :]
       log(fi, df.shape)
       df = df.sort_values('id')

       dfall  = pd.DataFrame()   ;    nchunk = int(len(df) // chunk)
       for i in range(0, nchunk+1):
           if i*chunk >= len(df) : break
           i2 = i+1 if i < nchunk else 3*(i+1)

           x0 = np_str_to_array( df[colemb].iloc[ i*chunk:(i2*chunk)].values    )
           log('X topk')
           topk_dist, topk_idx = faiss_index.search(x0, topk)
           log('X', topk_idx.shape)

           dfi                   = df.iloc[i*chunk:(i2*chunk), :][[ colid ]]
           dfi[ f'{colid}_list'] = np_matrix_to_str2( topk_idx, map_idx_dict)  ### to actual id
           if return_dist:     dfi[ f'dist_list']  = np_matrix_to_str( topk_dist )
           if return_simscore: dfi[ f'sim_list']   = np_matrix_to_str_sim( topk_dist )

           dfall = pd.concat((dfall, dfi))

       dirout2 = dir_out + "/" + fi.split("/")[-1]

       pd_to_file(dfall, dirout2, show=1)
       kk    = kk + 1
       if kk == 1 : dfall.iloc[:100,:].to_csv( dirout2.replace(".parquet", ".csv")  , sep="\t" )

   log('All finished')
   return os.path.dirname( dirout2 )

    
