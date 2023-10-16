# -*- coding: utf-8 -*-

import sys
import logging

"""
Loggers are created at the top of modules. Therefore each code may access
a logger. But there is a fundamental problem to this approach:

The configuration that determines the state of program may come from various
sources and is parsed only at runtime in the config.py module. In this config, the
loglevel is also specified.

So we need to adjust the loglevel to the value set in
the configuration for each submodule.
"""

def setup_logger(level=logging.INFO,
         format='[%(threadName)s] - %(asctime)s - %(name)s - %(levelname)s - %(message)s',
         logfile='marketing.log'):
    """
    Configure global log settings for GoogleScraper
    """
    logger = logging.getLogger()
    logger.setLevel(level)
   

    # See here: http://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module
    if not len(logger.handlers):
        formatter = logging.Formatter(format)
        # set stream to sys.stdout see https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        if logfile is not None:
            fh = logging.FileHandler(logfile)
            fh.setFormatter(formatter)
            logger.addHandler(fh)