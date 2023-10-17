from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.query import (PreparedStatement,  SimpleStatement,  BatchStatement, BatchType)
from cassandra import ConsistencyLevel
import ssl
import time
from simplek8s.config_reader import ConfigReader

class CassConn(object):
    def __init__(self,config_file_path=None):
        self.config = ConfigReader(config_file_path).config

    def make_connection(self,cluster_name,keyspace_name=None):
        hosts = self.config.get('cassandra',f'{cluster_name}_hosts').split(',')
        uname = self.config.get('cassandra',f'{cluster_name}_uname')
        pword = self.config.get('cassandra',f'{cluster_name}_pword')
        kspace = self.config.get('cassandra',f'{cluster_name}_keyspace')
        if keyspace_name is None:
            keyspace_name = kspace
        port  = int(self.config.get('cassandra',f'{cluster_name}_port'))
        timeout = None
        try:
            timeout = float(self.config.get('cassandra','pmaster_timeout'))
        except Exception as e:
            pass
        auth_provider = PlainTextAuthProvider(username=uname, password=pword)
        connection = Cluster(hosts, port=port,auth_provider=auth_provider, connect_timeout=5.0)
        session = connection.connect(keyspace_name,wait_for_all_pools=True)
        #session.set_keyspace(keyspace_name)
        session.default_timeout = timeout
        return connection, session

    def insert_multi_new(self, in_session, query, records, sync=True, max_try=2, batch_size=25):
        """
        @query: "INSERT INTO table (field1, field2, field3,...) VALUES (?, ?, ?, ...)"
        """ 
        insert_query = in_session.prepare(query)
        success = True
        print (f'inserting with batch size: {batch_size}')
        if len(records) > 0:
           cnt = 0
           success = False
           batch = BatchStatement(BatchType.LOGGED)
           for record in records:
               batch.add(insert_query,record)
               cnt += 1
               if cnt >= len(records) or len(batch) >= batch_size:
                   attempt = 0
                   while attempt <= max_try:
                       try:
                           attempt += 1
                           if sync:
                               future = in_session.execute(batch)
                           else:
                               future = in_session.execute_async(batch)
                           success= True
                           batch.clear() # = BatchStatement(BatchType.LOGGED)
                       except Exception as cass_err:
                           time.sleep(attempt*5)
                           success = False
                           if attempt > max_try:
                               raise Exception(f'too many tries {query}: cnt: {cnt} {cass_err}')
        return success

    def insert_multi(session, query, data_map, sync=True, max_try=2):
        attempt = 0
        success = True
        while len(data_map) > 0:
            try:
                attempt += 1
                batch = BatchStatement(BatchType.LOGGED)
                for key, value in data_map.items():
                    batch.add(query, (key,value,))
                if sync:
                    future = session.execute(batch)
                else:
                    future = session.execute_async(batch)
                success = True
                break
            except Exception as cerror:
                time.sleep(attempt*5)
                success= False
                if attempt > max_try:
                    raise Exception(f" too many tries {query}: {cerror}")
        return success

    def read_multi(session, query, key_list, batch_size=25, m_concurrent=1, max_try=2):
        res_map = dict()
        attempt = 0
        while len(key_list) > 0:
            attempt += 1
            try:
                res = execute_concurrent_with_args(session, query, key_list, concurrency=m_concurrent)    
                for success, result in res:
                    if not sucess:
                        if attempt > max_try:
                            raise Exception(f" too many tries {query}")
                        time.sleep(5*attampt)
                        continue
                    for key, value in result:
                        res_map[key] = value
                    break
            except Exception as cerror:
                if attampt > max_try:
                    raise Exception(f" too many tries {query}: {cerror}")
                time.sleep(5*attempt)
        return res_map

    @property
    def product_conn(self):
        if not hasattr(self, '_product_conn'):
            self._product_master_conn, self._product_master_session = self.make_connection('offline','productmaster')
        return self._product_master_session

