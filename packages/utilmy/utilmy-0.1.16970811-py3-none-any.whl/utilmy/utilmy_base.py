# -*- coding: utf-8 -*-
""" Main entry

"""
import os, sys, time, datetime,inspect, json, yaml, gc, random
# from tkinter import E
from box import Box


#### Typing ######################################################################################
## https://www.pythonsheets.com/notes/python-typing.html
### from utilmy import (  )
from typing import List, Optional, Tuple, Union, Dict, Any
Dict_none = Union[dict, None]
List_none = Union[list, None]
Int_none  = Union[None,int]
Path_type = Union[str, bytes, os.PathLike]

# try:
#     import numpy
#     npArrayLike = numpy.typing.ArrayLike
# except ImportError:
npArrayLike = Any




###################################################################################################
global verbose
def get_verbosity(verbose:int=None):
    """function get_verbosity :  get verbosity level from env variable (utilmy-verbose) [default: 3]
    """
    if verbose is None :
        verbose = os.environ.get('utilmy-verbose', 3)
    return verbose
verbose = get_verbosity()   ### Global setting


# def direpo(show=0):
#     """ Root folder of the repo in Unix / format
#     """
#     try :
#         import utilmy
#         dir_repo1 = os.path.dirname( utilmy.__path__[0] ).replace("\\","/") + "/"
#     except:
#         dir_repo1 = os.path.dirname( os.path.dirname(os.path.abspath(__file__))).replace("\\","/") + "/"

#     if show>0 :
#         log(dir_repo1)
#     return dir_repo1


def direpo(show=0):
    """ Root folder of the repo in Unix / format

    Params::
        show: print the path
    """
    import pkgutil

    dir_repo0 = pkgutil.get_loader("utilmy")
    if dir_repo0 is not None :
        dir_repo1 = os.path.dirname(os.path.dirname(dir_repo0.get_filename())).replace("\\","/") + "/"
    else :
        dir_repo1 = os.path.dirname( os.path.dirname(os.path.abspath(__file__))).replace("\\","/") + "/"

    if show:
        log(dir_repo1)
    return dir_repo1


# def dirpackage(show=0):
#     """ dirname of the file  utilmy_base.py  (ie site-packages/utilmy/ )
#     """
#     try :
#         import utilmy
#         dir_repo1 = os.path.abspath(utilmy.__path__[0]).replace("\\","/")
#     except:
#         dir_repo1 = os.path.dirname(os.path.abspath(__file__)).replace("\\","/") + "/"

#     if show>0 :
#         log(dir_repo1)
#     return dir_repo1


def dirpackage(show=0):
    """ dirname of the file  utilmy_base.py  (ie site-packages/utilmy/ )

    Params::
        show: print the path
    """
    import pkgutil
    dir_repo0 = pkgutil.get_loader("utilmy")
    if dir_repo0 is not None :
        dir_repo1 = os.path.dirname(dir_repo0.get_filename()).replace("\\","/") + "/"
    else :
        dir_repo1 = os.path.dirname( os.path.dirname(os.path.abspath(__file__))).replace("\\","/") + "/"
    if show>0 :
        log(dir_repo1)
    return dir_repo1


def dir_testinfo(tag="", verbose=1, ):
    """ Test infos:  return dir_repo, dir_tmp
    Docs::

        https://stackoverflow.com/questions/1095543/get-name-of-calling-functions-module-in-python
    """
    log("\n---------------------------------------------------------------------")
    drepo = direpo()
    dtmp  = os_get_dirtmp()
    assert os.path.exists(dtmp), f"Directory not found {dtmp}"

    import inspect
    fun_name = inspect.stack()[1].function
    if verbose>0 :
        print( inspect.stack()[1].filename,"::", fun_name,)

    dtmp  = dtmp + "/{tag}/"  if len(tag)  > 0  else dtmp + f"/{fun_name}/"
    os_makedirs(dtmp)

    log('repo: ', drepo)
    log('tmp_: ', dtmp)
    log("\n")
    return drepo, dtmp




###################################################################################################
def log(*s, **kw):
    print(*s, flush=True, **kw)

def log2(*s, **kw):
    if verbose >=2 : print(*s, flush=True, **kw)

def log3(*s, **kw):
    if verbose >=3 : print(*s, flush=True, **kw)

def loge(*s):
    print(*s,  flush=True)


def help():
    suffix = "\n\n\n###############################"
    ss     = help_create(modulename='utilmy', prefixs=None) + suffix
    log(ss)


###################################################################################################

