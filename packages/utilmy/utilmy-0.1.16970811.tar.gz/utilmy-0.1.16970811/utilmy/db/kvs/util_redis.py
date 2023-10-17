""" Fast redis client
Docs::

    pip install hiredis



"""
import time, random, string
from dataclasses import dataclass
from box import Box
import redis
from redis.cluster import RedisCluster, ClusterNode
import datetime

from utilmy import log


#################################################################################
#################################################################################
def test_all():
    #test_connection()
    #test_getput()
    test_getputmulti()


def test_all_cluster(config=None):
    test_cluster1()
    test_getputmulti()




def test_connection():
    # test connection failed
    try:
        client = redisClient(host='localsss', port=1123)
        assert False
    except ConnectionFailed:
        assert True

    # test connection success
    try:
        client = redisClient(host='localhost', port=6378, db=0)
        assert True
    except ConnectionFailed:
        assert False


def test_getput():
    client = redisClient(host='localhost', port=6378, db=0)
    client.put('foo', 'bar')
    res    = client.get('foo').decode('utf8')
    assert res == 'bar'


def randomStringGenerator(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def test_getputmulti():
    client = redisClient(host='localhost', port=6378, db=0)
    keyvalues = [['a', '1'], ['b', '2'], ['c', '3'], ['d', '4'], ['e', '5'], ['f', '6'], ['g', '7'], ['h', '8'], ['i', '9'], ['j', '10'], ['k', '11']]
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

    client.put_multi(keyvalues,3 )
    res = client.get_multi(keys, 5)
    assert len(res)  == len(keys)
    for i in range(len(keys)):
        # assert value
        assert keyvalues[i][1] == res[i].decode('utf-8')




########## Cluster ##################################################################
def test_cluster1():
    # test connection failed
    try:
        client = RedisClusterClient('localssss', 6379, [6379, ], 'bitnami')
        assert False
    except redis.exceptions.RedisClusterException:
        assert True


def test_cluster2():
    # test connection success
    try:
        client = RedisClusterClient('localhost', 6379, [6379, ], 'bitnami')
        assert True
    except redis.exceptions.RedisClusterException:
        assert False


def test_cluster3():
    client = RedisClusterClient('localhost', 6379, [6379, ], 'bitnami')
    client.put('foo', 'bar')
    res = client.get('foo').decode('utf8')
    assert res == 'bar'

def test_cluster_set_with_ttl():
    client = RedisClusterClient('localhost', 6379, [6379, ], 'bitnami')
    client.put('foo', 'bar', 1)
    time.sleep(1)
    res = client.get('foo')
    assert res == None

def test_cluster_getputmulti():
    client = RedisClusterClient('localhost', 6379, [6379, ], 'bitnami')
    keyvalues = [['a', '1'], ['b', '2'], ['c', '3'], ['d', '4'], ['e', '5'], ['f', '6'], ['g', '7'], ['h', '8'], ['i', '9'], ['j', '10'], ['k', '11'], ['l', '12']]
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', ]

    client.put_multi(keyvalues, 3)
    res = client.get_multi(keys, 5)
    assert len(res) == len(keys)   ###  11
    for i in range(len(keys)):
        # assert value
        assert keyvalues[i][1] == res[i].decode('utf-8')


def test_cluster_getmulti_5lastkey():
    client = RedisClusterClient('localhost', 6379, [6379, ], 'bitnami')
    keyvalues = [['a', '1'], ['b', '2'], ['c', '3'], ['d', '4'], ['e', '5'], ['f', '6'], ['g', '7'], ['h', '8'], ['i', '9'], ['j', '10'], ['k', '11'], ['l', '12']]
    keys = ['g', 'h', 'i', 'j', 'k']

    client.put_multi(keyvalues, 3)
    res = client.get_multi(keys, 3)

    leftoffset = 6
    assert len(res) == len(keys)   ###  5
    for i in range(len(keys) - 1):
        # assert value
        assert keyvalues[i+leftoffset][1] == res[i].decode('utf-8')


#################################################################################
#################################################################################
class RedisClusterClient:
    def __init__(self, host: str, port:str|int, ports: list(), password: str, read_from_replicas=True, encoding='utf-8', decode_response=True):
        nodes = list()
        for node_port in ports:
            nodes.append(ClusterNode(host=host, port=node_port))

        self.client = RedisCluster(
            startup_nodes=nodes,
            read_from_replicas=read_from_replicas,
            host=host,
            password=password,
            port=port,
            encoding=encoding,
            decode_response=decode_response)

        
        self.client.ping()


    def get(self, key):
        """get value from redis using key
        """
        return self.client.get(key)


    def put(self, key, val, ttl: float=None):
        """set value to key
        """
        self.client.set(key, val, ex=ttl)
        return True

    def put_multi(self, key_values, batch_size=500, transaction=False, nretry=3, ttl=None):
        """set multiple keys and values to redis
        Docs::

            key_values ([[key, value], ]): key and value as 2D list
            batch_size (int): number of batch.
            transaction (bool): enable MULTI and EXEC statements.
            nretry (int): number of retry
        """
        self.pipe = self.client.pipeline(transaction=False)
        n = len(key_values)
        n_batch = 1 +  int(len(key_values) // batch_size)

        ntotal = 0  
        for k in range(n_batch):
            for i in range(batch_size):
                ix  = k*batch_size + i 
                if ix >= n: break 
                key = key_values[ix][0]
                val = key_values[ix][1]
                # replace hset with set 
                # `batch get` will not found the key if order of element on the list is not the same
                # as order of list when setting value. because index of the key representing hash.
                self.pipe.set(key, val, ex=ttl)
                i += 1

            flag = True 
            ii   = 0
            while flag and ii < nretry:
                ii =  ii + 1 
                try :      
                    self.pipe.execute()
                    flag = False
                    ntotal += batch_size
                except Exception as e: 
                    log(e)
                    time.sleep(2)
                  
        return ntotal 


    def get_multi(self, keys, batch_size=500, transaction=False):
        """get multiple value using list of keys
        Parameters:
            keys (list(string)): list of keys
            batch_size (int): number of batch.
            transaction (bool): enable MULTI and EXEC statements.
        """
        self.pipe = self.client.pipeline(transaction=transaction)

        n       = len(keys)
        n_batch = int(n // batch_size)  + 1
        res     = []
        for k in range(n_batch):
            for i in range(batch_size):
                ix  = k*batch_size + i
                if ix >= n : break
                # replace hget with get 
                # `batch get` will not found the key if order of element on the list is not the same
                # as order of list when setting value. because index of the key representing hash.
                self.pipe.get(keys[ix])

            try :
                resk = self.pipe.execute()
                res  = res + resk
            except Exception as e : 
                log(e)   
                time.sleep(5)
                resk = self.pipe.execute()
                res  = res + resk

        return res



class redisClient:
    def __init__(self, host:  str = 'localhost', port: int = 6333, user='', password='',
                 config_file: str=None, db=0, config_keyname= 'redis', config_dict=None):
        """  hiredis client       
        Docs::

            host (str, ):             'localhost'
            port (int, ):              6333
            config_file (str, ):       None
            db (int, ):                   0
            config_keyname (str, ):  'redis'
            config_dict (_type_, ):   None

         Raises:
            ConnectionFailed: _description_
         """
        if isinstance(config_dict, dict) :
            self.cfg = config_dict

        elif isinstance(config_file, str):    
            from utilmy  import config_load
            self.cfg = config_load(config_file)
            self.cfg = self.cfg[config_keyname]

        else:
            self.cfg = { 'host': host, 'port': port, 'db': db,
                'user' : user, 'password': password
            }

        self.host = self.cfg['host']
        self.port = self.cfg['port']
        self.db = self.cfg['db']
        self.user = self.cfg['db']
        self.password = self.cfg['password']

        self.client = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        try:
            self.client.ping()
        except redis.exceptions.ConnectionError: 
            raise ConnectionFailed("Failed to connect to redis")
        except redis.exceptions.ResponseError:
            raise AuthenticationFailed("Invalid password")


    def get(self, key):
        """get value from redis using key
        """
        return self.client.get(key)


    def put(self, key, val, ttl=None):
        """set value to key
        """
        self.client.set(key, val, ex=ttl)
        return True

    def put_multi(self, key_values, batch_size=500, transaction=False, nretry=3, ttl=None):
        """set multiple keys and values to redis
        
        Parameters:
            key_values ([[key, value], ]): key and value as 2D list
            batch_size (int): number of batch.
            transaction (bool): enable MULTI and EXEC statements.
            nretry (int): number of retry
        """
        self.pipe = self.client.pipeline(transaction=False)
        n = len(key_values)
        n_batch = len(key_values) // batch_size

        ntotal = 0  
        for k in range(n_batch):
            for i in range(batch_size):
                ix  = k*batch_size + i 
                if ix >= n: break 
                key = key_values[ix][0]
                val = key_values[ix][1]
                # --> Important to document the issues in the code
                # replace hset with set 
                # `batch get` will not found the key if order of element on the list is not the same
                # as order of list when setting value. because index of the key representing hash.
                self.pipe.set(key, val, ex=ttl)
                i += 1

            flag = True 
            ii   = 0
            while flag and ii < nretry:
                ii =  ii + 1 
                try :      
                    self.pipe.execute()
                    flag = False
                    ntotal += batch_size
                except Exception as e: 
                    log(e)
                    time.sleep(2)
                  
        return ntotal 


    def get_multi(self, keys, batch_size=500, transaction=False):
        """get multiple value using list of keys
        Parameters:
            keys (list(string)): list of keys
            batch_size (int): number of batch.
            transaction (bool): enable MULTI and EXEC statements.
        """
        self.pipe = self.client.pipeline(transaction=transaction)

        n       = len(keys)
        n_batch = n // batch_size  + 1
        res = []
        for k in range(n_batch):
            for i in range(batch_size):
                ix  = k*batch_size + i
                if ix >= n : break
                try :
                    # --> Important to document the issues in the code
                    # replace hget with get 
                    # `batch get` will not found the key if order of element on the list is not the same
                    # as order of list when setting value. because index of the key representing hash.
                   self.pipe.get(keys[ix])
                except Exception as e :
                  log(e)   
                  time.sleep(5)
                  self.pipe.get(keys[ix])


            resk =  self.pipe.execute()
            res  = res + resk

        return res


class RedisQueries(object):
    def __init__(self,config_file=None):
        self.Redis_conn = redisClient(config_file = config_file)
        self.batch_size = 50

    @property
    def version_id(self):
        """
        """
        if not hasattr(self,'_zzz_version_id'):
            control_conn = self.Redis_conn
            self._zzz_version_id = control_conn.get('zzz_cfg_pending')
        return self._zzz_version_id

    def get_siid_to_title(self,siids):
        """
        """
        siid_to_title = dict()
        cad_map = self.Redis_conn.get_multi(keys)
        for siid, vals in cad_map.items():
            if len(vals) > 1:
                siid_to_title[siid] = vals[-1]
        return siid_to_title




#################################################################################
def randomStringGenerator(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ConnectionFailed(Exception):

    pass

class AuthenticationFailed(Exception):
    pass




############################################################################################################
if __name__ == '__main__':
    import fire
    fire.Fire()





