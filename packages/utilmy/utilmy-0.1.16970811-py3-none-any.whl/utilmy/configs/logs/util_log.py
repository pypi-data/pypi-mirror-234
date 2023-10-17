# -*- coding: utf-8 -*-
""" Universal logger
Doc::

   Global ENV Variables
     ## Only those ones are needed:
        export log_verbosity=10
        export log_type='logging'   / 'base' / 'loguru'

        ### Custom Config file
        export log_config_path = "~/myconfig.json"
        LOG_CONFIG = {
           'log_verbosity':  10     ,
            'log_type'     :  'base' ,
        }        

    Usage :
    from util_log import log

    # The severity levels
    # Level name    Severity value  Logger method
    # TRACE         5               logger.trace()
    # DEBUG         10              logger.debug()
    # INFO          20              logger.info()
    # SUCCESS       25              logger.success()
    # WARNING       30              logger.warning()
    # ERROR         40              logger.error()
    # CRITICAL      50              logger.critical()

"""
import os,sys,json
from logging.handlers import SocketHandler
from pathlib import Path


######################################################################################
##### Global settting  ###############################################################

LOG_CONFIG = {}

try:
    LOG_CONFIG_FILE = os.environ.get('log_config_path',  os.getcwd() + "/config.json" )
    with open(LOG_CONFIG_FILE, mode='r') as f:
        LOG_CONFIG = json.load(f)
except Exception as e:
    pass

LOG_CONFIG = {
    'log_verbosity':  os.environ.get('log_verbosity', LOG_CONFIG.get('log_verbosity',10)),
    'log_type'     :  os.environ.get('log_type',  LOG_CONFIG.get('log_type',"base")),
}
VERBOSITY   = int(LOG_CONFIG["log_verbosity"])
LOG_TYPE    = LOG_CONFIG["log_type"]

THISFILE_PATH = Path(__file__).resolve().parent





##############################################################################################
if LOG_TYPE == 'base':
    def log(*s):
        """function log.
        """
        print(*s, flush=True)


    def log2(*s):
        """function log2.
        """
        if VERBOSITY >=2 : print(*s, flush=True)


    def log3(*s):  ### Debugging level 2
        """function log3.
        """
        if VERBOSITY >=3 : print(*s, flush=True)


    def logw(*s):
        """function log warning
        """
        print(*s, flush=True)


    def logc(*s):
        """function log critical
        """
        print(*s, flush=True)


    def loge(*s):
        """function log error
        """
        print(*s, flush=True)


    def logr(*s):
        """function logr.
        """
        print(*s, flush=True)



    #########################################################################################
    def test_log():
        """function test.
        Doc::
        """
        log3("debug2")
        log2("debug")
        log("info")
        logw("warning")
        loge("error")
        logc("critical")

        try:
            a = 1 / 0
        except Exception as e:
            logr("error", e)
            loge("Catcch"), e



##############################################################################################
if LOG_TYPE == 'logging':
    import logging, socket
    ################### Logs #################################################################
    FORMATTER_1 = logging.Formatter("%(asctime)s,  %(name)s, %(levelname)s, %(message)s")
    FORMATTER_2 = logging.Formatter("%(asctime)s.%(msecs)03dZ %(levelname)s %(message)s")
    FORMATTER_3 = logging.Formatter("%(asctime)s  %(levelname)s %(message)s")
    FORMATTER_4 = logging.Formatter("%(asctime)s, %(process)d, %(filename)s,    %(message)s")
    FORMATTER_5 = logging.Formatter(
        "%(asctime)s, %(process)d, %(pathname)s%(filename)s, %(funcName)s, %(lineno)s,  %(message)s"
    )


    ########################################################################################
    ################### Logger #############################################################
    def logger_setup(
        logger_name=None,
        log_file=None,
        formatter=FORMATTER_1,
        isrotate=False,
        isconsole_output=True,
        logging_level=logging.DEBUG,
    ):
        """  Python logger setup
        Docs::

            from utilmy.config.log import util_log
            
            my_logger = util_log.logger_setup("my module name", log_file="")
            def log(*argv):
            my_logger.info(",".join([str(x) for x in argv]))

        """        
        # Gets the root logger or local one
        logger = logging.getLogger(logger_name)  if logger_name is not None  else logging.getLogger()

        logger.setLevel(logging_level)  # better to have too much log than not enough

        if isconsole_output:
            logger.addHandler(logger_handler_console(formatter))

        if log_file is not None:
            logger.addHandler(logger_handler_file(formatter=formatter, log_file_used=log_file, isrotate=isrotate))

        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger


    def logger_handler_console(formatter=None):
        formatter = FORMATTER_1 if formatter is None else formatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        return console_handler


    def logger_handler_file(isrotate=False, rotate_time="midnight", formatter=None, log_file_used=None):
        from logging.handlers import TimedRotatingFileHandler
        formatter = FORMATTER_1 if formatter is None else formatter
        if isrotate:
            print("Rotate log", rotate_time)
            fh = TimedRotatingFileHandler(log_file_used, when=rotate_time)
            fh.setFormatter(formatter)
            return fh
        else:
            fh = logging.FileHandler(log_file_used)
            fh.setFormatter(formatter)
            return fh


    #######################################################################################
    ##### Alias ###########################################################################
    logger = logger_setup()

    def log(*s):
        """function log.
        """
        logger.info(",".join([str(t) for t in s]))


    def log2(*s):
        """function log2.
        """
        logger.debug(",".join([str(t) for t in s]))


    def log3(*s):  ### Debuggine level 2
        """function log3.
        """
        logger.info(",".join([str(t) for t in s]))


    def logw(*s):
        """function logw.
        """
        logger.warning(",".join([str(t) for t in s]))


    def logc(*s):
        """function logc.
        """
        logger.critical(",".join([str(t) for t in s]))


    def loge(*s):
        """function loge.
        """
        logger.error(",".join([str(t) for t in s]))


    def logr(*s):
        """function logr.
        """
        logger.info(",".join([str(t) for t in s]))


    #########################################################################################
    def test_log():
        """function test.
        """
        log3("debug2")
        log2("debug")
        log("info")
        logw("warning")
        loge("error")
        logc("critical")

        try:
            a = 1 / 0
        except Exception as e:
            logr("error", e)
            loge("Catcch"), e