###################################################################################################
def help_info(fun_name:str="os.system", doprint=True):
    """  get infos about a function/module

    Parmas::
        fun_name:  function name
        doprint:   print the info

    """
    from box import Box

    fun_name = fun_name.strip()
    fun_name = fun_name.replace(" ", ".")

    if ":"in fun_name :
        x = fun_name.split(":")
        module_name = x[0]
        fun_name    = x[-1]
    else  :
        x           = fun_name.split(".")
        module_name = ".".join(x[:-1])
        fun_name    = x[-1]


    func = import_function(fun_name, module_name, fuzzy_match=True)

    dd = Box({})
    dd.name = fun_name
    # dd.args = help_signature(func)
    dd.args = help_get_funargs(func)
    dd.doc  = help_get_docstring(func)
    dd.code = help_get_codesource(func)

    try :
            ss = ""
            for l in dd.args:
                l  = l.split("=")
                if len(l)> 1:
                    ss = ss + f"'{l[0]}': {l[1]}"  +","
                else :
                    ss = ss + l +","
            dd.args2 = "{" + ss[:-1]  + "}"
    except :
        dd.args2 = dd.args

    if doprint == 1 or doprint == True :
        log( 'Name: ', "\n",  module_name +"."+ fun_name, "\n" )
        log( 'args:', "\n",  dd.args2, "\n" )
        log( 'doc:',  "\n",  dd.doc, "\n" )
        return ''

    return dd


def help_get_codesource(func):
    """ Extract code source from func name"""
    import inspect
    try:
        lines_to_skip = len(func.__doc__.split('\n'))
    except AttributeError:
        lines_to_skip = 0
    lines = inspect.getsourcelines(func)[0]
    return ''.join( lines[lines_to_skip+1:] )


def help_get_docstring(func):
    """ Extract Docstring from function"""
    # import inspect
    try:
        lines = func.__doc__
    except AttributeError:
        lines = ""
    return lines


def help_get_funargs(func):
    """ Extract Func args  :  (a, b, x='blah') 
    
    returns list of arg+default value strings"""
    import inspect
    try:
        ll = str( inspect.signature(func) )
        ll = ll[1:-1]
        # ll = [ t.strip() for t in ll.split(", ")] 
        ll = [ t.strip() for t in ll.split(",")] # may not have space after comma

    except :
        # ll = ""
        ll = [] # return type should be same (list)
    return ll


def help_signature(f):
    """function help_signature
    Args:
        f:
    Returns:

    """
    from collections import namedtuple
    sig = inspect.signature(f)
    args = [
        p.name for p in sig.parameters.values()
        if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    ]
    varargs = [
        p.name for p in sig.parameters.values()
        if p.kind == inspect.Parameter.VAR_POSITIONAL
    ]
    varargs = varargs[0] if varargs else None
    keywords = [
        p.name for p in sig.parameters.values()
        if p.kind == inspect.Parameter.VAR_KEYWORD
    ]
    keywords = keywords[0] if keywords else None
    defaults = [
        p.default for p in sig.parameters.values()
        if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        and p.default is not p.empty
    ] or None
    argspec = namedtuple('Signature', ['args', 'defaults',
                                        'varargs', 'keywords'])
    return argspec(args, defaults, varargs, keywords)


def help_create(modulename='utilmy.nnumpy', prefixs=None):
    """ Extract code source from test code
    """
    if ".py" in modulename :
        modulename = os_module_name(modulename)

    import importlib
    prefixs = ['test']
    module1 = importlib.import_module(modulename)
    ll      = dir(module1)
    ll  = [ t for t in ll if prefixs[0] in t]
    ss  = ""
    for fname in ll :
        fun = import_function(fname, modulename)
        ss += help_get_codesource(fun)
    return ss


def help_get_all_methods(class_object):
    method_list = [method for method in dir(class_object) if method.startswith('__') is False]
    return method_list


###################################################################################################
def os_get_dirtmp(subdir=None, return_path=False):
    """ return dir temp for testing,...
    """
    import tempfile
    from pathlib import Path
    dirtmp = tempfile.gettempdir().replace("\\", "/")
    dirtmp = dirtmp + f"/{subdir}/" if subdir is not None else dirtmp
    os.makedirs(dirtmp, exist_ok=True)
    return Path(dirtmp) if return_path  else dirtmp


def os_module_name(filepath=None, mode='importname'):
    try:
        dir1 = os.path.abspath(filepath).replace("\\","/")

        if mode == 'importname':
            dir1 = 'utilmy.' + dir1.split("utilmy/")[-1].replace("/", ".").replace(".py", "")
            return dir1
    except :
        return direpo()


def get_loggers(mode='print', n_loggers=2, verbose_level=None):
    """function get_loggers
    Args:
        mode:
        n_loggers:
        verbose_level:
    Returns:

    """
    global verbose
    verbose = get_verbosity(verbose_level)

    if mode == 'print' :
        ttuple = [log]
        if n_loggers >=  2:    ttuple.append(log2)
        if n_loggers >=  3:    ttuple.append(log3)
        return tuple(ttuple)


