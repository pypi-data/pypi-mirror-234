# -*- coding: utf-8 -*-
"""" Various utils
Docs::

    various


"""
import glob,json, os, pathlib, shutil, sys, tarfile,zipfile
import importlib, inspect
from typing import Optional, Union
import yaml


from utilmy.utilmy_base import to_file



#################################################################
from utilmy.utilmy_base import log, log2

def help():
    """function help"""
    from utilmy import help_create
    ss = help_create(__file__)
    print(ss)




#####################################################################
def test_all():
    """.
    Doc::

         cd utilmy
         python utils.py  test_all


     Easy to maintain and re-factors.
    """
    test1()
    # test2()
    # test3()
    # test4





def test1():
    """function test1.
    Doc::

            Args:
            Returns:

    """

    import utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()


    log("####### dataset_download_test() ..")
    test_file_path = dataset_donwload("https://github.com/arita37/mnist_png/raw/master/mnist_png.tar.gz", './testdata/tmp/test/dataset/')
    f = os.path.exists(os.path.abspath(test_file_path))
    assert f == True, "The file made by dataset_download_test doesn't exist"

    # dataset_donwload("https://github.com/arita37/mnist_png/raw/master/mnist_png.tar.gz", './testdata/tmp/test/dataset/')




    log("####### os_extract_archive() ..")
    #Testing os_extract_archive() extracting a zip file
    path1    = dirtmp + "/dirout/"
    path_zip = path1 + "test.zip"

    uu.to_file("Dummy test", path1 + "/zip_test.txt")

    ### https://docs.python.org/3/library/zipfile.html
    ### https://stackoverflow.com/questions/16091904/how-to-eliminate-absolute-path-in-zip-archive-if-absolute-paths-for-files-are-pr
    zf       = zipfile.ZipFile(path_zip, "w")
    zf.write(path1 + "/zip_test.txt", "zip_test.txt")
    zf.close()

    is_extracted  = os_extract_archive(
        file_path = path_zip,
        path      = drepo + "testdata/tmp/zip_test"
        #,archive_format = "auto"
        )
    assert is_extracted == True, "The zip wasn't extracted"

    # os_extract_archive("./testdata/tmp/test/dataset/mnist_png.tar.gz","./testdata/tmp/test/dataset/archive/", archive_format = "auto")





#####################################################################
from utilmy.utilmy_base import load_function_uri



def load_callable_from_uri(uri="mypath/myfile.py::myFunction"):
    """ Will return the function Python Object from the string path mypath/myfile.py::myFunction
    Doc::
            
            Args:
                uri:   
            Returns:
                
    """
    import importlib, inspect
    assert(len(uri)>0 and ('::' in uri or '.' in uri))
    if '::' in uri:
        module_path, callable_name = uri.split('::')
    else:
        module_path, callable_name = uri.rsplit('.',1)
    if os.path.isfile(module_path):
        module_name = '.'.join(module_path.split('.')[:-1])
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        module = importlib.import_module(module_path)
    return dict(inspect.getmembers(module))[callable_name]
        

def load_callable_from_dict(function_dict, return_other_keys=False):
    """function load_callable_from_dict.
    Doc::
            
            Args:
                function_dict:   
                return_other_keys:   
            Returns:
                
    """
    function_dict = function_dict.copy()
    uri = function_dict.pop('uri')
    func = load_callable_from_uri(uri)
    try:
        assert(callable(func))
    except:
        raise TypeError(f'{func} is not callable')
    arg = function_dict.pop('arg', {})
    if not return_other_keys:
        return func, arg
    else:
        return func, arg, function_dict
    







##########################################################################################
################### donwload  ############################################################
from utilmy.util_zip import dataset_donwload, os_extract_archive







###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()


