from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from eptools.slack_factory import SlackFactory
import os
from inspect import getframeinfo, stack
import traceback

#_svc_name_ = "..."
#log_path = C:\\logs\\pythonservice\\

eformat = logging.Formatter('%(asctime)s,%(msecs)d - %(levelname)s - %(message)s')
# iformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s - (in %(funcName)s)')
iformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def createLogger(name, log_path, level=logging.DEBUG, normal_format=iformat, error_format=eformat):
    handler = logging.FileHandler(os.path.join(log_path, 'info.log'))
    debug_handler = logging.FileHandler(
        os.path.join(log_path, 'debug.log'))
    error_handler = logging.FileHandler(
        os.path.join(log_path, 'error.log'))
    handler.setFormatter(normal_format)
    debug_handler.setFormatter(normal_format)
    error_handler.setFormatter(error_format)
    handler.setLevel(logging.INFO)
    debug_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.ERROR)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    return logger


def createRotatingLogger(name, log_path, level=logging.DEBUG, normal_format = iformat, error_format = eformat):
    handler = RotatingFileHandler(os.path.join(log_path , 'info.log'),backupCount=100,maxBytes=20_000_000,delay=True)
    debug_handler = RotatingFileHandler(os.path.join(log_path , 'debug.log'),backupCount=100,maxBytes=20_000_000,delay=True)
    error_handler = RotatingFileHandler(os.path.join(log_path , 'error.log'),backupCount=100,maxBytes=20_000_000,delay=True)
    handler.setFormatter(normal_format)
    debug_handler.setFormatter(normal_format)
    error_handler.setFormatter(error_format)
    handler.setLevel(logging.INFO)
    debug_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.ERROR)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    return logger

def createSlackLogger(name, logger = None, config_path=None):
    # optional config_path
    slacker = SlackFactory(config_path=config_path, logger=logger)
    return slacker