#### Universal config Loader
#import utilmy.cconfigs.util_config
#from utilmy.cconfigs.util_config import config_load


###################################################################################################
def to_file(txt:str, fpath:str, mode='a'):
    """  Write the argument "s" in a file.

    Docs::

        Args:
            s (string):     string to write in the file.
            filep (string): Path of the file to write.

        Returns:
            None.

        Example:
            import utilmy as uu
            filep = "./"
            isok  = uu.to_file("Test string", fpath=filep)

    """
    os_makedirs(fpath) ### create folder
    txt= str(txt)
    try :
        with open(fpath, mode=mode) as fp:
            fp.write(txt)
        return True
    except Exception as e:
        time.sleep(5)
        with open(fpath, mode=mode) as fp:
            fp.write(txt)
        return True


class toFileSafe(object):
    def __init__(self,fpath):
        """ Thread Safe file writer Class
        Docs::
            tofile = toFileSafe('mylog.log')
            tofile.w("msg")
        """
        import logging
        logger = logging.getLogger('logsafe')
        logger.setLevel(logging.INFO)
        ch = logging.FileHandler(fpath)
        ch.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(ch)
        self.logger = logger

    def write(self, *s):
        """ toFileSafe:write
        Args:
            msg:
        Returns:
        """
        msg = " ".join([ str(si) for si in s ])
        self.logger.info( msg)

    def log(self, *s):
        """ toFileSafe:log
        """
        msg = " ".join([ str(si) for si in s ])
        self.logger.info( msg)

    def w(self, *s):
        """ toFileSafe:w
        Args:
            msg:
        Returns:
        """
        msg = " ".join([ str(si) for si in s ])
        self.logger.info( msg)




def find_fuzzy(word:str, wlist:list, threshold=0.0):
    """ Find closest fuzzy string
        ll = dir(utilmy)
        log(ll)
        find_fuzzy('help create fun arguu', ll)
    """
    # import numpy as np
    from difflib import SequenceMatcher as SM
    scores = [ SM(None, str(word), str(s2) ).ratio() for s2 in wlist  ]
    #log(scores)
    # imax = np.argmax(scores)
    imax = max(range(len(scores)), key=scores.__getitem__)

    if scores[imax] > threshold :
        most_similar = wlist[imax]
        return most_similar
    else :
        raise Exception( f'Not exist {word}  ; {wlist} ' )


def import_function(fun_name=None, module_name=None, fuzzy_match=False):
    """function import_function
    Args:
        fun_name:
        module_name:
        fuzzy_match:
    Returns:

    """
    import importlib

    try :
        if isinstance(module_name, str):
            module1 = importlib.import_module(module_name)
            if fuzzy_match: fun_name = find_fuzzy(fun_name, dir(module1) )
            func = getattr(module1, fun_name)
        else :
            func = globals()[fun_name]
        return func
    except Exception as e :
        msg = "Missing " + str(fun_name) + "," + str(dir(module1))
        raise Exception( msg )




def sys_exit(msg="exited",  err_int=0):
    """function sys_exit
    Args:
        msg:
        err_int:
    Returns:

    """
    import os, sys
    log(msg)
    ### exit with no error msg
    # sys.stderr = open(os.devnull, 'w')
    sys.stdout = sys.__stdout__ = open(os.devnull, 'w')
    sys.exit(err_int)


def sys_install(cmd=""):
    """function sys_install
    Args:
        cmd:
    Returns:

    """
    import os, sys, time
    log("Installing  ")
    log( cmd +"  \n\n ...") ; time.sleep(7)
    os.system(cmd )
    log( "\n\n\n############### Please relaunch python  ############## \n")
    log('Exit \n\n\n')


def pip_install(pkg_str=" pandas "):
    """
    try:
        import pandas as pd
    except ImportError:

    finally:
        import pandas as pd
    """
    import subprocess, sys
    clist = [sys.executable, "-m", "pip", "install",  ]  + pkg_str.split(" ")
    log("Installing", pkg_str)
    subprocess.check_call(clist)


# def sys_path_append(path="__file__", level_above=2):
#     """ Add parent folder as path for import """
#     import sys,os

#     fi   = os.path.abspath(path)
#     diri = os.path.dirname(fi)
#     for i in range(1,level_above):
#         diri = os.path.join(os.path.dirname(fi),os.pardir)

#     sys.path.append(diri)


