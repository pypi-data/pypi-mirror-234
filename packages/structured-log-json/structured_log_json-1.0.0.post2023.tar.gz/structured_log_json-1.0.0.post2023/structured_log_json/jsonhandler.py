from logging.handlers  import BaseRotatingHandler
from logging import  FileHandler
import os
import re
import time
from typing import Tuple
import requests
import configparser
import json

class JsonRotatingFileHandler(BaseRotatingHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size.
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0,
                 encoding=None, delay=False):
        """
        Open the specified file and use it as the stream for logging.

        By default, the file grows indefinitely. You can specify particular
        values of maxBytes and backupCount to allow the file to rollover at
        a predetermined size.

        Rollover occurs whenever the current log file is nearly maxBytes in
        length. If backupCount is >= 1, the system will successively create
        new files with the same pathname as the base file, but with extensions
        "arbitrament_20220101_0001.log", "arbitrament_20220101_0001.log" etc. appended to it.
        For example, with a backupCount of 5
        and a base file name of "arbitrament.log" log at 2022.01.01, you would get "arbitrament_20220101_0000.log",
        "arbitrament_20220101_0001.log", "arbitrament_20220101_0002.log", ... through to "arbitrament_20220101_0005.log".
        The file being written to is always "arbitrament_20220101_0000.log" - when it gets filled up, it is closed
        and renamed to "arbitrament_20220101_0001.log", and if files "arbitrament_20220101_0001.log", "arbitrament_20220101_0002.log" etc.
        exist, then they are renamed to "arbitrament_20220101_0003.log", "arbitrament_20220101_0004.log" etc.
        respectively.

        If maxBytes is zero, rollover never occurs.
        """
        # If filename not end with"_\d{4}\d{2}\d{2}(\.\w+)?$" ;
        # filename need append date suffix
        if re.search("(_\d{4}\d{2}\d{2}(\.\w+)?$)", filename) is None:
            filename, self.baseFileDate = self.__add_date_in_filename(filename)
        # split Filename's prefix and suffix
        self.suffixFilename = self.__get_suffixFilename_from_baseFilename(filename)
        self.prefixFilename = self.__get_prefixFilename_from_baseFilename(filename, self.suffixFilename)
        if self.baseFileDate is None:
            self.baseFileDate = self.__getBaseFileDate(self.suffixFilename)
        # If rotation/rollover is wanted, it doesn't make sense to use another
        # mode. If for example 'w' were specified, then if there were multiple
        # runs of the calling application, the logs from previous runs would be
        # lost if the 'w' is respected, because the log file would be truncated
        # on each run.
        if maxBytes > 0:
            mode = 'a'
        BaseRotatingHandler.__init__(self, filename, mode, encoding=encoding,
                                     delay=delay)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def __getBaseFileDate(self, str)->str:
        extractDateStr = re.search("_(\d{4}\d{2}\d{2})(\.\w+)?$", str)
        if extractDateStr is  not None:
            return extractDateStr.group(1)

    def __get_suffixFilename_from_baseFilename(self, filename, suffix:str = '.log'):
        suffixFilename = ''
        suffixPos = filename.rfind(suffix)
        if suffixPos != -1:
            suffixFilename = filename[suffixPos::]
        return suffixFilename

    def __get_prefixFilename_from_baseFilename(self, filename, suffixFilename:str = '.log'):
        prefixFilename = ''
        suffixPos = filename.rfind(suffixFilename)
        if suffixPos != -1:
            prefixFilename = filename[:suffixPos]
        return prefixFilename

    def __add_date_in_filename(self, filename)-> Tuple[str,str]:
        """
        filename splice date, create new filename : XXXX_YYYYMMDD_0000.log
        :return: newFilename->str
        """
        #1. get current time, and formate date
        dateStr = time.strftime('%Y%m%d', time.localtime(time.time()))
        #2. filename splice date
        prefixFilename = self.__get_prefixFilename_from_baseFilename(filename)
        suffixFilename = self.__get_suffixFilename_from_baseFilename(filename)
        newFilename = prefixFilename + '_' + dateStr + suffixFilename

        return newFilename, dateStr

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # 1. baseFilename splice date
        #baseFilename,  dateStr  = self.__splice_date_suffix()
        # 2.  switches from one file to the next when the current file reaches a certain size.
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("{}_{:04d}{}".format(self.prefixFilename,
                                                                      i,
                                                                      self.suffixFilename))
                dfn = self.rotation_filename("{}_{:04d}{}".format(self.prefixFilename,
                                                                              i + 1,
                                                                              self.suffixFilename))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename("{}_{:04d}{}".format(self.prefixFilename,
                                                                    1,
                                                                    self.suffixFilename))
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()
            
    def create_internal_request(self, log_record):

        # 1. 读取配置文件
        #print (type(log_record))
        postapi_config = configparser.ConfigParser()
        config_file = "/etc/mr/config_5th.ini"
        postapi_config.read(config_file)

        api_status = postapi_config.get("global", "api_enable")

        # 2. 创建post data
        if api_status == "yes":
            api_server_url =  postapi_config.get("global", "server_url_internal")
            host_ip = postapi_config.get("global", "ip")
            log_type = log_record['event_header'][-1]
            timestamp = time.time()
            localtime = time.localtime(timestamp)
            default_time_format = '%Y-%m-%d %H:%M:%S'
            log_time = time.strftime(default_time_format, localtime)
            #log_time = log_record['event_header'][1]
            #str_message = json.dumps(log_record)

            #post_data = {"ip":host_ip,"type": "mimic_router","log_type": log_type,"time":log_time ,"message":str_message }
            post_data = {"ip":host_ip,"type": "mimic_router","log_type": log_type,"time":log_time ,"message":log_record }
            headers = {"Content-Type":"application/json"}
            try:
                response = requests.post(url=api_server_url,headers=headers,data=json.dumps(post_data),timeout=2.5)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                return e

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.create_internal_request(json.loads(msg))   #发送post报文给赛宁接口
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0

    def __isNeedNewBaseFileStream(self):
        # 1. get current time, and formate date
        dateStr = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 2. compare current time to self.baseFileDate
        if self.baseFileDate is None \
            or self.baseFileDate != dateStr:
            return True
        else:
            return False
    def __createNewBaseFileStream(self):
        """
        create new date base file
        :return:
        """
        # 1. close old date file stream
        if self.stream:
            self.stream.close()
            self.stream = None
        # 2. get current time, and formate date
        dateStr = time.strftime('%Y%m%d', time.localtime(time.time()))
        #3. splice new base file name
        newPrefixFilename =  re.search("(\S+)_(\d{4}\d{2}\d{2})(\.\w+)?$", self.prefixFilename).group(1)

        newFilename = newPrefixFilename + '_' + dateStr + self.suffixFilename
        #4. creat new file stream
        if os.path.exists(newFilename):
            os.remove(newFilename)

        self.baseFilename = newFilename

        if not self.delay:
            self.stream = self._open()
        self.baseFileDate = dateStr
        self.prefixFilename = newPrefixFilename

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.__isNeedNewBaseFileStream():
                self.__createNewBaseFileStream()
            else:
                if self.shouldRollover(record):
                    self.doRollover()
            FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)
