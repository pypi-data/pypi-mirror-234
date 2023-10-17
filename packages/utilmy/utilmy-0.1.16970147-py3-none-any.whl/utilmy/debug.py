# -*- coding: utf-8 -*-
"""Util for debugging
Doc::

    https://eliot.readthedocs.io/en/stable/

    pip install filprofiler

    https://github.com/alexmojaki/snoop




"""
import itertools, time, multiprocessing, pandas as pd, numpy as np, pickle, gc
import os, sys, time, datetime,inspect, json, yaml, gc
from collections import OrderedDict

###################################################################################################
from utilmy.utilmy_base import log, log2

def help():
    from utilmy import help_create
    ss  = help_create(__file__)  #### Merge test code
    print(ss)


###################################################################################################
def print_everywhere():
    """.
    Doc::
            
            https://github.com/alexmojaki/snoop
    """
    txt ="""
    import snoop; snoop.install()  ### can be used anywhere
    
    @snoop
    def myfun():
    
    from snoop import pp
    pp(myvariable)
        
    """
    import snoop
    snoop.install()  ### can be used anywhere"
    print("Decaorator @snoop ")


def log10(*s, nmax=60):
    """ Display variable name, type when showing,  pip install varname.
    Doc::
            
        
    """
    from varname import varname, nameof
    for x in s :
        print(nameof(x, frame=2), ":", type(x), "\n",  str(x)[:nmax], "\n")


def logvar(*s):
    """    ### Equivalent of print, but more :  https://github.com/gruns/icecream.
    Doc::
            
            pip install icrecream
            ic()  --->  ic| example.py:4 in foo()
            ic(var)  -->   ic| d['key'][1]: 'one'
        
    """
    from icecream import ic
    return ic(*s)




def profiler_start():
    """function profiler_start.
    Doc::
            
        from utilmy.util_debug import profiler_start, profiler_stop
        profiler_start()
        ...
        profiler_stop() 
                
    """
    ### Code profiling
    from pyinstrument import Profiler
    global profiler
    profiler = Profiler()
    profiler.start()


def profiler_stop():
    """function profiler_stop.
    Doc::
            
        from utilmy.util_debug import profiler_start, profiler_stop
        profiler_start()
        ...
        profiler_stop()        
                
    """
    global profiler
    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))




def log_debug_everywhere():
    """  Debug printer
    Docs ::

        https://github.com/alexmojaki/snoop
        import snoop; snoop.install()  ### can be used anywhere

        @snoop
        def myfun():

        from snoop import pp
        pp(myvariable)


    """
    txt ="""
        
    """
    import snoop
    snoop.install()  ### can be used anywhere"
    print("Decaorator @snoop ")


def logfull(*s, nmax=60):
    """ Display variable name, type when showing,  pip install varname

    """
    from varname import varname, nameof
    for x in s :
        print(nameof(x, frame=2), ":", type(x), "\n",  str(x)[:nmax], "\n")


def logfull2(*s):
    """    ### Equivalent of print, but more :  https://github.com/gruns/icecream
    pip install icrecream
    ic()  --->  ic| example.py:4 in foo()
    ic(var)  -->   ic| d['key'][1]: 'one'

    """
    from icecream import ic
    return ic(*s)


def log_trace(msg="", dump_path="", globs=None):
    """function log_trace
    Args:
        msg:
        dump_path:
        globs:
    Returns:

    """
    print(msg)
    import pdb;
    pdb.set_trace()





#####################################################################################
def os_typehint_check(fun):
    """
    Doc::
            # prints 
            # a -> arg is <class 'int'> , annotation is <class 'int'> / True
            # b -> arg is <class 'str'> , annotation is <class 'str'> / True
            # c -> arg is <class 'int'> , annotation is <class 'float'> / False

    """
    # def f(a: int, b: str, c: float):
    import inspect
    args = inspect.getfullargspec(fun).args
    annotations = inspect.getfullargspec(fun).annotations
    # annotations = f.__annotations__
    # print(type(locals()), locals())
    for x in args:
        type_info = type(locals()[x])
        print(x, '->','arg is', type_info, ',','annotation is', annotations[x],'/', type_info in annotations[x])



def os_get_function_name():
    import traceback
    try :
       return traceback.extract_stack(None, 2)[0][2]
    except : return ''


def os_get_function_parameters_and_values():
    import inspect 
    try :
        frame = inspect.currentframe().f_back
        args, _, _, values = inspect.getargvalues(frame)
        return ([(i, values[i]) for i in args])
    except: return ''    


def test2():
    def my_func(a, b, c=None):
        log('Running ' + get_function_name() + '(' + str(get_function_parameters_and_values()) +')')






###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()