def sys_path_append(path="__file__", level_above=2, position=-1):
    """ Add parent folder as path for import 
    
    Params::
        path: absolute or relative path to file/directory to add to sys.path (default=__file__)
        level_above: number of levels above the path to add to sys.path (default=2)
        position: position in sys.path to add the path (default=-1 for last position)
    """
    import sys,os

    fi   = os.path.abspath(path)
    direc = os.path.dirname(fi)
    
    direc = os.path.join(os.path.dirname(fi), *[os.pardir]*level_above)

    if position == -1:
        sys.path.append(direc)
    else:
        sys.path.insert(position, direc)



def load_function_uri(uri_name: str="MyFolder/myfile.py:my_function"):
    """ Load dynamically Python function/Class Object from string name
    Doc::

        myfun = load_function_uri(uri_name: str="MyFolder/utilmy_base.py:pd_random")

        -- Pandas CSV case : Custom MLMODELS One
        #"dataset"        : "mlmodels.preprocess.generic:pandasDataset"

        -- External File processor :
        "dataset"        : "MyFolder/preprocess/myfile.py:pandasDataset"


        Args:
            package (string): Package's name. Defaults to "mlmodels.util".
            name (string): Name of the function that belongs to the package.

        Returns:
            Returns the function of the package.

        Example:
            from utilmy import utils
            function = utils.load_function_uri("datetime.timedelta",)
            print(function())#0:00:00

    """
    import importlib, sys
    from pathlib import Path


    uri_name = uri_name.replace("\\", "/")

    if ":" in uri_name :
        pkg = uri_name.split(":")
        if ":/" in uri_name:  ### windows case
            pkg = uri_name.split("/")[-1].split(":")

        assert len(pkg) > 1, "  Missing :   in  uri_name module_name:function_or_class "
        package, name = pkg[0], pkg[1]
        package = package.replace(".py", "")

    else :
        pkg = uri_name.split(".")
        package = ".".join(pkg[:-1])
        package = package.replace(".py", "")
        name    = pkg[-1]


    try:
        #### Import from package mlmodels sub-folder
        return  getattr(importlib.import_module(package), name)

    except Exception as e1:
        try:
            ### Add Folder to Path and Load absoluate path module
            path_parent = str(Path(package).parent.parent.absolute())
            sys.path.append(path_parent)
            log(path_parent)

            #### import Absolute Path model_tf.1_lstm
            log(str(package))
            model_name   = Path(package).stem  # remove .py
            package_name = str(Path(package).parts[-2]) + "." + str(model_name)

            log(package_name, model_name)
            return  getattr(importlib.import_module(package_name), name)

        except Exception as e2:
            raise NameError(f"Module {pkg} notfound, {e1}, {e2}")







### Generic Glob  #################################################################################
from utilmy.oos import  glob_glob


from utilmy.util_download import google_download, download_google


###################################################################################################
def pd_random(ncols=7, nrows=100):
    """function pd_random
    Args:
        ncols:
        nrows:
    Returns:

    """
    import pandas as pd
    ll = [[ random.random() for i in range(0, ncols)] for j in range(0, nrows) ]
    df = pd.DataFrame(ll, columns = [str(i) for i in range(0,ncols)])
    return df



def pd_generate_data(ncols=7, nrows=100):
    """ Generate sample data for function testing categorical features
    """
    import numpy as np, pandas as pd
    np.random.seed(444)
    numerical    = [[ random.random() for i in range(0, ncols)] for j in range(0, nrows) ]
    df = pd.DataFrame(numerical, columns = [str(i) for i in range(0,ncols)])
    df['cat1']= np.random.choice(  a=[0, 1],  size=nrows,  p=[0.7, 0.3]  )
    df['cat2']= np.random.choice(  a=[4, 5, 6],  size=nrows,  p=[0.5, 0.3, 0.2]  )
    df['cat1']= np.where( df['cat1'] == 0,'low',np.where(df['cat1'] == 1, 'High','V.High'))
    return df



def pd_generate_data2(n_colnum=3, n_colcat=4, nrows=100, use_catstr=1, max_category=20, seed=4,
                      show=1):
    """Generate a pandas DataFrame with random data.

    Parameters:
        n_colnum (int): The number of numerical columns to generate (default: 3).
        n_colcat (int): The number of categorical columns to generate (default: 4).
        nrows (int): The number of rows in the DataFrame (default: 100).
        use_catstr (int): Flag indicating whether to use string representation for categorical values (default: 1).
        max_category (int): The maximum number of categories for each categorical column (default: 20).
        seed (int): The seed for the random number generator (default: 4).
        show (int): Flag indicating whether to display the data types of the generated DataFrame (default: 1).

    Returns:
        pd.DataFrame: The generated DataFrame with random data.
    """
    import numpy as np, pandas as pd
    np.random.seed(seed)
    # Numerical
    df = pd.DataFrame()
    for i in range(0, n_colnum):
        df[f'num{i}'] = np.random.random(size=nrows)

    # Categories
    for i in range(0, n_colcat):
        if use_catstr == 1:
            catval = [str(i) for i in range(0, 2 + np.random.randint(max_category))]
        else:
            catval = [i for i in range(0, 2 + np.random.randint(max_category))]

        df[f'cat{i}'] = np.random.choice(a=catval, size=nrows)

    if show>0:
        log(df.dtypes)
    return df