class EasyPostLogger():
    """ 
    Wrapper class for logging.

    Allows to log to following outputs:
    - console
    - file log
    - slack log

    params
    ----
    name
        If name is passed, it will setup a file logger and slack logger by default
    If 
    """
    _instance_cache = {}
    def __new__(cls, name: str=None, logpath: str=None, config_path: str=None):
        # Generate a unique key based on the parameters
        if not name:
            name = "AnonymousLogger"
        key = (name)

        # Check if an instance with the same parameters exists
        if key not in cls._instance_cache:
            instance = super(EasyPostLogger, cls).__new__(cls)
            cls._instance_cache[key] = instance
            instance.file_logger = None
            instance.slack_logger = None
            instance.config_path = config_path
            instance.name = name
            if not name:
                instance.name = "AnonymousLogger"
            instance._svc_logger_ = instance.name + '_logger'
            if logpath:
                instance.name = instance.name
                instance._svc_logpath_ = os.path.join(logpath,instance.name) + '\\'
            else:
                instance._svc_logpath_ = '\\\\10.10.10.12\\F-drive\\Shares\\IT\\ServiceLogs\\' + instance.name + '\\'
            if not os.path.exists(instance._svc_logpath_):
                os.makedirs(instance._svc_logpath_)
            instance.file_logger = createRotatingLogger(instance._svc_logger_ , instance._svc_logpath_)
            instance.slack_logger = createSlackLogger(instance.name,logger=instance.file_logger,config_path=instance.config_path)
            instance.slacker_level = logging.WARNING

        return cls._instance_cache[key]

    def set_file_logger(self, file_logger):
        self.file_logger = file_logger

    def set_slack_logger(self, slack_logger: SlackFactory):
        """ Sets slack logger instance. """
        self.slack_logger = slack_logger

    def set_slack_level(self, log_level: int):
        """ Sets minimum loglevel which is written to slack. """
        self.slacker_level = log_level

    def __overall__(self, msg: str, level: int):
        caller = getframeinfo(stack()[2][0])
        full_msg = f"{msg} \n\t\t\t- (in \"{caller.function}()\" at path \"{caller.filename}\" at line {caller.lineno})"
        if self.file_logger:
            # log to file logger with correct loglevel
            if level == logging.DEBUG: 
                self.file_logger.debug(full_msg)
            elif level == logging.INFO: 
                self.file_logger.info(full_msg)
            elif level == logging.WARNING: 
                self.file_logger.warning(full_msg)
            elif level == logging.ERROR: 
                self.file_logger.error(full_msg)
            elif level == logging.CRITICAL: 
                self.file_logger.critical(full_msg)


        if self.slack_logger:
            if self.slacker_level <= level:
                self.slack_logger.log(self.name, message=full_msg, error=str(msg).split('\n')[0])

    def debug(self, msg: str):
        self.__overall__(msg=msg,level = logging.DEBUG)

    def info(self, msg: str):
        self.__overall__(msg=msg,level = logging.INFO)

    def warning(self, msg: str, ex: Exception = None):
        """ Prints warning log. """
        self.__overall__(msg=msg, level = logging.WARNING)

    def warning_with_exception(self, msg: str, ex: Exception = None):
        """ 
        Prints warning log. 
        
        Params:
        ----
        msg: 
            message to log. Can be message or context in case an exception is passed as second param
        ex:
            Optional exception. 
            Appends the stacktrace of the exception to the msg param. 
        """

        error_msg = msg        
        if ex:
            error_msg += "\n" + str(ex)

        self.__overall__(msg=error_msg,level = logging.WARNING)

    def error(self, msg=None, ex: Exception= None):
        """ 
        Logs a error message to slack and filelogger.

        params
        ----
        msg {str | Exception}:
            If str: message is prepended before param 'ex'
            If Exception: param 'ex' is overwritten with value of param 'msg'
        ex {Exception}:
            Represents the optional exception.
            Gets overwritten with exception of param 'msg' is param 'msg' represents an Exception
        """
        error_msg = self.build_error_msg(msg=msg, ex=ex)
        self.__overall__(msg=error_msg,level = logging.ERROR)

    
    def critical(self, msg=None, ex: Exception= None):
        error_msg = self.build_error_msg(msg=msg, ex=ex)
        self.__overall__(msg=error_msg,level =logging.CRITICAL)

    def build_error_msg(self, msg=None, ex: Exception= None):
        """ 
        
        Only gets called from "error" and "critical"
        """
        # Will contain completele error message
        error_msg = ""
        
        # If param "msg" is an Exception, the param "ex" is overwritten with "msg" which is now the exception 
        if msg and issubclass(type(msg), Exception):
            ex = msg
            msg = None
        
        # Concatenate the message
        if msg:
            error_msg = msg
        if ex:
            # Optional newline to add between message and exception
            if len(error_msg) > 0:
                error_msg += " \n"
            error_msg += type(ex).__name__ + ": "
            error_msg += self.get_exception_with_stacktrace(ex)

        # Safety check: if no params where passed -> send defualt message
        if len(error_msg) < 1:
            error_msg = "Error without info occured"
        
        return error_msg

    def get_exception_with_stacktrace(self, ex):
        """ Gets the stacktrace of an exception. """
        # Reference: https://stackoverflow.com/a/4564595/15657263
        error_msg = str(ex)
        try:
            tb = traceback.format_exc()
            error_msg += "\n" + tb
        except Exception as ex:
            print("Traceback Exception:", ex)

        return error_msg



def test_code_with_slack_logger():
    # Setup logging
    logger = EasyPostLogger()
    slack_logger = createSlackLogger("EPTools-slacker-logger")
    logger.debug("test")
    logger.set_slack_level(logging.ERROR)
    logger.set_slack_logger(slack_logger)

    # Run demo exception which gets caught
    try:
        raise ValueError("I'm an ValueError Exception. Wiehoewiehoe toetatoeta. I will be the last test exception of today. Sorry for disturbing.")
    except Exception as ex:
        logger.warning_with_exception("I'm a test exception that should not happen", ex)
        logger.error(ex)

def test_code__msg_param_is_exception():

    for x in range(50):
        logger = EasyPostLogger('TESTLOGGER')
        logger2 = EasyPostLogger()
    
        try:
            raise ValueError("i'm the exception message")
        except Exception as ex:
            logger.error(msg="Ik ben een context mg van Jonas&Arno", ex=ex)
            logger2.error(ex)


def test_with_logpath():
    logger = EasyPostLogger('TestLogger',logpath='c:\\Logs')
    
    try:
        raise ValueError("i'm the exception message")
    except Exception as ex:
        logger.error(msg="Ik ben een context msg van Jonas&Arno", ex=ex)



if __name__ == '__main__':
    # test_code_with_slack_logger()
    try:
        test_code__msg_param_is_exception()
    except Exception as ex:
        print(ex)
    # test_with_logpath()