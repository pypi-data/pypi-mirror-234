"""
    Application log setup and use
"""

import os
import sys
import logging

from dtscore import utils
from dtscore import globals as gl

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
FATAL = logging.FATAL

#--------------------------------------------------------------------------------------------------
# log setup
def setup_log(moduleName:str, log_filename:str):
    logging.basicConfig(filename=log_filename, filemode='w', format=gl.logformat)
    log_formatter = logging.Formatter(gl.logformat)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter)                                        
    
    log = logging.getLogger(moduleName)
    log.setLevel(gl.loglevel)
    
    # writing to stdout                                                     
    log.addHandler(handler)                                            
   
    log.info('log configured')
    return log

#--------------------------------------------------------------------------------------------------
#   log initialization
def initialize_log(log_filename:str):
    full_log_path = os.path.join(gl.logshome, utils.datestampFileName(log_filename))
    logging.basicConfig(filename=full_log_path, filemode='w', format=gl.logformat)
    log_formatter = logging.Formatter(gl.logformat)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(handler)
    
#--------------------------------------------------------------------------------------------------
def get_log(module_name:str,log_level:int) -> logging.Logger:
    log = logging.getLogger(module_name)
    log.setLevel(log_level)
    return log