def pd_getdata(verbose=True):
    """data = test_get_data()
    df   = data['housing.csv']
    df.head(3)
    https://github.com/szrlee/Stock-Time-Series-Analysis/tree/master/data
    """
    import pandas as pd
    flist = [
        'https://raw.githubusercontent.com/samigamer1999/datasets/main/titanic.csv',
        'https://github.com/subhadipml/California-Housing-Price-Prediction/raw/master/housing.csv',
        'https://raw.githubusercontent.com/AlexAdvent/high_charts/main/data/stock_data.csv',
        'https://raw.githubusercontent.com/samigamer1999/datasets/main/cars.csv',
        'https://raw.githubusercontent.com/samigamer1999/datasets/main/sales.csv',
        'https://raw.githubusercontent.com/AlexAdvent/high_charts/main/data/weatherdata.csv'
    ]
    data = {}
    for url in flist :
        fname =  url.split("/")[-1]
        log( "\n", "\n", url, )
        df = pd.read_csv(url)
        data[fname] = df
        if verbose: log(df)
        # df.to_csv(fname , index=False)
    log(data.keys() )
    return data


class Index0(object):
    """ Class Maintain global index,
    Docs::
        file_name = f"{dtmp}/test_file_{int(time.time())}.txt"
        index = m.Index0(file_name, min_chars=8)
        ### 2 save some data
        data   = [ "testestest", 'duplicate', '5char', '### comment line, so skipped',]
        output = [ 'testestest', 'duplicate',  ]
        index.save(data)
        assert set(index.read()) == set(output), f"{output} , {index.read()}"
    """
    def __init__(self, findex:str="ztmp_file.txt", min_chars=5):
        """ Index0:__init__
        Args:
            findex (function["arg_type"][i]) :
        Returns:

        """
        self.findex        = findex
        self.min_chars = min_chars
        log(os.path.dirname(self.findex))
        os.makedirs(os.path.dirname(self.findex), exist_ok=True)
        if not os.path.isfile(self.findex):
            with open(self.findex, mode='a') as fp:
                fp.write("")

    def read(self,):
        """ Index0:read
        Args:
            :
        Returns:

        """
        with open(self.findex, mode='r') as fp:
            flist = fp.readlines()

        if len(flist) < 1 : return []
        flist2 = []
        for t  in flist :
            if len(t) >= self.min_chars and t[0] != "#"  :
                flist2.append( t.strip() )
        return flist2

    def save(self, flist:list):
        """ Index0:save
        Args:
            flist (function["arg_type"][i]) :
        Returns:

        """
        if len(flist) < 1 : return True
        ss = ""
        for fi in flist :
          ss = ss + str(fi) + "\n"
        # log(ss)
        with open(self.findex, mode='a') as fp:
            fp.write(ss )
        return True



###################################################################################################
def json_load(path) :
    """function json_load.
    Doc::

    """
    try :
        with open(path, mode='r') as fp:
            return json.load(fp)
    except Exception as e :
        log(e)
        return {}


def json_save(dd:dict, path:str) :
    """function json_save
    Doc::

    """
    class MyEncoder(json.JSONEncoder):
        ### to handle numpy type
        ### https://stackoverflow.com/questions/27050108/convert-numpy-type-to-python
        def default(self, obj):
            val = getattr(obj, "tolist", lambda: obj )()
            return val
            #return super(MyEncoder, self).default(obj)

    os_makedirs(path)
    try :
        with open(path, mode='w') as fp:
            json.dump(dd, fp, cls=MyEncoder)
    except Exception as e :
        log(e)


def pprint(dd,indent=3):
    if isinstance(dd, dict):
        log(json.dumps(dd, sort_keys=True, indent=indent,separators=(',', ': ') ))
    else :
        log(dd)



###################################################################################################
###### dates #####################################################################################
from utilmy.dates import (date_now_range, date_now)




###################################################################################################
###### Pandas #####################################################################################
from utilmy.parallel import (
    pd_read_file,    ### parallel reading
    pd_read_file2,
    pd_groupby_parallel,
)