##############################################################################################
if LOG_TYPE == 'loguru':
    from loguru import logger
    #####################################################################################
    # "socket_test", 'default'  'debug0;
    LOG_CONFIG_PATH = THISFILE_PATH / "config_loguru.yaml"
    LOG_TEMPLATE    = os.environ.get('log_loguru_template', "debug0")


    #####################################################################################
    def logger_setup(log_config_path: str = None, log_template: str = "default", **kwargs):
        """ Generic Logging setup
        Doc::

            Overide logging using loguru setup
            1) Custom config from log_config_path .yaml file
            2) Use shortname log, log2, logw, loge for logging output

            Args:
                log_config_path:
                template_name:
                **kwargs:
            Returns:None

        """
        try:
            from utilmy import config_load
            cfg = config_load(log_config_path)

        except Exception as e:
            print(f"Cannot load yaml file {log_config_path}, Using Default logging setup")
            cfg = {"log_level": "DEBUG", "handlers": {"default": [{"sink": "sys.stdout"}]}}

        ########## Parse handlers  ####################################################
        globals_ = cfg
        handlers = cfg.pop("handlers")[log_template]
        rotation = globals_.pop("rotation")


        for handler in handlers:
            if 'sink' not in handler :
                print(f'Skipping {handler}')
                continue

            if handler["sink"] == "sys.stdout":
                handler["sink"] = sys.stdout

            elif handler["sink"] == "sys.stderr":
                handler["sink"] = sys.stderr

            elif handler["sink"].startswith("socket"):
                sink_data       = handler["sink"].split(",")
                ip              = sink_data[1]
                port            = int(sink_data[2])
                handler["sink"] = SocketHandler(ip, port)

            elif ".log" in handler["sink"] or ".txt" in handler["sink"]:
                handler["rotation"] = handler.get("rotation", rotation)

            # override globals values
            for key, value in handler.items():
                if key in globals_:
                    globals_[key] = value

            handler.update(globals_)

        ########## Addon config  ##############################################
        logger.configure(handlers=handlers)

        ########## Custom log levels  #########################################
        # configure log level in config_log.yaml to be able to use logs depends on severity value
        # if no=9 it means that you should set log level below DEBUG to see logs,
        try:
            logger.level("DEBUG_2", no=9, color="<cyan>")

        except Exception as e:
            ### Error when re=-defining level
            print('warning', e)

        return logger


    #######################################################################################
    ##### Initialization ##################################################################
    logger_setup(log_config_path=LOG_CONFIG_PATH, log_template=LOG_TEMPLATE)


    #######################################################################################
    ##### Alias ###########################################################################
    def log(*s):
        """function log.
        """
        logger.opt(depth=1, lazy=True).info(",".join([str(t) for t in s]))


    def log2(*s):
        """function log2.
        """
        logger.opt(depth=2, lazy=True).debug(",".join([str(t) for t in s]))


    def log3(*s):  ### Debuggine level 2
        """function log3.
        """
        logger.opt(depth=2, lazy=True).debug(",".join([str(t) for t in s]))

    def logw(*s):
        """function logw.
        """
        logger.opt(depth=1, lazy=True).warning(",".join([str(t) for t in s]))


    def logc(*s):
        """function logc.
        """
        logger.opt(depth=1, lazy=True).critical(",".join([str(t) for t in s]))


    def loge(*s):
        """function loge.
        """
        logger.opt(depth=1, lazy=True).exception(",".join([str(t) for t in s]))


    def logr(*s):
        """function logr.
        """
        logger.opt(depth=1, lazy=True).error(",".join([str(t) for t in s]))


    #########################################################################################
    def test_log():
        """function test.
        Doc::
        """
        log3("debug2")
        log2("debug")
        log("info")
        logw("warning")
        loge("error")
        logc("critical")

        try:
            a = 1 / 0
        except Exception as e:
            logr("error", e)
            loge("Catcch"), e


    ######## Stream Server ####################################################################
    import socketserver, pickle, struct,  json

    class LoggingStreamHandler(socketserver.StreamRequestHandler):
        def handle(self):
            """ LoggingStreamHandler:handle.
            Doc::
            """
            from loguru import logger
            while True:
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break
                slen = struct.unpack('>L', chunk)[0]
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))
                record = pickle.loads(chunk)
                #print(json.loads(record['msg']))
                level, message = record["levelname"], json.loads(record["msg"])['text']
                logger.patch(lambda record: record.update(record)).log(level, message)



    def test_launch_server():
        '''.
        Doc::

                Server code from loguru.readthedocs.io
                Use to test network logging

                python   test.py test_launch_server
        '''
        PORT = 5000 #Make sure to set the same port defined in logging template
        server = socketserver.TCPServer(('localhost', PORT), LoggingStreamHandler)
        server.serve_forever()


    def test_server():
        """function test_server.
        Doc::
        """
        print("\n\n\n########## Test 2############################")
        os.environ['log_type'] = 'loguru'
        import util_log


        from util_log import log3, log2, log, logw, loge, logc, logr

        ### Redefine new template
        util_log.logger_setup('config_loguru.yaml', 'server_socket')

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





