# -*- coding: utf-8 -*-
"""  Utilities related to OS : file in/out, System Infod, Memory/Variables
Doc::
    utilmy/oos.py
    -------------------------functions----------------------
    aaa_bash_help()
    glob_glob(dirin = "", file_list = [], exclude = "", include_only = "", min_size_mb = 0, max_size_mb = 500000, ndays_past = -1, nmin_past = -1, start_date = '1970-01-02', end_date = '2050-01-01', nfiles = 99999999, verbose = 0, npool = 1)
    help()
    os_copy(dirfrom = "folder/**/*.parquet", dirto = "", mode = 'file', exclude = "", include_only = "", min_size_mb = 0, max_size_mb = 500000, ndays_past = -1, nmin_past = -1, start_date = '1970-01-02', end_date = '2050-01-01', nfiles = 99999999, verbose = 0, dry = 0)
    os_copy_safe(dirin:str = None, dirout:str = None, nlevel = 5, nfile = 5000, logdir = "./", pattern = "*", exclude = "", force = False, sleep = 0.5, cmd_fallback = "", verbose = Trueimport shutil, time, os, globflist = [] ; dirinj = dirinnlevel) =  [] ; dirinj = dirinnlevel):)
    os_cpu_info()
    os_file_check(fpath:str)
    os_file_date_modified(dirin, fmt="%Y%m%d-%H = "%Y%m%d-%H:%M", timezone = 'Asia/Tokyo')
    os_file_info(dirin, returnval = 'list', date_format = 'unix')
    os_file_replacestring(findstr, replacestr, some_dir, pattern = "*.*", dirlevel = 1)
    os_get_function_name()
    os_get_ip()
    os_get_os()
    os_get_uniqueid(format = "int")
    os_getcwd()
    os_import(mod_name = "myfile.config.model", globs = None, verbose = True)
    os_makedirs(dir_or_file)
    os_merge_safe(dirin_list = None, dirout = None, nlevel = 5, nfile = 5000, nrows = 10**8, cmd_fallback  =  "umount /mydrive/  && mount /mydrive/  ", sleep = 0.3)
    os_monkeypatch_help()
    os_path_size(path  =  '.')
    os_path_split(fpath:str = "")
    os_process_list()
    os_ram_info()
    os_ram_sizeof(o, ids, hint = " deep_getsizeof(df_pd, set()
    os_remove(dirin = "folder/**/*.parquet", min_size_mb = 0, max_size_mb = 1, exclude = "", include_only = "", ndays_past = 1000, start_date = '1970-01-02', end_date = '2050-01-01', nfiles = 99999999, dry = 0)
    os_removedirs(path, verbose = False)
    os_search_content(srch_pattern = None, mode = "str", dir1 = "", file_pattern = "*.*", dirlevel = 1)
    os_sleep_cpu(cpu_min = 30, sleep = 10, interval = 5, msg =  "", verbose = True)
    os_system(cmd, doprint = False)
    os_system_list(ll, logfile = None, sleep_sec = 10)
    os_variable_check(ll, globs = None, do_terminate = True)
    os_variable_del(varlist, globx)
    os_variable_exist(x, globs, msg = "")
    os_variable_init(ll, globs)
    os_wait_processes(nhours = 7)
    os_walk(path, pattern = "*", dirlevel = 50)
    z_os_search_fast(fname, texts = None, mode = "regex/str")
    zz_os_remove_file_past(dirin = "folder/**/*.parquet", ndays_past = 20, nfiles = 1000000, exclude = "", dry = 1)
    -------------------------methods----------------------
    fileCache.__init__(self, dir_cache = None, ttl = None, size_limit = 10000000, verbose = 1)
    fileCache.get(self, path)
    fileCache.set(self, path:str, flist:list, ttl = None)
    -------------------------------------------------------
    https://github.com/uqfoundation/pox/tree/master/pox
"""
import os, sys, time, datetime,inspect, json, yaml, gc, pandas as pd, numpy as np, glob, re
import socket
from typing import Union
from pathlib import Path
from queue import Queue

#################################################################
from utilmy.utilmy_base import log, log2

def help():
    """function help
    """
    from utilmy import help_create
    ss = help_create(__file__)
    print(ss)


#################################################################
###### TEST #####################################################
def test_all():
    """ python  utilmy/oos.py test_all


    """
    test_filecache()
    test_globglob()
    test_os()





def test_globglob():
    """ python  utilmy/oos.py test_globglob
    """
    # import utilmy # unused import
    # drepo, dtmp = utilmy.dir_testinfo() # unused variable

    tlist= [
        "folder/test/file1.txt",
        "folder/test/tmp/1.txt",
        "folder/test/tmp/myfile.txt",
        "folder/test/tmp/record.txt",
        "folder/test/tmp/part.parquet",
        "folder/test/file2.txt",
        "folder/test/file3.txt"
    ]

    for path in tlist:
        os_makedirs(path)
        with open(path, mode='w') as fp :
            fp.write("details")
        assert os.path.exists( path) , "File doesn't exist"


    ####### Details #####################################################
    res = glob_glob(dirin="folder/**/*.txt")
    print(res)
    assert "folder/test/tmp/part.parquet" not in res, "Failed, glob_glob"

    res = glob_glob(dirin="folder/**/*.txt",exclude="file2.txt,1")
    print(res)
    assert "folder/test/tmp/part.parquet" not in res, "Failed, glob_glob"
    assert "folder/test/file2.txt" not in res, "Failed, glob_glob"
    assert "folder/test/tmp/1.txt" not in res, "Failed, glob_glob"
    assert "folder/test/file1.txt" not in res, "Failed, glob_glob"

    res = glob_glob(dirin="folder/**/*.txt",exclude="file2.txt,1",include_only="file")
    print(res)
    assert "folder/test/file3.txt"  in res, "Failed, glob_glob"
    assert "folder/test/tmp/myfile.txt"  in res, "Failed, glob_glob"

    res = glob_glob(dirin="folder/**/*",nfiles=5)
    print(res)
    assert len(res) == 5, "Failed, glob_glob"

    res = glob_glob(dirin="folder/**/*.txt",ndays_past=0,nmin_past=5,verbose=1)
    print(res)

    res = glob_glob(dirin="folder/",npool=1)
    print(res)

    res =     glob_glob(dirin="folder/test/",npool=1)
    print(res)


    flist = [
        'folder/test/file.txt',
        'folder/test/file1.txt',
        'folder/test/file2.txt',
        'folder/test/file3.txt',
        'folder/test/tmp/1.txt',
        'folder/test/tmp/myfile.txt',
        'folder/test/tmp/record.txt'
    ]

    res = glob_glob(dirin="", file_list=flist)
    print(res)
    assert "folder/test/file.txt" not in res, "Failed, glob_glob"

    res =  glob_glob(file_list=flist)
    print(res)
    assert "folder/test/file.txt" not in res, "Failed, glob_glob"

    res = glob_glob(file_list=flist,exclude="file2.txt,1",include_only="file")
    print(res)
    assert "folder/test/file3.txt"  in res, "Failed, glob_glob"
    assert "folder/test/tmp/myfile.txt"  in res, "Failed, glob_glob"


    res = glob_glob(file_list=flist,exclude="file2.txt,1",include_only="file",npool=1)
    print(res)
    assert "folder/test/file3.txt"  in res, "Failed, glob_glob"
    assert "folder/test/tmp/myfile.txt"  in res, "Failed, glob_glob"


def test_filecache():
    """ python  utilmy/oos.py test_filecache
    """
    import utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()

    fc = fileCache(dir_cache= dirtmp + '/test')
    data = [1,2 ,3, 4]
    fc.set( 'test', data )
    log(fc.get('test'))
    assert fc.get('test') == data, 'FAILED, file cache'


def test_os_module_uncache():
    """ python  utilmy/oos.py test_os_module_uncache
    """
    import  utilmy as uu
    drepo, dirtmp = uu.dir_testinfo()

    import sys
    old_modules = sys.modules.copy()
    exclude_mods = {"json.decoder"}
    excludes_prefixes = {exclude_mod.split('.', 1)[0] for exclude_mod in exclude_mods}
    os_module_uncache(exclude_mods)
    new_modules = sys.modules.copy()
    removed = []
    kept = []
    for module_name in old_modules:
        module_prefix = module_name.split('.', 1)[0]
        if (module_prefix in excludes_prefixes) and (module_name not in exclude_mods):
            assert module_name not in new_modules
            removed.append(module_name)
        else:
            assert module_name in new_modules
            if module_name in exclude_mods:
                kept.append(module_name)
    log("Successfully remove module cache: ", ", ".join(removed))
    log("Successfully kept: ", ", ".join(kept))