from utilmy.ppandas import (
    #pd_random,
    pd_merge,
    pd_plot_multi,
    pd_plot_histogram,
    pd_filter,
    pd_to_file,
    pd_sample_strat,
    pd_cartesian,
    pd_col_bins,
    pd_dtype_reduce,
    pd_dtype_count_unique,
    pd_dtype_to_category,
    pd_dtype_getcontinuous,
    pd_del,
    pd_add_noise,
    pd_cols_unique_count,
    pd_show,
    pd_to_hiveparquet,
    pd_to_mapdict
)




#########################################################################################################
##### Utils numpy, list #################################################################################
#from utilmy.keyvalue import  (
#   diskcache_load,
#   diskcache_save,
#   diskcache_save2,
#   db_init, db_size, db_flush
#)



###################################################################################################
###### Parallel #####################################################################################
from utilmy.parallel import (
    multithread_run,
    multiproc_run
)




###################################################################################################
####### Numpy compute #############################################################################
from utilmy.nnumpy import (

    dict_to_namespace,
    to_dict,
    to_timeunix,
    to_datetime,
    np_list_intersection,
    np_add_remove,
    to_float,
    to_int,
    is_int,
    is_float

)



##### OS, cofnfig ######################################################################################
from utilmy.oos import(
    os_path_size,
    os_path_split,
    os_file_check,
    os_file_replacestring,
    os_walk,
    z_os_search_fast,
    os_search_content,
    os_get_function_name,
    os_variable_exist,
    os_variable_init,
    os_import,
    os_variable_check,
    os_variable_del,
    os_system_list,
    #os_to_file,
    os_get_os,
    os_get_ip,
    os_ram_info,
    os_sleep_cpu,
    os_cpu_info,
    # os_ram_object,
    os_copy,
    os_removedirs,
    os_getcwd,
    os_system,
    os_makedirs,
)

### Alias
os_remove = os_removedirs
#to_file   = os_to_file



################################################################################################
########  Configuration  #######################################################################
from utilmy.configs.util_config import (
config_load,
global_verbosity


)


######################################################################################################
######## External IO #################################################################################

######################################################################################################
###### Plot ##########################################################################################
#from utilmy.viz.vizhtml import (
#  images_to_html,   ### folder of images to HTML
#  test_getdata
# )



###################################################################################################
###### Debug ######################################################################################
from utilmy.debug import (
    print_everywhere,

    log10,
    log_trace,  ###(msg="", dump_path="", globs=None)  Debug with full trace message


    profiler_start,
    profiler_stop
)




def fire_Fire():
    """Executes `fire.Fire()` function while optionally enabling profiling using Pyinstrument.
    Docs::

        export pyinstrument=1
        python myfile.py   myfunction  --arg1 "ok"

        export pyinstrument=0
        python myfile.py   myfunction  --arg1 "ok"

        myfile.py: 
            def myfunction(arg1):
                print(arg1)

            if __name__ == "__main__":
                from utilmy import fire_Fire
                fire_Fire()


        If the `pyinstrument` environment variable is set to `"1"`, 
        the function starts the Profiler from the Pyinstrument library, 
        executes the `fire.Fire()` function, stops the Profiler, 
        and prints the profiling output. 
    """    
    if os.environ.get('pyinstrument', "0") == "1":
        print("##### Pyinstrument profiling Start ############")            
        import pyinstrument
        profiler = pyinstrument.Profiler()
        profiler.start()

        fire.Fire()
        profiler.stop()  
        print(profiler.output_text(unicode=True, color=True))
    else:
        fire.Fire()


def code_break():
    """ Break the code running and start local interpreter for debugging


    """
    import pdb 
    pdb.set_trace()



######################################################################################################
########Git ##########################################################################################
def git_repo_root():
    """function git_repo_root
    Args:
    Returns:

    """
    try :
        cmd = "git rev-parse --show-toplevel"
        mout, merr = os_system(cmd)
        path = mout.split("\n")[0]
        if len(path) < 1:  return None
    except : return None
    return path


def git_current_hash(mode='full'):
    """function git_current_hash
    Args:
        mode:
    Returns:

    """
    import subprocess
    label = None
    try:
        # label = subprocess.check_output(["git", "describe", "--always"]).strip();
        label = subprocess.check_output([ 'git', 'rev-parse', 'HEAD' ]).strip()
        label = label.decode('utf-8')
    except Exception as e:
        log('Error get git hash')
        label=  None
    return label




