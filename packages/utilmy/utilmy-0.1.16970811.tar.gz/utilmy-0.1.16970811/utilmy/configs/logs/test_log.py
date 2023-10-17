# -*- coding: utf-8 -*-
""" Test for universal logger

"""
import sys, os, logging, json


##############################################################################
def test_all():

    test1()
    test2()
    test_logging()
    test4()
    test5()



def test1():
    """function test1.

    Testing the functions log3, log2, log, logw, loge, logc, logr

    """
    import io, sys
    # These libraries are for testing output.
    # https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print

    os.environ['log_verbosity']='10'
    os.environ['log_type']='base'

    with open("config.json", mode='w') as f:
        f.write(json.dumps({'log_verbosity': 10, 'log_type': 'base'}, indent=4))

    from utilmy.configs.logs.util_log import log3, log2, log, logw, loge, logc, logr
    log3("debug2")
    log2("debug")
    log("info")
    logw("warning")
    logc("critical")

    log("####### log() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    log("testing log")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing log\n", "FAILED -> config_load(); The return value isn't expected"

    log("####### log2() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    log2("testing log2")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing log2\n", "FAILED -> config_load(); The return value isn't expected"

    log("####### log3() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    log3("testing log3")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing log3\n", "FAILED -> config_load(); The return value isn't expected"
    
    log("####### logw() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    logw("testing logw")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing logw\n", "FAILED -> config_load(); The return value isn't expected"

    log("####### logc() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    logc("testing logc")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing logc\n", "FAILED -> config_load(); The return value isn't expected"

    log("####### loge() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    loge("testing loge")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing loge\n", "FAILED -> config_load(); The return value isn't expected"

    log("####### logr() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    logr("testing logr")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "testing logr\n", "FAILED -> config_load(); The return value isn't expected"

    try:
        a = 1 / 0
    except Exception as e:
        logr("error", e)
        loge("Exception"), e

    log("finish")

        


def test2():
    """function test2.

    Testing the functions logger_setup, logr, loge

    """
    os.environ['log_verbosity']='20'
    os.environ['log_type']='loguru'

    with open("config.json", mode='w') as f:
        f.write(json.dumps({'log_verbosity': 5, 'log_type': 'base'}, indent=4))

    # import util_log
    from utilmy.configs.logs import util_log

    import importlib
    importlib.reload(util_log)

    from utilmy.configs.logs.util_log import log3, log2, log, logw, loge, logc, logr

    ### Redefine new template
    util_log.logger_setup('config_loguru.yaml', 'default')

    log3("debug2")
    log2("debug")
    log("info")
    logw("warning")
    logc("critical")

    try:
        a = 1 / 0
    except Exception as e:
        logr("error", e)
        loge("Exception"), e

    log("finish")



def test_logging():
    """function test_logging.

    Testing the functions in util_log.py

    """
    os.environ['log_verbosity']='10'
    os.environ['log_type']='logging'

    with open("config.json", mode='w') as f:
        f.write(json.dumps({'log_verbosity': 10, 'log_type': 'logging'}, indent=4))

    from utilmy.configs.logs import util_log

    import importlib
    importlib.reload(util_log)

    from utilmy.configs.logs.util_log import logger, log3, log2, log, logw, loge, logc, logr, logger_setup
    from utilmy.configs.logs.util_log import FORMATTER_1, FORMATTER_2, FORMATTER_3, FORMATTER_4, FORMATTER_5

    s='test logger_name'
    print('\ntest logger_name')
    logger=logger_setup(logger_name= 'test_logging' )
    log2(s)

    # test log_fomatter
    print('\ntest log_fomatter ')
    log_formats=[FORMATTER_1, FORMATTER_2,FORMATTER_3,FORMATTER_4,FORMATTER_5]
    for format in log_formats:
        logger=logger_setup(formatter=format)
        log2(s)

    # test isrotate
    s='test isrotate'
    print('\ntest isrotate ')
    logger=logger_setup(isrotate=True)
    log2(s)

    # test isconsole_output
    s='test isconsole_output'
    print('\ntest isconsole_output ')
    logger=logger_setup(isconsole_output=False)
    log2(s)

    # test logging_level
    print('\ntest logging levels')
    log_levels=[logging.CRITICAL, logging.ERROR,logging.WARNING,logging.INFO,logging.DEBUG]

    for log in log_levels:
        logger=logger_setup(logging_level=log)
        if log==logging.CRITICAL:
            s='critical'
            logc(s)
        elif log==logging.ERROR:
            s='error'
            loge(s)
        elif log==logging.WARNING:
            s='warning'
            logw(s)
        elif log==logging.INFO:
            s='info'
            log2(s)
        elif log==logging.DEBUG:
            s='debug'
            log3(s)


    # test log_file
    s='test log_file'
    print('\ntest log_file test.log')
    logger=logger_setup(log_file='test.log')
    log2(s)
  
def test4():
    """ function test4.
    
    Testing the functions log2 and log3 with verbosity equals to 1.
    
    """
    import io, sys

    os.environ['log_verbosity']='1'
    os.environ['log_type']='base'

    with open("config.json", mode='w') as f:
        f.write(json.dumps({'log_verbosity': 1, 'log_type': 'base'}, indent=4))

    from utilmy.configs.logs.util_log import log3, log2, log

    log("####### log2() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    log2("testing log2")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "", "FAILED -> config_load(); The return value isn't expected"

    log("####### log3() ..")
    captured_output = io.StringIO()
    sys.stdout = captured_output
    log3("testing log3")
    sys.stdout = sys.__stdout__
    result_value = captured_output.getvalue()
    assert result_value == "", "FAILED -> config_load(); The return value isn't expected"
    
def test5():
    """ function test5.
    
    Testing the functions in util_log.py.
    
    """

    import importlib
    import utilmy as uu
    from utilmy.configs.logs import util_log
    drepo, dirtmp = uu.dir_testinfo()

    util_log.log("Testing default env values")
    importlib.reload(util_log)
    assert util_log.VERBOSITY == 10, "FAILED; VERBOSITY wasn't expected"
    assert util_log.LOG_TYPE == "base", "FAILED; LOG_TYPE wasn't expected"
    
    util_log.log("Testing log_verbosity and log_type")
    os.environ['log_verbosity'] = '1'
    os.environ['log_type'] = 'logging'
    importlib.reload(util_log)
    assert util_log.VERBOSITY == 1, "FAILED; VERBOSITY wasn't expected"
    assert util_log.LOG_TYPE == "logging", "FAILED; LOG_TYPE wasn't expected"
    os.environ.pop('log_verbosity', None)
    os.environ.pop('log_type', None)

    util_log.log("Testing log_config_path")
    os.environ['log_config_path'] = dirtmp+"config.json"
    with open(dirtmp+"config.json", mode='w') as f:
        f.write(json.dumps({'log_verbosity': 2, 'log_type': 'logging',}, indent=4))
    importlib.reload(util_log)
    assert util_log.VERBOSITY == 2, "FAILED; VERBOSITY wasn't expected"
    assert util_log.LOG_TYPE == "logging", "FAILED; LOG_TYPE wasn't expected"
    os.remove(dirtmp+"config.json")

    util_log.log("Testing order priority")
    os.environ['log_config_path'] = dirtmp+"config.json"
    os.environ['log_verbosity'] = '3'
    with open(dirtmp+"config.json", mode='w') as f:
        f.write(json.dumps({'log_verbosity': 2, 'log_type': 'logging',}, indent=4))
    importlib.reload(util_log)
    assert util_log.VERBOSITY == 3, "FAILED; VERBOSITY wasn't expected"
    assert util_log.LOG_TYPE == "logging", "FAILED; LOG_TYPE wasn't expected"
    os.remove(dirtmp+"config.json")
    os.environ.pop('log_verbosity', None)
    os.environ.pop('log_type', None)

############################################################################
if __name__ == "__main__":
    # test_logging()
    import fire
    fire.Fire()


"""
03.07.21 00:06:55|DEBUG   |   __main__    |    mytest     |  5|debug
03.07.21 00:06:55|INFO    |   __main__    |    mytest     |  6|info
03.07.21 00:06:55|WARNING |   __main__    |    mytest     |  7|warning
03.07.21 00:06:55|ERROR   |   __main__    |    mytest     |  8|error
NoneType: None
03.07.21 00:06:55|CRITICAL|   __main__    |    mytest     |  9|critical
03.07.21 00:06:55|ERROR   |   __main__    |    mytest     | 14|error,division by zero
03.07.21 00:06:55|ERROR   |   __main__    |    mytest     | 15|Catcch
Traceback (most recent call last):

  File "D:/_devs/Python01/gitdev/arepo/zz936/logs\test.py", line 21, in <module>
    mytest()
    └ <function mytest at 0x000001835D132EA0>

> File "D:/_devs/Python01/gitdev/arepo/zz936/logs\test.py", line 12, in mytest
    a = 1 / 0

ZeroDivisionError: division by zero

Process finished with exit code 0


"""