def test_os():
    from pytz import timezone
    import sys, os, inspect, requests, json
    import utilmy as uu

    drepo, dirtmp = uu.dir_testinfo()


    old_modules = sys.modules.copy()
    exclude_mods = {"json.decoder"}
    excludes_prefixes = {exclude_mod.split('.', 1)[0] for exclude_mod in exclude_mods}
    os_module_uncache(exclude_mods)
    new_modules = sys.modules.copy()
    removed = []
    kept = []
    for module_name in old_modules:
        module_prefix = module_name.split('.', 1)[0]
        if (module_prefix in excludes_prefixes) and (module_name not in exclude_mods):
            assert module_name not in new_modules
            removed.append(module_name)
        else:
            assert module_name in new_modules
            if module_name in exclude_mods:
                kept.append(module_name)

    log("Successfully remove module cache: ", ", ".join(removed))
    log("Successfully kept: ", ", ".join(kept))

    log("####### os_makedirs() ..")
    os_makedirs('ztmp/ztmp2/myfile.txt')
    os_makedirs('ztmp/ztmp3/ztmp4')
    os_makedirs('/tmp/one/two')
    os_makedirs('/tmp/myfile')
    os_makedirs('/tmp/one/../mydir/')
    os_makedirs('./tmp/test')
    os_makedirs('./tmp','test2/test3')
    os_makedirs('./tmp','test2/test3/test4')

    os_makedirs(Path('./test21/') , Path("test22/test23/"),  Path("test24/test25/"),  "/test12/test13/" )
    os_makedirs('./tmp',Path('test1a/test2'), 'test3/test4')

    # add more weird test cases here
    os_makedirs('/tmp',Path('test10a/test11'), 'test12/test13///')
    os_makedirs('/tmp',Path('test30a/test31'), 'test32/test33///', 'test34/test35')
    os_makedirs('C:/tmp',Path(r'test51a\\test52'), 'test53/') # windows path. should work on linux too


    os.system("ls ztmp")
    os.system("ls ./tmp")

    path = ["/tmp/", "ztmp/ztmp3/ztmp4", "/tmp/myfile", "./tmp/test","/tmp/one/../mydir/", 
            "./tmp/test2/test3/test4",
            "./tmp/test1a/test2/test3/test4",
            "./test21/test22/test23/test24/test25/test12/test13",
            "./tmp/test1a/test2/test3/test4",
            "/tmp/test10a/test11/test12/test13",
            "/tmp/test30a/test31/test32/test33/test34/test35",
            "C:/tmp/test51a/test52/test53"
           ]
    for p in path:
        f = os.path.exists(os.path.abspath(p))
        assert  f == True, "path " + p

    log("####### os_removedirs() ..")
    rev_stat = os_removedirs("ztmp/ztmp2")
    assert not rev_stat == False, "Cannot delete root folder"

    os_removedirs(dirtmp + "/os_test")
    assert ~os.path.exists(dirtmp + "/os_test"), "Folder still found after removing"

    res = os_system( f" ls . ",  doprint=True)
    log(res)
    res = os_system( f" ls . ",  doprint=False)
    log(os_get_os())

    uu.to_file("Dummy text", dirtmp + "/os_file_test.txt")
    os_file_check(dirtmp + "/os_file_test.txt")



    log("#######   os_search_fast() ..")
    uu.to_file("Dummy text to test fast search string", dirtmp + "/os_search_test.txt")
    res = z_os_search_fast(dirtmp + "/os_search_test.txt", ["Dummy"],mode="regex")
    assert  not log(res) and len(res) >0, res

    log("#######   os_search_content() ..")
    dfres = os_search_content(srch_pattern=['Dummy'], dir1=dirtmp, file_pattern="*.txt", mode="str", dirlevel=2)
    assert not log(dfres) and len(dfres) > 0, dfres
    
    #Testing with multiple lines
    line = """
    First dummy text
    Second dummy text
    Third dummy text
    Fourth dummy text"""
    uu.to_file(line, dirtmp + "/os_file_test_multiple_lines.txt")
    dfres = os_search_content(srch_pattern=["Fourth dummy text"], dir1=dirtmp, file_pattern="*multiple_lines.txt", mode="str", dirlevel=2)
    assert not log(dfres) and len(dfres) == 1, dfres

    #Testing with regex mode
    line = """
        message:
        This is a dummy text with a dummy email

        subject: dummy@mail.com
    """
    uu.to_file(line, dirtmp + "/os_file_test_email_regex.txt")
    dfres = os_search_content(srch_pattern=[r'\w+@mail\.\w{2,3}'], dir1=dirtmp, file_pattern="*email_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 1, dfres

    line = """
            this is a url example, www.google.com
            and this is a wrong url example, www.example
    """
    uu.to_file(line, dirtmp + "/os_file_test_url_regex.txt")
    dfres = os_search_content(srch_pattern=[r'www\.[A-z]+\.com'], dir1=dirtmp, file_pattern="*url_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 1, dfres

    line = """
            This is a dummy credit card number: 2222405343248877	
            This is a dummy credit card number with spaces: 2222 4053 4324 8877
            This is a wrong credit card number: 2a22 4053 4324 8877
    """
    uu.to_file(line, dirtmp + "/os_file_test_credit_regex.txt")
    dfres = os_search_content(srch_pattern=[r'\d{4}\s?\d{4}\s?\d{4}\s?\d{4}'], dir1=dirtmp, file_pattern="*credit_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 2, dfres

    line = """
            This is a dummy ip number: 192.168.0.123	
            This is a wrong ip number: 196.1618.0.123
    """
    uu.to_file(line, dirtmp + "/os_file_test_ip_regex.txt")
    dfres = os_search_content(srch_pattern=[r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'], dir1=dirtmp, file_pattern="*ip_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 1, dfres

    line = """
            This is a USA zip number: 35004
            This is a wrong USA zip number 3500s4
            This is a USA zip number with hyphen: 35004-4567
    """
    uu.to_file(line, dirtmp + "/os_file_test_zip_regex.txt")
    dfres = os_search_content(srch_pattern=[r'\d{5}(-\d{4})?'], dir1=dirtmp, file_pattern="*zip_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 2, dfres

    line = """
            This is a dummy social security number: 595-82-4782
            This is a wrong social security number: 595-882-4782
    """
    uu.to_file(line, dirtmp + "/os_file_test_social_security_regex.txt")
    dfres = os_search_content(srch_pattern=[r'\d{3}-\d{2}-\d{4}'], dir1=dirtmp, file_pattern="*social_security_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 1, dfres

    line = """
            This is an amount of dollars: $500
            This is an amount of dollars with decimals: $741.89
            This is an amount of dollars: $476,445.197
            This is a wrong amount of dollars with decimals: 975
    """
    uu.to_file(line, dirtmp + "/os_file_test_us_amount_regex.txt")
    dfres = os_search_content(srch_pattern=[r'\$\d+(?:,\d{3})*(?:.\d{2})?'], dir1=dirtmp, file_pattern="*us_amount_regex.txt", mode="regex", dirlevel=2)
    assert not log(dfres) and len(dfres) == 3, dfres

    #Testing the argument dirlevel
    uu.to_file("dummy text", dirtmp + "folder1/folder2/folder3/folder4/folder5/os_file_test_dirlevel.txt")
    dfres = os_search_content(srch_pattern=["dummy text"], dir1=dirtmp, file_pattern="*dirlevel.txt", mode="str", dirlevel=5)
    assert not log(dfres) and len(dfres) == 1, dfres
    dfres = os_search_content(srch_pattern=["dummy text"], dir1=dirtmp, file_pattern="*dirlevel.txt", mode="str", dirlevel=4)
    assert not log(dfres) and len(dfres) == 0, dfres

    #Testing with json files
    random_dict = {"test":54, "random":"test"}
    jsonString = json.dumps(random_dict)
    uu.to_file(jsonString,dirtmp + "os_file_test_json.json")
    dfres = os_search_content(srch_pattern=[jsonString], dir1=dirtmp, file_pattern="*json.json", mode="str", dirlevel=1)
    assert not log(dfres) and len(dfres) == 1, dfres

    #Testing ignoring file extensions
    uu.to_file("dummy text", dirtmp + "folder_ext/os_file_test_ign_f_ext.txt")
    random_dict = {"test":"dummy text"}
    jsonString = json.dumps(random_dict)
    uu.to_file(random_dict, dirtmp + "folder_ext/os_file_test_ign_f_ext.json")
    dfres = os_search_content(srch_pattern=["dummy text"], dir1=dirtmp + "folder_ext/", ignore_exts=[".json"])
    assert not log(dfres) and len(dfres) == 1, dfres

    #Testing callback parameter
    #callback that removes the file
    def test_callback(file_path):
        dir_path = os.path.dirname(file_path)
        os_remove(dir_path + "/*", ndays_past=0)

    uu.to_file("dummy text", dirtmp + "folder_callback/os_file_callback_test.txt")
    os_search_content(srch_pattern=["dummy text"], dir1=dirtmp + "folder_callback/", callback = test_callback)
    dfres = os_search_content(srch_pattern=["dummy text"], dir1=dirtmp + "folder_callback/")
    assert not log(dfres) and len(dfres) == 0, dfres

    #Testing callback parameter that it only executes itself when the file matchs the srch_pattern
    uu.to_file("test text", dirtmp + "folder_callback/os_file_callback_test.txt")
    os_search_content(srch_pattern=["dummy text"], dir1=dirtmp + "folder_callback/", callback = test_callback)
    dfres = os_search_content(srch_pattern=["test text"], dir1=dirtmp + "folder_callback/")
    assert not log(dfres) and len(dfres) == 1, dfres

    #Testing filtering by the modification time.
    #Changing the modification time of these files for testing
    first_filename = dirtmp + "folder_modification/os_file_first_modification_file.txt"
    second_filename = dirtmp + "folder_modification/os_file_second_modification_file.txt"
    third_filename = dirtmp + "folder_modification/os_file_third_modification_file.txt"
    uu.to_file("dummy text", first_filename)
    uu.to_file("dummy text", second_filename)
    uu.to_file("dummy text", third_filename)
    stat = os.stat(second_filename)
    first_mtime = datetime.datetime(2023, 3, 28)
    os.utime(second_filename, times=(stat.st_atime, first_mtime.timestamp()))    
    stat = os.stat(third_filename)
    second_mtime = datetime.datetime(2023, 3, 29)
    os.utime(third_filename, times=(stat.st_atime, second_mtime.timestamp()))
    #Testing to search the second filename by its new modification time
    dfres = os_search_content(srch_pattern=["dummy text"], dir1=dirtmp + "folder_modification/",start_time = first_mtime.date(), end_time = first_mtime.date())
    assert not log(dfres) and len(dfres) == 1, dfres


    log("###### os_walk() ..")
    folders = os_walk(path=dirtmp, pattern="*.txt")
    assert len(folders["file"]) > 0, "Pattern with wildcard doesn't work"

    log("#######   os_copy_safe() ..")
    uu.to_file("Dummy text", drepo + "/testdata/tmp/test/os_copy_safe_test.txt")
    os_copy_safe(dirin=drepo + "testdata/tmp/test", dirout=drepo + "testdata/tmp/test_copy_safe/", nlevel=1, pattern="*.txt")
    log(drepo + "testdata/tmp/test_copy_safe/os_copy_safe_test.txt")
    f = os.path.exists(os.path.abspath(drepo + "/testdata/tmp/test_copy_safe/os_copy_safe_test.txt"))
    assert  f == True, "The file os_copy_safe_test.txt doesn't exist"

    log("####### os_copy() ..")
    uu.to_file("Dummy text", drepo + "/testdata/tmp/test/os_copy_test.txt")
    os_copy(
        dirfrom=drepo + "testdata/tmp/test",
        dirto=drepo + "testdata/tmp/test_copy",
        mode="dir")
    f = os.path.exists(os.path.abspath(drepo + "testdata/tmp/test_copy/os_copy_test.txt"))
    assert  f == True, "The file os_copy_test.txt doesn't exist"


    cwd = os.getcwd()
    #log(os_walk(cwd))
    cmd = ["pwd","whoami"]
    os_system_list(cmd, sleep_sec=0)


    log("#######   os_variables_test ..")
    ll = ["test_var"]
    globs = {}
    os_variable_init(ll, globs)
    os_variable_exist("test_var", globs)
    os_variable_check("other_var", globs,do_terminate=False)
    os_import(mod_name="pandas", globs=globs)
    os_variable_del(["test_var"], globs)
    log(os_variable_exist("test_var", globs))
    assert os.path.exists(dirtmp + "/"),"Directory doesn't exist"


    log("#######   os utils...")
    log("#######   os_get_os()..")
    log(os_get_os())
    platform = sys.platform.lower()
    if platform == 'win32':
        platform = 'windows'
    assert os_get_os().lower() == platform, "Platform mismatch"

    log("#######   os_cpu_info()..")
    log(os_cpu_info())

    log("#######   os_ram_info()..")
    log(os_ram_info())

    log("#######   os_getcwd()..")
    log(os_getcwd())
    os_sleep_cpu(cpu_min=30, sleep=1, interval=5, verbose=True)

    log("#######   os_ram_sizeof()..")
    c = {1, 3, "sdsfsdf"}
    log(os_ram_sizeof(c, set()))


    log("#######   os_path_size() ..")
    size_ = os_path_size(drepo)
    assert not log("total size", size_) and size_> 10 , f"error {size_}"


    log("#######   os_path_split() ..")
    result_ = os_path_split(dirtmp + "/test.txt")
    log("result", result_)

    # TODO: Add test to this function here
    log("#######   os_file_replacestring() ..")



    cwd = os.getcwd()
    '''TODO: for f in list_all["fullpath"]:
        KeyError: 'fullpath'
    res = os_search_content(srch_pattern= "Dummy text",dir1=os.path.join(cwd ,"tmp/test/"))
    log(res)
    '''

    log("#######   os_system_list() ..")
    cmd = ["pwd","whoami"]
    os_system_list(cmd, sleep_sec=0)
    os_system("whoami", doprint=True)


    log("#######   os_file_check()")
    uu.to_file("test text to write to file", dirtmp + "/file_test.txt", mode="a")
    os_file_check(dirtmp + "/file_test.txt")


    log("#######   os_file_replacestring...")
    uu.to_file("Dummy file to test os utils", dirtmp+"/os_utils_test.txt")
    uu.to_file("Dummy text to test replace string", dirtmp+"/os_test/os_file_test.txt")
    print("dtmp:",dirtmp + "/os_test/")
    os_file_replacestring("text", "text_replace", dirtmp + "/os_test/")


    log("#######   os_ram_sizeof()...")
    log(os_ram_sizeof(["3434343", 343242, {3434, 343}], set()))


    log("\n#######", os_merge_safe)
    uu.to_file("""test input1""", dirtmp + "test1.txt" )
    uu.to_file("""test input2""", dirtmp + "test2.txt" )

    os_merge_safe(dirin_list=[dirtmp+'./*.txt'], dirout=dirtmp+"merge.txt")
    os_remove(dirin=dirtmp+'test1.txt', ndays_past=-1)
    log(os_file_date_modified(dirin=dirtmp+'merge.txt'))

    flist = glob_glob(dirtmp)
    assert len(flist) < 2, flist



    log("#######   os_remove()")
    obj_dir = dirtmp+"/xtest*.txt"
    total_files = []
    for name in ("xtest1", "xtest2", "xtest3"):
        with open(dirtmp+"/{}.txt".format(name), "w") as f:
            f.write(name)
            total_files.append(f.name)

    # test dry remove
    before_files = glob.glob(obj_dir, recursive=True)
    os_remove(dirin=obj_dir,
              min_size_mb=0, max_size_mb=1,
              exclude="", include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=99999999,
              dry=1)
    cur_files = glob.glob(obj_dir, recursive=True)
    assert before_files == cur_files

    # test exclude
    excludes = [dirtmp+"xtest1.txt", dirtmp+"xtest2.txt"]
    print(excludes)
    os_remove(dirin=obj_dir,
              min_size_mb=0, max_size_mb=1,
              exclude=','.join(excludes), include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=99999999,
              dry=0)
    cur_files = glob.glob(obj_dir, recursive=True)
    for file in total_files:
        if file in excludes:
            assert file in cur_files
        else:
            assert file not in cur_files

    # test file num limit
    before_files = glob.glob(obj_dir, recursive=True)
    os_remove(dirin=obj_dir,
              min_size_mb=0, max_size_mb=1,
              exclude="", include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=1,
              dry=0)
    cur_files = glob.glob(obj_dir, recursive=True)
    assert len(before_files) - len(cur_files) == 1

    # test file size
    before_files = glob.glob(obj_dir, recursive=True)
    os_remove(dirin=obj_dir,
              min_size_mb=1, max_size_mb=2,
              exclude="", include_only="",
              ndays_past=0, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=1,
              dry=0)
    cur_files = glob.glob(obj_dir, recursive=True)
    assert len(before_files) == len(cur_files)


    timezone_name = 'Asia/Tokyo'
    datetime_format = '%Y%m%d-%H:%M'
    file_dir = dirtmp + "/test.txt"


    log("\n#######", os_file_date_modified)
    uu.to_file("first line", file_dir)
    created_time = datetime.datetime.now(timezone(timezone_name)).strftime(datetime_format)
    last_modified_created = os_file_date_modified(file_dir, datetime_format, timezone_name)

    log(created_time, last_modified_created)
    assert created_time == last_modified_created


    log("\n#######", os_get_ip)
    public_ip = get_public_ip()
    log("Public IP", public_ip)
    log("Internal IP", os_get_ip())

    uu.to_file("first line", file_dir)

    log("\n#######", os_file_info)
    test_file_size = os.stat(file_dir).st_size / (1024 * 1024)
    test_file_modification_time = os.stat(file_dir).st_mtime
    log("File Directory:", file_dir)
    log("File Size in MB:", test_file_size)
    log("File Modification time:", test_file_modification_time)

    
    file_stats = os_file_info(file_dir)
    assert file_dir == file_stats[0][0]
    assert test_file_size == file_stats[0][1]
    assert test_file_modification_time == file_stats[0][2]


    log("\n#######", os_file_info)
    _, file__name__, _, function_name = os_get_function_name().split(',')

    log("File __name__ value:", __name__)
    log("Function name:", inspect.stack()[0][3])
    assert file__name__ == __name__
    assert function_name == inspect.stack()[0][3]




########################################################################################################
###### File parsing functions ###########################################################################
def glob_glob(dirin="", file_list=[], exclude="", include_only="",
            min_size_mb=0, max_size_mb=500000,
            ndays_past=-1, nmin_past=-1,  start_date='1970-01-02', end_date='2050-01-01',
            nfiles=99999999, verbose=0, npool=1
    ):
    """ Advanced glob.glob filtering.
    Docs::

        dirin:str = "": get the files in path dirin, works when file_list=[]
        file_list: list = []: if file_list works, dirin will not work
        exclude:str  = ""
        include_only:str = ""
        min_size_mb:int = 0
        max_size_mb:int = 500000
        ndays_past:int = 3000
        start_date:str = '1970-01-01'
        end_date:str = '2050-01-01'
        nfiles:int = 99999999
        verbose:int = 0
        npool:int = 1: multithread not working
        
        https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio
    """
    import glob, copy, datetime as dt, time


    def fun_glob(dirin=dirin, file_list=file_list, exclude=exclude, include_only=include_only,
            min_size_mb=min_size_mb, max_size_mb=max_size_mb,
            ndays_past=ndays_past, nmin_past=nmin_past,  start_date=start_date, end_date=end_date,
            nfiles=nfiles, verbose=verbose,npool=npool):
        """
        Docs::
            dirin:str = "": get the files in path dirin, works when file_list=[]
            file_list: list = []: if file_list works, dirin will not work
            exclude:str  = ""
            include_only:str = ""
            min_size_mb:int = 0
            max_size_mb:int = 500000
            ndays_past:int = 3000
            start_date:str = '1970-01-01'
            end_date:str = '2050-01-01'
            nfiles:int = 99999999
            verbose:int = 0
            npool:int = 1: multithread not working
        """
        if dirin and not file_list:
            files = glob.glob(dirin, recursive=True)
            files = sorted(files)

        if file_list:
            files = file_list

        ####### Exclude/Include  ##################################################
        for xi in exclude.split(","):
            if len(xi) > 0:
                files = [  fi for fi in files if xi not in fi ]

        if include_only:
            tmp_list = [] # add multi files
            for xi in include_only.split(","):
                if len(xi) > 0:
                    tmp_list += [  fi for fi in files if xi in fi ]
            files = sorted(set(tmp_list))

        ####### size filtering  ##################################################
        if min_size_mb != 0 or max_size_mb != 0:
            flist2=[]
            for fi in files[:nfiles]:
                try :
                    if min_size_mb <= os.path.getsize(fi)/1024/1024 <= max_size_mb :   #set file size in Mb
                        flist2.append(fi)
                except : pass
            files = copy.deepcopy(flist2)

        #######  date filtering  ##################################################
        now    = time.time()
        cutoff = 0

        if ndays_past > -1 :
            cutoff = now - ( abs(ndays_past) * 86400)

        if nmin_past > -1 :
            cutoff = cutoff - ( abs(nmin_past) * 60  )

        if cutoff > 0:
            if verbose > 0 :
                print('now',  dt.datetime.utcfromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S"),
                       ',past', dt.datetime.utcfromtimestamp(cutoff).strftime("%Y-%m-%d %H:%M:%S") )
            flist2=[]
            for fi in files[:nfiles]:
                try :
                    t = os.stat( fi)
                    c = t.st_ctime
                    if c < cutoff:             # delete file if older than 10 days
                        flist2.append(fi)
                except : pass
            files = copy.deepcopy(flist2)

        ####### filter files between start_date and end_date  ####################
        if start_date and end_date:
            start_timestamp = time.mktime(time.strptime(str(start_date), "%Y-%m-%d"))
            end_timestamp   = time.mktime(time.strptime(str(end_date), "%Y-%m-%d"))
            flist2=[]
            for fi in files[:nfiles]:
                try:
                    t = os.stat( fi)
                    c = t.st_mtime
                    if start_timestamp <= c <= end_timestamp:
                        flist2.append(fi)
                except: pass
            files = copy.deepcopy(flist2)

        return files

    if npool ==  1:
        return fun_glob(dirin, file_list, exclude, include_only,
            min_size_mb, max_size_mb,
            ndays_past, nmin_past,  start_date, end_date,
            nfiles, verbose,npool)

    else :
        raise Exception('no working with npool>1')
        # from utilmy import parallel as par
        # input_fixed = {'exclude': exclude, 'include_only': include_only,
        #                'npool':1,
        #               }
        # if dirin and not file_list:
        #     fdir = [item for item in os.walk(dirin)] # os.walk(dirin, topdown=False)
        # if file_list:
        #     fdir = file_list
        # res  = par.multithread_run(fun_glob, input_list=fdir, input_fixed= input_fixed,
        #         npool=npool)
        # res  = sum(res) ### merge
        # return res



def os_remove(dirin="folder/**/*.parquet",
              min_size_mb=0, max_size_mb=0,
              exclude="", include_only="",
              ndays_past=-1, start_date='1970-01-02', end_date='2050-01-01',
              nfiles=99999999,
              dry=False):

    """  Delete files with criteria, using glob_glob
    Docs::

        Args:
            dirin (str)        : Path with wildcards to match folder name. (Default to "folder/**/*.parquet".)
            min_size_mb (int)  : Min size of the files. (Default to 0.)
            max_size_mb (int)  : Max size of the files. (Default to 1.)
            exclude (str)      : Paths separated by commas to exclude. (Default to "".)
            include_only (str) : Paths to only include. (Default to "".)
            ndays_past (int)   : Number of days past that the file must be old. (Defaults to -1.)
            start_date (str)   : Start date of the file creation, format "YYYY-MM-DD". (Default to '1970-01-02'.)
            end_date (str)     : End date of the file creation, format "YYYY-MM-DD". (Default to '2050-01-01'.)
            nfiles (int)       : Max number of files to remove. (Default to 99999999.)
            dry (Bool)         : Flag to test. (Default to 0.)
        Example:
            from utilmy import oos
            path = "/home/user/Desktop/example/*"
            oos.os_remove(path, ndays_past=0)
            #All the files in "example" are deleted
    """
    import os
    # import sys, time, glob, datetime as dt # unused imports

    dry = True if dry in {True, 1} else False

    flist2 = glob_glob(dirin, exclude=exclude, include_only=include_only,
            min_size_mb= min_size_mb, max_size_mb= max_size_mb,
            ndays_past=ndays_past, start_date=start_date, end_date=end_date,
            nfiles=nfiles,)


    print ('Nfiles', len(flist2))
    jj = 0
    for fi in flist2 :
        try :
            if not dry :
                os.remove(fi)
                jj = jj +1
            else :
                print(fi)
        except Exception as e :
            print(fi, e)

    if dry :  print('dry mode only')
    else :    print('deleted', jj)



def glob_glob_list(dirin="", file_list=None, exclude="", include_only="",
            min_size_mb=0, max_size_mb=500000,
            ndays_past=-1, nmin_past=-1,  start_date='1970-01-02', end_date='2050-01-01',
            nfiles=99999999, verbose=0, npool=1
    ):
    """ Advanced glob.glob filtering.
    Docs::

        dirin:str = "": get the files in path dirin, works when file_list=[]
        file_list: list = []: file_list of [filename, date, size] OR [filename, date]
        exclude:str       = ""
        include_only:str  = ""
        min_size_mb:int   = 0
        max_size_mb:int   = 500000
        ndays_past:int    = 3000
        start_date:str    = '1970-01-01'
        end_date:str      = '2050-01-01'
        nfiles:int        = 99999999
        verbose:int       = 0
        npool:int         = 1: multithread not working
        
        https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio
    """
    import copy, datetime as dt, time
    import fnmatch

    if len(file_list) < 1 : return []

    dtlist   = None
    sizelist = None
    if isinstance(file_list[0] , list ) :
        m = len(file_list[0])
        flist    = []

        files = [ fi for fi in file_list if fnmatch.fnmatch(fi[0], dirin) ]

        if m ==1 :
            flist    = [ fi[0] for fi in files ]

        if m ==2 :
            flist    = [ fi[0] for fi in files ]
            dtlist   = [ fi[1] for fi in files ] #### Datetime

        if m ==3 :
            flist    = [ fi[0] for fi in files ]
            dtlist   = [ fi[1] for fi in files ]
            sizelist = [ fi[2] for fi in files ] ### size in bytes

    else :
        files = [ fi for fi in file_list if fnmatch.fnmatch(fi, dirin) ]
        files = sorted(files)
        

    ####### Exclude/Include  ##################################################
    for xi in exclude.split(","):
        if len(xi) > 0:
            files = [  fi for fi in files if xi not in fi ]

    if include_only:
        tmp_list = [] # add multi files
        for xi in include_only.split(","):
            if len(xi) > 0:
                tmp_list += [  fi for fi in files if xi in fi ]
        files = sorted(set(tmp_list))

    ####### size filtering  ##################################################
    if min_size_mb != 0 or max_size_mb != 0 and sizelist is not None :
        flist2=[]
        for ii,fi in enumerate(files[:nfiles]):
            try :
                if min_size_mb <= sizelist[ii] <= max_size_mb :   #set file size in Mb
                    flist2.append(fi)
            except : pass
        files = copy.deepcopy(flist2)

    #######  date filtering  ##################################################
    now    = time.time()
    cutoff = 0

    if ndays_past > -1 :
        cutoff = now - ( abs(ndays_past) * 86400)

    if nmin_past > -1 :
        cutoff = cutoff - ( abs(nmin_past) * 60  )

    if cutoff > 0 and dtlist is not None:
        if verbose > 0 :
            print('now',   dt.datetime.utcfromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S"),
                  ',past', dt.datetime.utcfromtimestamp(cutoff).strftime("%Y-%m-%d %H:%M:%S") )
        flist2=[]
        for ii, fi in enumerate(files[:nfiles]):
            try :
                c = dtlist[ii]
                if c < cutoff:             # delete file if older than 10 days
                    flist2.append(fi)
            except : pass
        files = copy.deepcopy(flist2)

    ####### filter files between start_date and end_date  ####################
    if start_date and end_date and dtlist:
        start_timestamp = time.mktime(time.strptime(str(start_date), "%Y-%m-%d"))
        end_timestamp   = time.mktime(time.strptime(str(end_date), "%Y-%m-%d"))
        flist2=[]
        for fi in files[:nfiles]:
            try:
                c = dtlist[ii]
                if start_timestamp <= c <= end_timestamp:
                    flist2.append(fi)
            except: pass
        files = copy.deepcopy(flist2)

    return files




########################################################################################################
###### Code running  ###################################################################################
def os_system(cmd, doprint=False):
    """ Get stdout, stderr from Command Line into  a string varables  mout, merr
    Docs::     
        Args:
            cmd: Command to run subprocess
            doprint=False: int
        Returns:
            out_txt, err_txt
    """
    import subprocess
    try :
        p          = subprocess.run( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, )
        mout, merr = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')
        if doprint:
            l = mout  if len(merr) < 1 else mout + "\n\nbash_error:\n" + merr
            print(l)

        return mout, merr
    except Exception as e :
        print( f"Error {cmd}, {e}")


def os_subprocess_decode(proc, is_binary=False, return_stream=False):
    """

    """
    # If we need a stream
    if return_stream: return proc.stdout


    # If we need to return the data only
    file_data = ""
    if not is_binary:
        for this_line in iter(proc.stdout.readline, b''):

            # Poll for return code
            proc.poll()
            # If return code exists exit from loop
            if proc.returncode is not None:
                break

            # Decode the binary stream
            this_line_decoded = this_line.decode("utf8")
            if this_line_decoded:
                # In case you want to have stdout as well
                # If removed there will be no indication that we are still receiving the data
                log(this_line_decoded)
                file_data = file_data + "\n" + this_line_decoded
    else:
        for this_bit in iter(proc.stdout.read, b''):
            file_data = bytes()
            log(this_bit, sep="", end="")
            file_data = file_data + this_bit

    # If the process returncode is None and we reach here, start polling for returncode until it exists
    while proc.returncode is None:
        proc.poll()

    # raise exception if error occurred, else return file_data
    if proc.returncode != 0 and proc.returncode is not None:
        _, err = proc.communicate()
        raise Exception(f"Error occurred with exit code {proc.returncode}\n{str(err.decode('utf8'))}")
    elif proc.returncode == 0:
        return file_data



#####################################################################################################
##### File I-O ######################################################################################
class fileCache(object):
    def __init__(self, dir_cache=None, ttl=None, size_limit=10000000, verbose=1):
        """ Simple cache system to store path --> list of files
            for S3 or HDFS
            Docs::
                Args:
                    dir_cache=None
                    ttl=None
                    size_limit=10000000 (int)
                    verbose=1 (int)
        """
        import tempfile, diskcache as dc

        dir_cache = tempfile.tempdir() if dir_cache is None else dir_cache
        dir_cache= dir_cache.replace("\\","/")
        dir_cache= dir_cache + "/filecache.db"
        self.dir_cache = dir_cache
        self.verbose = verbose
        self.size_limit = size_limit
        self.ttl = ttl if ttl is not None else 10

        cache = dc.Cache(dir_cache, size_limit= self.size_limit, timeout= self.ttl )
        if self.verbose:
            print('Cache size/limit', len(cache), self.size_limit )
        self.db = cache


    def get(self, path):
        """ method get
         Docs::
            Args:
                path: str
            Returns:
                self.db.get(path, None)
         """
        path = path.replace("\\","/")
        return self.db.get(path, None)


    def set(self, path:str, flist:list, ttl=None):
        """
        Docs::
            Args:
                path:str
                flist:list
                ttl=None
                expire (float) - seconds until item expires (default None, no expiry)
            Returns:
                None
        """
        ttl = ttl if isinstance(ttl, int)  else self.ttl
        path = path.replace("\\","/")
        self.db.set(path, flist, expire=float(ttl), retry=True)



def os_copy(dirfrom="folder/**/*.parquet", dirto="",

            mode='file',

            exclude="", include_only="",
            min_size_mb=0, max_size_mb=500000,
            ndays_past=-1, nmin_past=-1,  start_date='1970-01-02', end_date='2050-01-01',
            nfiles=99999999, verbose=0,

            dry=0
            ) :
    """  Advance copy with filter.
    Docs::
          mode:str = 'file'  :   file by file, very safe (can be very slow, not nulti thread)
          https://stackoverflow.com/questions/123198/how-to-copy-files
          exclude:str = ""
          include_only:str = ""
          min_size_mb:int = 0
          max_size_mb:int = 500000
          ndays_past:int = -1
          nmin_past:int = -1
          start_date:str = '1970-01-02'
          end_date:str = '2050-01-01'
          nfiles:int = 99999999
          verbose:int = 0
          dry:int = 0
    """
    # import os # unused imports
    import shutil

    dry   = True if dry ==True or dry==1 else False
    flist = glob_glob(dirfrom, exclude=exclude, include_only=include_only,
            min_size_mb= min_size_mb, max_size_mb= max_size_mb,
            ndays_past=ndays_past, nmin_past=nmin_past, start_date=start_date, end_date=end_date,
            nfiles=nfiles,)

    if mode =='file':
        print('Nfiles', len(flist))
        jj = 0
        for fi in flist :
            try :
                if not dry :
                    shutil.copy(fi, dirto)
                    jj = jj +1
                else :
                    print(fi)
            except Exception as e :
                print(fi, e)


        if dry :  print('dry mode only')
        else :    print('deleted', jj)

    elif mode =='dir':
        try:
            shutil.copytree(dirfrom, dirto, symlinks=False, ignore=None, ignore_dangling_symlinks=False)
        except FileExistsError as e:
            print('Directory is already exists')
        except Exception as e:
            print(e)



def os_copy_safe(dirin:str=None, dirout:str=None,  nlevel=5, nfile=5000, logdir="./", pattern="*", exclude="", force=False, sleep=0.5, cmd_fallback="",
                 verbose=True):  ###
    """ Copy safe, using callback command to re-connect network if broken
    Docs::
        Args:
            dirin:str = None
            dirout:str = None
            nlevel:int = 5
            nfile:int = 5000
            logdir:str = "./"
            pattern:str = "*"
            exclude:str = ""
            force:bool = False
            sleep:float = 0.5
            cmd_fallback:str =""
            verbose:bool = True
        Return:
            None
    """
    import shutil, time, os, glob

    flist = [] ; dirinj = dirin
    for j in range(nlevel):
        ztmp   = glob.glob(dirinj + "/" + pattern)
        dirinj = dirinj + "/*/"
        if len(ztmp) < 1: break
        flist.extend(ztmp)

    flist2 = []
    for x in exclude.split(","):
        if len(x) <= 1: continue
        for t in flist:
            if  not x in t:
                flist2.append(t)
    flist = [x for x in flist if x not in flist2]

    log('n files', len(flist), dirinj, dirout); time.sleep(sleep)
    kk = 0; ntry = 0; i = 0
    for i in range(0, len(flist)):
        fi  = flist[i]
        fi2 = fi.replace(dirin, dirout)

        try:
            if not fi.isascii(): continue
        except AttributeError:
            pass

        if not os.path.isfile(fi): continue

        if (not os.path.isfile(fi2)) or force:
            kk = kk + 1
            if kk > nfile: return 1
            if kk % 50 == 0 and sleep > 0: time.sleep(sleep)
            if kk % 10 == 0 and verbose: log(fi2)
            os.makedirs(os.path.dirname(fi2), exist_ok=True)
            try:
                shutil.copy(fi, fi2)
                ntry = 0
                if verbose: log(fi2)
            except Exception as e:
                log(e)
                time.sleep(10)
                log(cmd_fallback)
                os.system(cmd_fallback)
                time.sleep(10)
                i = i - 1
                ntry = ntry + 1
    log('Scanned', i, 'transfered', kk)

### Alias
#os_copy = os_copy_safe


def os_merge_safe(dirin_list=None, dirout=None, nlevel=5, nfile=5000, nrows=10**8,
                  cmd_fallback = "umount /mydrive/  && mount /mydrive/  ", sleep=0.3):
    """function os_merge_safe
    Docs::
        Args:
            dirin_list:None
            dirout:None
            nlevel:int = 5
            nfile:int = 5000
            nrows:int = 10**8
            cmd_fallback:str = "umount /mydrive/  && mount /mydrive/  "
            sleep:float = 0.3
        Returns:
            None
    """
    ### merge file in safe way
    nrows = 10**8
    flist = []
    for fi in dirin_list :
        flist = flist + glob.glob(fi)
    log(flist); time.sleep(2)

    os_makedirs(dirout)
    fout = open(dirout,'a')
    for fi in flist :
        log(fi)
        ii   = 0
        fin  = open(fi,'r')
        while True:
            try :
                ii = ii + 1
                if ii % 100000 == 0 : time.sleep(sleep)
                if ii > nrows : break
                x = fin.readline()
                if not x: break
                fout.write(x.strip()+"\n")
            except Exception as e:
                log(e)
                os.system(cmd_fallback)
                time.sleep(10)
                fout.write(x.strip()+"\n")
        fin.close()


def os_removedirs(path, verbose=False):
    """  issues with no empty Folder
    # Delete everything reachable from the directory named in 'top',
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it could delete all your disk files.
    Docs::
        Args:
            path: Path to walk and create directory
            verbose=False
        Returns:
            True | False
    """
    if len(path) < 3 :
        print("cannot delete root folder")
        return False

    import os
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            try :
                os.remove(os.path.join(root, name))
                if verbose: log(name)
            except Exception as e :
                log('error', name, e)

        for name in dirs:
            try :
                os.rmdir(os.path.join(root, name))
                if verbose: log(name)
            except  Exception as e:
                log('error', name, e)

    try :
        os.rmdir(path)
    except: pass
    return True


def unix_path(path:str):
    """function unix_path
    Docs::
        Args:
            path:str
        Returns:
            path
    """
    path = path.replace("\\", "/")
    path = re.sub(r"//+", "/", path)
    return path



# def os_makedirs(dir_or_file:Union[str, Path]):
#     """function os_makedirs
#     Docs::
#         Args:
#             dir_or_file:
#         Returns:
#             None
#     """
#     dir_or_file = unix_path(dir_or_file) ## windows case
#     if os.path.isfile(dir_or_file) or "." in dir_or_file.split("/")[-1] :
#         os.makedirs(os.path.dirname(os.path.abspath(dir_or_file)), exist_ok=True)
#         #f = open(dir_or_file,'w')
#         #f.close()
#     else :
#         os.makedirs(os.path.abspath(dir_or_file), exist_ok=True)



def os_makedirs(*dir_or_file:Union[str, Path]):
    """function os_makedirs
    Docs::
        Args:
            dir_or_file:
        Returns:
            None
    """
    direc = dir_or_file[0]
    if isinstance(direc, Path):
        direc = str(direc.absolute())

    for dir in dir_or_file[1:]:
        if isinstance(dir, Path):
            dir = str(dir)
        direc = direc + "/" + dir

    _dir_or_file = unix_path(direc) ## will replace all double // and for windows case \\ -> /
    if os.path.isfile(_dir_or_file) or "." in _dir_or_file.split("/")[-1] :
        os.makedirs(os.path.dirname(os.path.abspath(_dir_or_file)), exist_ok=True)
        #f = open(dir_or_file,'w')
        #f.close()
    else :
        os.makedirs(os.path.abspath(_dir_or_file), exist_ok=True)


def os_getcwd():
    """  os.getcwd() This is for Windows Path normalized As Linux path /
        Docs::
            Args:
                None
            Returns:
                root: an absolute pathname of the current working directory
    """
    # root = os.path.abspath(os.getcwd()).replace("\\", "/") + "/"
    root = unix_path(os.path.abspath(os.getcwd()) + "/") # make sure it is one / at the end
    return  root


def os_system_list(ll, logfile=None, sleep_sec=10):
    """function os_system_list
    Docs::
        Args:
            ll:
            logfile:None = None
            sleep_sec:int = 10
        Returns:
            None
    """
    ### Execute a sequence of cmd
    import time, sys
    n = len(ll)
    for ii,x in enumerate(ll):
        try :
            log(x)
            if sys.platform == 'win32' :
                cmd = f" {x}   "
            else :
                cmd = f" {x}   2>&1 | tee -a  {logfile} " if logfile is not None else  x

            os.system(cmd)

            # tx= sum( [  ll[j][0] for j in range(ii,n)  ]  )
            # log(ii, n, x,  "remaining time", tx / 3600.0 )
            #log('Sleeping  ', x[0])
            time.sleep(sleep_sec)
        except Exception as e:
            log(e)


def os_process_list():
    """  List of processes
    #ll = os_process_list()
    #ll = [t for t in ll if 'root' in t and 'python ' in t ]
    ### root   ....  python run
    Docs::
        Args:
            None
        Returns:
            ll
    """
    import subprocess
    ps = subprocess.Popen('ps -ef', shell=True, stdout=subprocess.PIPE)
    ll = ps.stdout.readlines()
    ll = [ t.decode().replace("\n", "") for t in ll ]
    return ll



def os_scandir(path, yield_dir=False, walk=False):
	"""
	Iterate through a directory
    and `yield` the filePath object of each Files and Folders*.

    Docs::
        Args:
            path: path to the directory
            yield_dir (bool): if True yields directories too (default: False)
            walk (bool): if True, will walk over the subdirectories with os.scandir() (default: False)
        Yields:
            filePath object of each Files and Folders

	"""

	Q = Queue()
	Q.put(path)
	while not Q.empty():
		path = Q.get()

		try:
			dir = os.scandir(path)
		except OSError:
			continue
		for entry in dir:
			try:
				is_dir = entry.is_dir(follow_symlinks=False)
			except OSError as error:
				continue
			if is_dir and walk:
				Q.put(entry.path)
			
			if yield_dir or not is_dir:
				yield entry

		dir.close()



# def os_path_size(path = '.'):
#     """function os_path_size
#     Docs::
#         Args:
#             path:str = "."
#         Returns:
#             total_size
#     """
#     total_size = 0
#     for dirpath, dirnames, filenames in os.walk(path):
#         for f in filenames:
#             fp = os.path.join(dirpath, f)
#             # skip if it is symbolic link
#             if not os.path.islink(fp):
#                 total_size += os.path.getsize(fp)

#     return total_size



def os_path_size(path = '.'):
	"""
	returns the size of a directory and its subdirectories.
    
    function os_path_size
        Docs::
            Args:
                path:str = "."
            Returns:
                total_size
	"""
	total = 0

    # why use os_scandir() instead of os.walk()?
    # os.scandir() is faster than os.walk(), it also caches the data. walk_dir() uses it.
	for entry in os_scandir(path, walk=True):
		try:
			total += entry.stat(follow_symlinks=False).st_size
		except OSError:
			continue
	return total


def os_path_split(fpath:str=""):
    """function os_path_split
    Args:
        fpath ( str ) :
    Returns:
        parent, fname, ext
    """
    #### Get path split
    fpath = unix_path(fpath)
    if fpath[-1] == "/":
        fpath = fpath[:-1]

    parent = "/".join(fpath.split("/")[:-1])
    fname  = fpath.split("/")[-1]
    if "." in fname :
        ext = ".".join(fname.split(".")[1:])
    else :
        ext = ""

    return parent, fname, ext



def os_file_replacestring(findstr, replacestr, some_dir, pattern="*.*", dirlevel=1):
    """  replace string into sub-files
    Docs::
        Args:
            findstr="logo.png" (str)
            replacestr="logonew.png" (str)
            some_dir=r"D:/__Alpaca__details/aiportfolio" (str)
            pattern="*.html" (str)
            dirlevel=5 (int)
        Returns:
            None
    """
    def os_file_replacestring1(find_str, rep_str, file_path):
        """replaces all find_str by rep_str in file file_path
        Docs::
            Args:
                find_str:str - finds string
                rep_str:str - replaces string
                file_path:str - file to replace string
            Returns:
                None
        """
        import fileinput

        file1 = fileinput.FileInput(file_path, inplace=True, backup=".bak")
        for line in file1:
            line = line.replace(find_str, rep_str)
            sys.stdout.write(line)
        file1.close()
        print(("OK: " + format(file_path)))


    list_file = os_walk(some_dir, pattern=pattern, dirlevel=dirlevel)
    list_file = list_file['file']
    for file1 in list_file:
        os_file_replacestring1(findstr, replacestr, file1)




def os_file_date_modified(dirin, fmt="%Y%m%d-%H:%M", timezone='Asia/Tokyo'):
    """last modified date
    Docs::
        Args:
            dirin:str -The time of last modification of the specified path
            fmt:str="%Y%m%d-%H:%M" -Time format
            timezone:str='Asia/Tokyo' -Timezone
        Returns:
            mtime2.strftime(fmt) | ""
    """
    import datetime
    from pytz import timezone as tzone, utc
    try:

        mtime  = os.path.getmtime(dirin)
        mtime2 = datetime.datetime.utcfromtimestamp(mtime)
        mtime2 = mtime2.replace(tzinfo=utc)
        mtime2 = mtime2.astimezone(tzone(timezone))
        
        return mtime2.strftime(fmt)
    except:
        return ""


def os_file_check(fpath:str):
    """Check file stat info
    Docs::
        Args:
            fpath: str - File patj
        Returns:
            flag: True | False
    """
    import os, time

    flist = glob_glob(fpath)
    flag = True
    for fi in flist :
        try :
            log(fi,  os.stat(fi).st_size*0.001, time.ctime(os.path.getmtime(fi)) )
        except :
            log(fi, "Error File Not exist")
            flag = False
    return flag


# TODO
def os_file_info(dirin, returnval='list', date_format='unix'):
    """ Return file info:   filenmae, Size in mb,  Unix time (Epoch time, Posix time)
    Docs::
        Args:
            dirin
            returnval='list'
            date_format='unix'
        Returns:
            flist2
    """
    flist = glob_glob(dirin)
    flist2 =[]
    mbyte  =1 /(1024*1024)
    for fi in flist :
        try :
            st = os.stat(fi)

            ####  Size in mb,  Unix time (Epoch time, Posix time)
            res =[ fi, st.st_size * mbyte  , st.st_mtime ]
            flist2.append(res )

        except Exception as e :
            log(fi, e)

    return flist2



def os_walk(path, pattern="*", dirlevel=50):
    """  Get files from  sub-folder, same than glob_glob
    Docs::

        Args:
            path (str)    : Directory path.
            pattern (str) : Pattern with wildcards like those used in Unix shells. (Defaults to "*".)
            dirlevel (int): Max Level of sub-directories, (0=root dir, 1= one path below, etc.). (Defaults to 50.)
            Returns:
                Returns dict of  ['file' , 'dir'].
            Example:
                from utilmy import oos
                path = "/tmp/example"
                sub_folders = oos.os_walk(path=path)
                print("Subfolders:", sub_folders)
    """
    import fnmatch, os, numpy as np

    matches = {'file':[], 'dir':[]}
    dir1    = unix_path(path).rstrip("/")
    num_sep = dir1.count("/")

    for root, dirs, files in os.walk(dir1):
        root = unix_path(root)
        for fi in files :
            if root.count("/") > num_sep + dirlevel: continue
            matches['file'].append(unix_path(os.path.join(root, fi)))

        for di in dirs :
            if root.count("/") > num_sep + dirlevel: continue
            matches['dir'].append(unix_path(os.path.join(root, di) + "/"))

    ### Filter files
    matches['file'] = [ t for t in fnmatch.filter(matches['file'], pattern) ]
    return  matches




#######################################################################################################
##### OS, config ######################################################################################
# TODO
def os_monkeypatch_help():
    """function os_monkeypatch_help
    Args:
        None
    Returns:
        None
    https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
    """
    print( """    
    """)


def os_module_uncache(exclude='os.system'):
    """Remove package modules from cache except excluded ones.
       On next import they will be reloaded.  Useful for monkey patching
    Args:
        exclude (iter<str>): Sequence of module paths.
        https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
    Returns:
        None
    """
    import sys
    pkgs = []
    for mod in exclude:
        pkg = mod.split('.', 1)[0]
        pkgs.append(pkg)

    to_uncache = []
    for mod in sys.modules:
        if mod in exclude:
            continue

        if mod in pkgs:
            to_uncache.append(mod)
            continue

        for pkg in pkgs:
            if mod.startswith(pkg + '.'):
                to_uncache.append(mod)
                break

    for mod in to_uncache:
        del sys.modules[mod]


def os_import(mod_name="myfile.config.model", globs:dict=None, verbose=True):
    """function os_import
    Args:
        mod_name:
        globs: Should be globals()
        verbose:
    Returns:
        None
    """
    ### Import in Current Python Session a module   from module import *
    ### from mod_name import *
    if globs is None:
        ValueError("globs is None, please use glob=globals()")

    module = __import__(mod_name, fromlist=['*'])
    if hasattr(module, '__all__'):
        all_names = module.__all__
    else:
        all_names = [name for name in dir(module) if not name.startswith('_')]

    all_names2 = []
    no_list    = ['os', 'sys' ]
    for t in all_names :
        if t not in no_list :
            ### Mot yet loaded in memory  , so cannot use Global
            #x = str( globs[t] )
            #if '<class' not in x and '<function' not in x and  '<module' not in x :
            all_names2.append(t)
    all_names = all_names2

    if verbose :
        print("Importing: ")
        for name in all_names :
            print( f"{name}=None", end=";")
        print("")
    globs.update({name: getattr(module, name) for name in all_names})







###################################################################################################
def os_search_content(srch_pattern=None, ignore_exts = [] ,mode="str", dir1="", file_pattern="*.*", dirlevel=1, callback = None, start_time = None, end_time = None):
    """  search inside the files with a max dir level.
    Docs::

        Args:
            srch_pattern (list of str) : Strings to match the file's content. (Defaults to None.)
            mode (str)                 : Mode to search, ("str" or "regex"). (Defaults to "str".)
            dir1 (str)                 : Directory name to search its content. (Defaults to "".)
            file_pattern (str)         : File pattern to match the content. (Defaults to "*.*".)
            dirlevel (int)             : Max dir level to search. (Defaults to 1.)
        Returns:
            Returns a df with the matches, the columns are the following:
                1.search: Word of the matching.
                2.filename: Directory of the matching.
                3.lineno: Number line of the matching.
                4.pos: Position of the matching.
                5.line: Line of the matching.
        Examples:
            from utilmy import oos
            path = "/tmp/folder"
            content = oos.os_search_content(dir1=path,file_pattern="*")
            print(content) #Displays a df
    """
    import pandas as pd
    if srch_pattern is None:
        srch_pattern = ["from ", "import "]

    ###  'file', 'dir'
    dict_all = os_walk(dir1, pattern=file_pattern, dirlevel=dirlevel)
    if(dict_all["file"]):
        dict_all["file"] = glob_glob(file_list=dict_all["file"],start_date=start_time,end_date=end_time)
    ll = []
    for f in dict_all["file"]:
        if ignore_exts and os.path.splitext(f)[1] in ignore_exts:
            continue
        result = z_os_search_fast(f, texts=srch_pattern, mode=mode)
        if callback and result:
            callback(f)
        ll = ll + result
    df = pd.DataFrame(ll, columns=["search", "filename", "lineno", "pos", "line"])
    return df


def z_os_search_fast(fname, texts=None, mode="regex/str"):
    """function z_os_search_fast
    search inside all files.
    
    Docs::

        Args:
            fname (str)         : Path of the file.
            texts (list of str) : Strings or regex to search.
            mode (str)          : Mode to search. ("str" or "regex"). (default to "regex/str".)
        Returns:
            Return a list of tuples. each tuple has the following values of each matching:
                1. Word of the matching.
                2. Directory of the matching.
                3. Number line of the matching.
                4. Position of the matching.
                5. Line of the matching.
        Examples:
            from utilmy import oos
            path = "/tmp/file"
            searching = oos.z_os_search_fast(fname=path,texts=["dummy"],mode="str")
            print("Searching result:", searching)
    """
    import re
    if texts is None:
        texts = ["myword"]

    res = []  # url:   line_id, match start, line
    enc = "utf-8"
    fname = os.path.abspath(fname)
    try:
        with open(fname, "rb") as f: # using wi
            if mode == "regex":
                texts = [(text, re.compile(text.encode(enc))) for text in texts]
                for lineno, line in enumerate(f):
                    for text, textc in texts:
                        found = re.search(textc, line)
                        if found is not None:
                            try:
                                line_enc = line.decode(enc)
                            except UnicodeError:
                                line_enc = line
                            res.append((text, fname, lineno + 1, found.start(), line_enc))

            elif mode == "str":
                texts = [(text, text.encode(enc)) for text in texts]
                for lineno, line in enumerate(f):
                    for text, textc in texts:
                        found = line.find(textc)
                        if found > -1:
                            try:
                                line_enc = line.decode(enc)
                            except UnicodeError:
                                line_enc = line
                            res.append((text, fname, lineno + 1, found, line_enc))

    except IOError as xxx_todo_changeme:
        (_errno, _strerror) = xxx_todo_changeme.args
        print("permission denied errors were encountered")

    except re.error:
        print("invalid regular expression")

    return res







###################################################################################################
def os_variable_init(ll, globs):
    """function os_variable_init
    Docs::
        Args:
            ll:
            globs:
        Returns:
            None
    """
    for x in ll :
        try :
            globs[x]
        except :
            globs[x] = None


def os_variable_exist(x ,globs, msg="") :
    """function os_variable_exist
    Docs::
        Args:
            x:
            globs: globals()
            msg:str = ""
        Returns:
            True | False
    """
    # x_str = str(globs.get(x, None))
    # if "None" in x_str:
    #     log("Using default", x)
    #     return False
    # else :
    #     log("Using ", x)
    #     return True

    if x not in globs:
        log("Using default", x)
        return False

    log("Using ", x)
    return True


def os_variable_check(ll, globs=None, do_terminate=True, raise_error_if_none=True):
    """function os_variable_check
    Docs::
        Checks if all variables are defined
        Args:
            ll: list of variables
            globs:None
            do_terminate:bool = True - Terminate if not defined
            raise_error_if_none:bool = False - Raise error if any variable is None
        Returns:
            bool - True if all variables are defined
    """
    import sys
    # for x in ll :
    #     try :
    #         a = globs[x]
    #         if a is None : raise Exception("")
    #     except :
    #         log("####### Vars Check,  Require: ", x  , "Terminating")
    #         if do_terminate:
    #             sys.exit(0)

    for x in ll:
        try:
            a = globs[x]
            if a is None and raise_error_if_none:
                raise Exception(f"Variable {x} is None")
        except:
            if do_terminate:
                log("####### Vars Check,  Require: ", x, "Terminating")
                sys.exit(0)
            else:
                return False

    return True


def os_variable_del(varlist, globx):
    """function os_clean_memory
        Docs::
            Args:
                varlist: list of variables
                globx: globals()
            Returns:
                None
    """
    for x in varlist :
        try :
            del globx[x]
            gc.collect()
        except : pass


def os_ram_sizeof(o, ids, hint=" deep_getsizeof(df_pd, set()) "):
    """ Find the memory footprint of a Python object
    Docs::
        deep_getsizeof(df_pd, set())
        The sys.getsizeof function does a shallow size of only. It counts each
        object inside a container as pointer only regardless of how big it
    """
    from collections import Mapping, Container
    from sys import getsizeof

    _ = hint

    d = os_ram_sizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, str):
        r = r

    if isinstance(o, Mapping):
        r = r + sum(d(k, ids) + d(v, ids) for k, v in o.items())

    if isinstance(o, Container):
        r = r + sum(d(x, ids) for x in o)

    return r * 0.0000001


def os_get_function_name():
    """function os_get_function_name
    Docs::
        Args:
            None
        Returns:
            ss
    """
    ### Get ane,
    import sys, socket
    ss = str(os.getpid()) # + "-" + str( socket.gethostname())
    ss = ss + "," + str(__name__)
    try :
        ss = ss + "," + __class__.__name__
    except :
        ss = ss + ","
    ss = ss + "," + str(  sys._getframe(1).f_code.co_name)
    return ss






###################################################################################################
def os_get_process_info(sep="-"):
    """ get  PID process-IPAdress-UnixTime to identify uniquely each process.
        Docs::
            Args:
                sep="-" (str)
            Returns:
                sep.join(ss)
    """
    import time
    ss = []
    ss.append( str(os.getpid()) )
    ss.append( os_get_ip())
    ss.append( str(int(time.time())) )
    return sep.join(ss)



def os_get_uniqueid(format="int"):
    """ Unique INT64 ID:  OSname +ip + process ID + timeStamp
        for distributed compute
    Docs::
        Args:
            format:str = "int"
        Returns:
            None
    """
    


def os_get_os():
    """function os_get_os
    """
    import platform
    return platform.system()

def get_public_ip():
    import requests
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
    except:
        pass
    return None

def os_get_ip(mode='internal'):
    """Return primary ip adress
    Docs::
        Does NOT need routable net access or any connection at all.
        Works even if all interfaces are unplugged from the network.
        Does NOT need or even try to get anywhere else.
        Works with NAT, public, private, external, and internal IP's
        Pure Python 2 (or 3) with no external dependencies.
        Works on Linux, Windows, and OSX.
        Args:
            mode='internal' (str)
    """

    if mode =='internal':
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    else :
        # import requests, json
        # public_ip = json.loads(requests.get("https://ip.seeip.org/jsonip?").text)["ip"]
        # return public_ip

        return get_public_ip()


# TODO
def os_cpu_info():
    """ get info on CPU  : nb of cpu, usage
    Docs:
        https://stackoverflow.com/questions/9229333/how-to-get-overall-cpu-usage-e-g-57-on-linux
        Args:
            None
        Returns:
            ddict
    """
    ncpu= os.cpu_count()

    # cmd = """ top -bn1 | grep "Cpu(s)" |  sed "s/.*, *\([0-9.]*\)%* id.*/\1/" |  awk '{print 100 - $1"%"}'  """
    # cpu_usage = os_system(cmd)


    # cmd = """ awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1) "%"; }' <(grep 'cpu ' /proc/stat) <(sleep 1;grep 'cpu ' /proc/stat) """
    # cpu_usage = os_system(cmd)

    import psutil
    cpu_usage = psutil.cpu_percent(interval=1)

    ddict= {'ncpu': ncpu, 'cpu_usage': cpu_usage}
    return ddict


def os_ram_info():
    """ Get total memory and memory usage in any OS
        Docs::
            Args:
                None
            Returns:
                ret (dict) : total, free, used, percent
    """
    # if 'linux' in sys.platform.lower():
    #     with open('/proc/meminfo', 'r') as mem:
    #         ret = {}
    #         tmp = 0
    #         for i in mem:
    #             sline = i.split()
    #             if str(sline[0]) == 'MemTotal:':
    #                 ret['total'] = int(sline[1])
    #             elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
    #                 tmp += int(sline[1])
    #         ret['free'] = tmp
    #         ret['used'] = int(ret['total']) - int(ret['free'])
    #     return ret

    import psutil
    mem = psutil.virtual_memory()
    ret = {}
    ret['total'] = mem.total
    ret['free'] = mem.free
    ret['used'] = mem.used
    ret["percent"] = mem.percent

    return ret



def os_sleep_cpu(cpu_min=30, sleep=10, interval=5, msg= "", verbose=True):
    """function os_sleep_cpu
    Docs::
        Args:
            cpu_min:int = 30
            sleep:int = 10
            interval:int = 5
            msg:str = ""
            verbose:bool = True
        Returns:
            aux
    """
    #### Sleep until CPU becomes normal usage
    import psutil, time
    aux = psutil.cpu_percent(interval=interval)  ### Need to call 2 times
    while aux > cpu_min:
        ui = psutil.cpu_percent(interval=interval)
        aux = 0.5 * (aux +  ui)
        if verbose : log( 'Sleep sec', sleep, ' Usage %', aux, ui, msg )
        time.sleep(sleep)
    return aux



def os_wait_processes(nhours=7):
    """function os_wait_processes
    Args:
        nhours:int = 7
    Returns:
        None
    """
    t0 = time.time()
    while (time.time() - t0 ) < nhours * 3600 :
        ll = os_process_list()
        if len(ll) < 2 : break   ### Process are not running anymore
        log("sleep 30min", ll)
        time.sleep(3600* 0.5)




###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()

