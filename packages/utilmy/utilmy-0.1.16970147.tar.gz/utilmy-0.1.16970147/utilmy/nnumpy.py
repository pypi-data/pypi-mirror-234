# -*- coding: utf-8 -*-
HELP= """



"""
import os, sys, time, datetime,inspect, json, yaml, gc
from collections import OrderedDict

###################################################################################################
from utilmy.utilmy_base import log, log2

def help():
    from utilmy import help_create
    ss  = help_create(__file__)  #### Merge test code
    ss += HELP
    print(ss)



###################################################################################################
def test_all():
    """#### python test.py   test_nnumpy
    """
    test1()


def test1():
    """
    """
    from utilmy import nnumpy as m


    log("#############", m.np_list_intersection)
    l1 = [1,2,3]
    l2 = [3,4,1]
    result = m.np_list_intersection(l1,l2)
    log(result)
    assert set(result).issubset(set(l1)),"Intersection item(s) not in first list"
    assert set(result).issubset(set(l2)),"Intersection item(s) not in second list"


    log("#############", m.np_add_remove)
    set_ = {1,2,3,4,5}
    add_element = 6
    remove_elements = [1,2]
    result = m.np_add_remove(set_,remove_elements,add_element)
    remove_elements = [1,2,3]
    assert set([add_element]).issubset(set(result)),"Added element not in revised set"


    res = m.to_dict(kw=[1,2,3])
    log("to_dict",res)
    assert isinstance(res,dict),"Return result not of dictionary type"
    m.to_timeunix(datex="2020-10-06")
    m.to_datetime("10/05/2021")


    log("#############",m.LRUCache)
    lrc = LRUCache()
    key = 'check'
    value = [1,2,3,4,5]
    lrc[key] = value
    res = lrc[key]
    assert res==value,"Item mismatch in getting and setting items"
    log(res)


    log("#############",m.fixedDict)
    od = OrderedDict()
    key = 'check'
    value = [1,2,3,4,5]
    od[key] = value
    fxd = fixedDict(od)
    key2 = 'check2'
    value2 = [9,7]
    fxd[key2] = value2
    res2 = fxd[key2]
    res = fxd[key]
    log(res)
    log(res2)
    assert res == value,"Item mismatch in getting and setting items"
    assert res2 == value2,"Item mismatch in getting and setting items"



def test1_convert():
    """function test1
    """
    from datetime import datetime

    int_ = 1
    float_ = 1.1
    log(is_int(int_))
    assert is_int(int_) == True, 'Failed to convert'
    log(is_float(float_))
    assert is_float(float_) == True, 'Failed to convert'
    log(to_float(int_))
    assert to_float(int_) == 1.0, 'Failed to convert'
    log(to_int(float_))
    assert to_int(float_) == 1, 'Failed to convert'

    log(to_timeunix(datex="2022-01-01"))
    assert to_timeunix(datex="2022-01-01"), 'Failed to convert'

    log(to_datetime(datetime.now()))
    assert to_datetime(datetime.now()), 'Failed to convert'




##############################################################################################################
####### Dict, Cache  #########################################################################################
class LRUCache(object):
    def __init__(self, max_size=4):
        """ LRUCache:__init__.
        Doc::
                    Args:
                        max_size:     
                    Returns:
                       
        """
        if max_size <= 0:
            raise ValueError

        self.max_size = max_size
        self._items = OrderedDict()

    def _move_latest(self, key):
        """ LRUCache:_move_latest.
        Doc::          
        """
        # Order is in descending priority, i.e. first element
        # is latest.
        self._items.move_to_end(key, last=False)

    def __getitem__(self, key, default=None):
        """ LRUCache:__getitem__.
        Doc::         
        """
        if key not in self._items:
            return default

        value = self._items[key]
        self._move_latest(key)
        return value

    def __setitem__(self, key, value):
        """ LRUCache:__setitem__.
        Doc::
                             
        """
        if len(self._items) >= self.max_size:
            keys = list(self._items.keys())
            key_to_evict = keys[-1]
            self._items.pop(key_to_evict)

        self._items[key] = value
        self._move_latest(key)
        
        
        
class fixedDict(OrderedDict):
    """  fixed size dict
          ddict = fixedDict(limit=10**6)

    """
    def __init__(self, *args, **kwds):
        """ fixedDict:__init__.
        Doc::
        """
        self.size_limit = kwds.pop("limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        """ fixedDict:__setitem__.
        Doc::                       
        """
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        """ fixedDict:_check_size_limit.
        Doc::         
        """
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


class dict_to_namespace(object):
    #### Dict to namespace
    def __init__(self, d):
        """ dict_to_namespace:__init__.
        Doc::                       
        """
        self.__dict__ = d


from typing import Any, Callable, Sequence, Dict
def dict_flatten(d, *,recursive: bool = True, join_fn= ".".join,) -> Dict[str, Any]:
    r"""Flatten dictionaries recursively.
    
    
    """
    result: Dict[str, Any] = {}
    for key, item in d.items():
        if isinstance(item, dict) and recursive:
            subdict = dict_flatten(item, recursive=True, join_fn=join_fn)
            for subkey, subitem in subdict.items():
                result[join_fn((key, subkey))] = subitem
        else:
            result[key] = item
    return result


def dict_unflatten(d, *, recursive= True, split_fn= lambda s: s.split(".", maxsplit=1),) -> Dict[str, Any]:
    r"""Unflatten dictionaries recursively.
    
    """
    result = {}
    for key, item in d.items():
        split = split_fn(key)
        result.setdefault(split[0], {})
        if len(split) > 1 and recursive:
            assert len(split) == 2
            subdict = dict_unflatten(
                {split[1]: item}, recursive=recursive, split_fn=split_fn
            )
            result[split[0]] |= subdict
        else:
            result[split[0]] = item
    return result





######################################################################################################
def np_list_intersection(l1, l2) :
  """function np_list_intersection.
  Doc::

  """
  return [x for x in l1 if x in l2]


def np_add_remove(set_, to_remove, to_add):
    """function np_add_remove.
    Doc::
            
            Args:
                set_:   
                to_remove:   
                to_add:   
            Returns:
                
    """
    # a function that removes list of elements and adds an element from a set
    result_temp = set_.copy()
    for element in to_remove:
        result_temp.remove(element)
    result_temp.add(to_add)
    return result_temp



######################################################################################################
def to_dict(**kw):
  """function to_dict.
  Doc::
            
  """
  ## return dict version of the params
  return kw


def to_timeunix(datex="2018-01-16"):
  """function to_timeunix.
  Doc::


  """
  if isinstance(datex, str)  :
     return int(time.mktime(datetime.datetime.strptime(datex, "%Y-%m-%d").timetuple()) * 1000)

  if isinstance(datex, datetime.date)  :
     return int(time.mktime( datex.timetuple()) * 1000)



def to_datetime(x) :
  """function to_datetime.
  Doc::
          
            
  """
  import pandas as pd
  return pd.to_datetime( str(x) )


def to_float(x, valdef=-1):
    """function to_float.
    Doc::     
    """
    try :
        return float(x)
    except :
        return valdef


def to_int(x, valdef=-1):
    """function to_int.                
    """
    try :
        return int(x)
    except :
        return -1


def is_int(x):
    """function is_int.
    """
    try :
        int(x)
        return True
    except:
        return False


def is_float(x):
    """function is_float. 
    """
    try :
        float(x)
        return True
    except:
        return False





###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()