################################################################################################
################################################################################################
class Session(object) :
    """ Save Python Interpreter session on disk
        from util import Session
        sess = Session("recsys")
        sess.save( globals() )
    """
    def __init__(self, dir_session="ztmp/session/",) :
        """ Session:__init__
        Args:
            dir_session:
            :
        Returns:

        """
        os.makedirs(dir_session, exist_ok=True)
        self.dir_session =  dir_session
        self.cur_session =  None
        log(self.dir_session)

    def show(self) :
        """ Session:show
        Args:
        Returns:

        """
        import glob
        flist = glob.glob(self.dir_session + "/*" )
        log(flist)

    def save(self, name, glob=None, tag="") :
        """ Session:save
        Args:
            name:
            glob:
            tag:
        Returns:

        """
        path = f"{self.dir_session}/{name}{tag}/"
        self.cur_session = path
        os.makedirs(self.cur_session, exist_ok=True)
        self.save_session(self.cur_session, glob)

    def load(self, name, glob:dict=None, tag="") :
        """ Session:load
        Args:
            name:
            glob (function["arg_type"][i]) :
            tag:
        Returns:

        """

        if glob is None : 
            ValueError("glob is None, please pass globals() as glob")
        path = f"{self.dir_session}/{name}{tag}/"
        self.cur_session = path
        log(self.cur_session)
        self.load_session(self.cur_session , glob )


    def save_session(self, folder , globs, tag="" ) :
        """ Session:save_session
        Args:
            folder:
            globs:
            tag:
        Returns:

        """
        import pandas as pd
        os.makedirs( folder , exist_ok= True)
        lcheck = [ "<class 'pandas.core.frame.DataFrame'>", "<class 'list'>", "<class 'dict'>",
                 "<class 'str'>" ,  "<class 'numpy.ndarray'>" ]
        lexclude = {   "In", "Out", "get_ipython", 'exit','quit', 'Session',  }
        gitems = globs.items()
        for x, _ in gitems :
            if not x.startswith('_') and  x not in lexclude  :
                x_type =  str(type(globs.get(x) ))
                fname  =  folder  + "/" + x + ".pkl"
                try :
                    if "pandas.core.frame.DataFrame" in x_type :
                        pd.to_pickle( globs[x], fname)

                    elif x_type in lcheck or x.startswith('clf')  :
                        save( globs[x], fname )

                    log(fname)
                except Exception as e:
                    log(x, x_type, e)


    def load_session(self, folder, globs:dict=None) :
        """
        """
        log(folder)
        for dirpath, subdirs, files in os.walk( folder ):
            for x in files:
                filename = os.path.join(dirpath, x)
                x = x.replace(".pkl", "")
                try :
                    globs[x] = load(  filename )
                    log(filename)
                except Exception as e :
                    log(filename, e)


def save(dd, to_file="", verbose=False):
    """function save
    Args:
        dd:
        to_file:
        verbose:
    Returns:

    """
    import pickle, os
    os.makedirs(os.path.dirname(to_file), exist_ok=True)
    pickle.dump(dd, open(to_file, mode="wb") , protocol=pickle.HIGHEST_PROTOCOL)
    #if verbose : os_file_check(to_file)


def load(to_file=""):
    """function load
    Args:
        to_file:
    Returns:

    """
    import pickle
    # dd =   pickle.load(open(to_file, mode="rb")) # this often keeps the file open
    with open(to_file, mode="rb") as fp:
        dd = pickle.load(fp)
    return dd






###################################################################################################
###### Test #######################################################################################
def test_all():
    """function test_all
    """
    test1()
    # test_datenow()
    test_loadfunctionuri()


def test_loadfunctionuri():
    import utilmy as m
    drepo, dtmp = dir_testinfo()

    log("####", m.load_function_uri )
    ll = [ drepo + "utilmy/utilmy_base.py:test_dummy"

    ]
    for uri_name in ll :
        myclass = load_function_uri(uri_name=uri_name)
        result = myclass()
        assert myclass, 'FAILED -> load_function_uri'


def test_dummy():
    print('test dummy is ok')

