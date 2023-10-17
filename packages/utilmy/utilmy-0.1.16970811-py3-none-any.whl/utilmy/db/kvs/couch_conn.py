import zlib
from datetime import timedelta
import couchbase
import couchbase_core
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator, ClusterOptions
from couchbase.bucket import Bucket
# from simplek8s.config_reader import ConfigReader

class CouchConn(object):
    def __init__(self,config_file_path=None):
        self.config = ConfigReader(config_file_path).config

    def make_conn(self,name):
        hosts = self.config.get('couchbase',f'{name}_hosts')
        bucket = self.config.get('couchbase',f'{name}_bucket')
        timeout = float(self.config.get('couchbase',f'{name}_timeout'))
        password = self.config.get('couchbase',f'{name}_user_pwd')
        uname = self.config.get('couchbase',f'{name}_user')
        cluster = Cluster(f'couchbase://{hosts}?enable_tracing=false',ClusterOptions(PasswordAuthenticator(uname,password)),quiet=True)
        couch_bucket= cluster.bucket(bucket)
        couch_bucket.quiet = True
        couch_bucket.default_format = couchbase_core._libcouchbase.FMT_BYTES
        #couch_bucket.enable_tracing = "no"
        return couch_bucket


    @property
    def sc_search_conn(self):
        if not hasattr(self,'_sc_search_conn') or self._sc_search_conn is None:
            self._sc_search_conn = self.make_conn('sc4_search')
        return self._sc_search_conn

    @property
    def top_conn(self):
        if not hasattr(self,'_sc_top_conn') or self._sc_top_conn is None:
            self._sc_top_conn = self.make_conn('sc4_top')
        return self._sc_top_conn

    @property
    def sc_control_conn(self):
        if not hasattr(self,'_sc_control_conn') or self._sc_control_conn is None:
            self._sc_control_conn = self.make_conn('sc4_control')
        return self._sc_control_conn

    @property
    def sc_user_conn(self):
        if not hasattr(self,'_sc_user_conn') or self._sc_user_conn is None:
            self._sc_user_conn = self.make_conn('sc4_user')
        return self._sc_user_conn