##############################################################################################
def test_all():
    test_log()



########################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()






#######################################################################################
#######################################################################################
def z_logger_stdout_override():
    """ Redirect stdout --> logger.
    Doc::

            Returns:
    """
    import contextlib
    import sys
    class StreamToLogger:
        def __init__(self, level="INFO"):
            self._level = level

        def write(self, buffer):
            for line in buffer.rstrip().splitlines():
                logger.opt(depth=1).log(self._level, line.rstrip())

        def flush(self):
            pass

    logger.remove()
    logger.add(sys.__stdout__)

    stream = StreamToLogger()
    with contextlib.redirect_stdout(stream):
        print("Standard output is sent to added handlers.")


def z_logger_custom_1():
    """function z_logger_custom_1.
    Doc::

            Args:
            Returns:

    """
    import logging
    import sys
    from pprint import pformat
    from loguru._defaults import LOGURU_FORMAT

    # LOGURU_FORMAT = "<green>{time:DD.MM.YY HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    LOGURU_FORMAT = "<green>{time:DD.MM.YY HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"

    class InterceptHandler(logging.Handler):
        """Logs to loguru from Python logging module"""

        def emit(self, record: logging.LogRecord) -> None:
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = str(record.levelno)

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
                # frame = cast(FrameType, frame.f_back)
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level,
                record.getMessage(),
            )

    def format_record(record: dict) -> str:
        """
        Custom format for loguru loggers.
        Uses pformat for log any data like request/response body during debug.
        Works with logging if loguru handler it.
        Example:
        >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
        >>> logger.bind(payload=).debug("users payload")
        >>> [   {   'count': 2,
        >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
        >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
        """

        format_string = LOGURU_FORMAT
        if record["extra"].get("payload") is not None:
            record["extra"]["payload"] = pformat(
                record["extra"]["payload"], indent=4, compact=True, width=88
            )
            format_string += "\n<level>{extra[payload]}</level>"

        format_string += "{exception}\n"
        return format_string

    def setup_logging():
        # intercept everything at the root logger
        logging.root.handlers = [InterceptHandler()]
        logging.root.setLevel("INFO")

        # remove every other logger's handlers
        # and propagate to root logger
        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

        # configure loguru
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "level": logging.DEBUG,
                    "format": format_record,
                }
            ]
        )
        logger.level("TIMEIT", no=22, color="<cyan>")