def test1():
    import utilmy as m
    drepo, dtmp = dir_testinfo()

    ###################################################################
    log("\n##### git_repo_root  ", m.git_repo_root())
    assert not m.git_repo_root() == None, "err git repo"

    log("\n##### git_current_hash  ", m.git_current_hash())
    assert not m.git_current_hash() == None, "err git hash"


    ####################################################################
    log("\n##### global_verbosity  ")
    log('verbosity', m.global_verbosity(__file__, "config.json", 40,))
    log('verbosity', m.global_verbosity('../', "config.json", 40,))
    log('verbosity', m.global_verbosity(__file__))

    verbosity = 40
    gverbosity = m.global_verbosity(__file__)
    assert gverbosity == 5, "incorrect default verbosity"
    gverbosity =m.global_verbosity(__file__, "config.json", 40,)
    assert gverbosity == verbosity, "incorrect verbosity "


    ####################################################################
    file_name = f"{dtmp}/test_file_{int(time.time())}.txt"
    index = m.Index0(file_name, min_chars=8)
    data  = [ "testestest", 'duplicate', '5char', '8charlong', '### comment line, so skipped',]
    xtrue = [ 'testestest', 'duplicate', '8charlong'  ]
    index.save(data)
    x = set(index.read())
    assert not log(x) and x  == set(xtrue), f"{xtrue} <> {x}"

    ####################################################################

    log('#### Session')
    d0 = os_get_dirtmp()
    folder_name = f"{d0}/session"

    session = m.Session(folder_name)
    log(session)

    # save session
    glob = {'test': 'qwe rty yui'}
    res = session.save(name='session1', glob=glob)

    glob2 = {'test': 'nothing here'}
    res = session.load(name='session1', glob=glob2)

    assert glob2 == glob, 'FAILED, -> session error'

    ####################################################################

    def _test_func(arg1, arg2):
        """HELP doc string
        """
        return arg1 + arg2


    for name in [ 'utilmy.parallel', 'utilmy.nnumpy',  ]:
        log("\n####", name,"\n", m.help_create(name))
        # assert m.help_create(name), f'FAILED -> help_create {name}'
        log("\n####", name,"\n", m.help_info(name))
        # assert m.help_info(name), f'FAILED -> help_info {name}'

    log("\n####", m.help_get_codesource(func=_test_func))
    assert m.help_get_codesource(func=_test_func), 'FAILED -> help_get_codesource'

    log("\n####", m.help_get_docstring(func=_test_func))
    assert m.help_get_docstring(func=_test_func), 'FAILED -> help_get_docstring'

    log("\n####", m.help_get_funargs(func=_test_func))
    assert m.help_get_funargs(func=_test_func), 'FAILED -> help_get_funargs'

    log("\n####", m.help_signature(f=_test_func))
    assert m.help_signature(f=_test_func), 'FAILED -> help_signature'

    ####################################################################
    log("\n####", m.os_get_dirtmp)
    assert m.os_get_dirtmp(), 'FAILED -> os_get_dirtmp'
    assert m.os_get_dirtmp(subdir='test'), 'FAILED -> os_get_dirtmp'
    assert m.os_get_dirtmp(subdir='test', return_path=True), 'FAILED -> os_get_dirtmp'


    log("\n####", m.os_module_name(filepath='utilmy/utilmy_base.py'))
    assert m.os_module_name(filepath=drepo + 'utilmy/utilmy_base.py'), 'FAILED -> os_module_name'


    log("\n####", m.get_loggers())
    log("\n####", m.get_loggers(n_loggers=3))

    log("\n####", m.import_function(fun_name='test_all', module_name='utilmy'))
    assert m.import_function(fun_name='test_all', module_name='utilmy'), 'FAILED -> import_function'



    ####################################################################
    log("\n####", m.pd_random)
    df = m.pd_random(nrows=37, ncols=5)
    assert tuple(df.shape) == (37,5), f"FAILED -> Current shape: {df.shape}  vs True Shape 37,5 "

    log("\n####", m.pd_generate_data)
    df = m.pd_generate_data(nrows=25, ncols=7)
    assert tuple(df.shape) == (25,7+2), f"FAILED -> Current shape: {df.shape}  vs True Shape 25,7+2 "

    log("\n####", m.pd_getdata)
    files = ['titanic.csv', 'housing.csv', 'stock_data.csv', 'cars.csv', 'sales.csv', 'weatherdata.csv']
    assert list(m.pd_getdata(verbose=False).keys()) == files, f"FAILED -> all the files are not read properly"


    log("\n####", m.save, m.load)
    data_for_save = "data_for_save"
    m.save(data_for_save, "./testfile")
    loaded_data = m.load("./testfile")
    assert loaded_data == data_for_save, "FAILED -> save and load"


    log("\n####", m.to_file)
    to_file("some_text_data","./testfile",mode="w")
    with open("./testfile", mode="r") as fp:
        file_content = fp.read()
    assert file_content == "some_text_data", "FAILED -> to_file"

    os.remove("./testfile")



    ####################################################################
    score_word_dict = {}
    word = 'Catherine M Gitau'
    wlist = ['Catherine Gitau', 'Gitau Catherine']


    log("\n####", m.find_fuzzy)
    log(f"Similarity score of '{word}' with:")
    from difflib import SequenceMatcher as SM
    for wlist_word, score in zip(wlist, [SM(None, str(word), str(s2) ).ratio() for s2 in wlist]):
        score_word_dict[score] = wlist_word
        log(f"'{wlist_word}' - {score}")
    highest_score_word = score_word_dict[max(list(score_word_dict.keys()))]
    assert highest_score_word == m.find_fuzzy(word, wlist), f"FAILED -> find_fuzzy. Word with highest score should be {highest_score_word}, got {m.find_fuzzy(word, wlist)}"





###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()
