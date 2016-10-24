#!/usr/bin/env python
# coding=utf-8
import logging
import logging.handlers
PROXY_AVAILABLE, PROXY_UNEXPECT, PROXY_UNKNOW_ERR, PROXY_UNAVAILABLE, PROXY_TRANSPARENT = range(5)
VALID, INVALID = range(2)
PROXY, STATUS, CHECK_TIME = range(3)


LOGGERNAME="proxy_check"
LOGNAME = "verifyProxy.log"
FORMATTER = '%(asctime)s|%(thread)s|%(name)s|%(levelname)s|%(filename)s:%(lineno)d %(message)s'
LOGLEVEL = logging.DEBUG
LOG_FILE_NUM = 5
LOG_FILE_SIZE = 20*1024#*1024
class Logger:
    m_instance = None
    def __init__(self):
        self.logger = logging.getLogger(LOGGERNAME)
        self.logger.setLevel(LOGLEVEL)

        fileHandler = logging.handlers.TimedRotatingFileHandler(LOGNAME, 'D', 1, LOG_FILE_NUM)
        fileHandler.suffix = "%Y%m%d.log"
        #fileHandler = logging.handlers.RotatingFileHandler(LOGNAME, maxBytes = LOG_FILE_SIZE, backupCount = LOG_FILE_NUM)
        #fileHandler = logging.FileHandler(LOGNAME)
        fileHandler.setLevel(LOGLEVEL)

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(LOGLEVEL)

        formatter = logging.Formatter(FORMATTER)
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)
    @classmethod
    def getInstance(cls):
        if(cls.m_instance == None):
            cls.m_instance = Logger()
        return cls.m_instance.logger

logging = Logger.getInstance()

