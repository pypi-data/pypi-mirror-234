import json
import os
import sys
import threading
from collections import OrderedDict
from typing import List, Dict, Any

import logging
import time

def formatTime(created, msecs):
        """
        Return the creation time of the specified LogRecord as formatted text.

        This method should be called from format() by a formatter which
        wants to make use of a formatted time. This method can be overridden
        in formatters to provide for any specific requirement, but the
        basic behaviour is as follows: if datefmt (a string) is specified,
        it is used with time.strftime() to format the creation time of the
        record. Otherwise, an ISO8601-like (or RFC 3339-like) format is used.
        The resulting string is returned. This function uses a user-configurable
        function to convert the creation time to a tuple. By default,
        time.localtime() is used; to change this for a particular formatter
        instance, set the 'converter' attribute to a function with the same
        signature as time.localtime() or time.gmtime(). To change it for all
        formatters, for example if you want all logging times to be shown in GMT,
        set the 'converter' attribute in the Formatter class.
        """
        ct = time.localtime(created)
        default_time_format = '%Y-%m-%d %H:%M:%S'
        default_msec_format = '%s,%03d'
        s = time.strftime(default_time_format, ct)
        if default_msec_format:
            s = default_msec_format % (s, msecs)
        return s
# Press the green button in the gutter to run the script.
def findCaller(logThreads=True,logProcesses=True):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        if hasattr(sys, '_getframe'):
            currentframe = lambda: sys._getframe(2)
        else:  # pragma: no cover
            def currentframe():
                """Return the frame object for the caller's stack frame."""
                try:
                    raise Exception
                except Exception:
                    return sys.exc_info()[2].tb_frame.f_back
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        orig_f = f
        if not f:
            f = orig_f
        rv = {"file_name":"(unknown file)", "line_id":0, "function_name":"(unknown function)"}
        while hasattr(f, "f_code"):
            co = f.f_code
            filename_org = os.path.normcase(co.co_filename)
            if filename_org == __file__:
                f = f.f_back
                continue
            try:
                filename = os.path.basename(filename_org)
                module = os.path.splitext(filename)[0]
            except (TypeError, ValueError, AttributeError):
                filename = filename_org
                module = "Unknown module"
            rv["file_name"]= filename
            rv["line_id"] =f.f_lineno
            rv["module_name"] = module
            rv["function_name"] = co.co_name
            break

        if logThreads:
            thread = threading.get_ident()
            threadName = threading.current_thread().name
        else:  # pragma: no cover
            thread = None
            threadName = None

        rv["thread_id"] = thread
        rv["thread_name"] = threadName
        if not logging.logMultiprocessing:  # pragma: no cover
            processName = None
        else:
            processName = 'MainProcess'
            mp = sys.modules.get('multiprocessing')
            if mp is not None:
                # Errors may occur if multiprocessing has not finished loading
                # yet - e.g. if a custom import hook causes third-party code
                # to run when multiprocessing calls import. See issue 8200
                # for an example
                try:
                    processName = mp.current_process().name
                except Exception:  # pragma: no cover
                    pass
        if logProcesses and hasattr(os, 'getpid'):
            process = os.getpid()
        else:
            process = None
        rv["process_id"] = process
        rv["process_name"] =  processName

        ct = time.time()
        msecs = (ct - int(ct)) * 1000
        timestamp = formatTime(ct, msecs)
        rv["timestamp"] = timestamp
        return rv

def createLocation(sysInfo, location:Dict[str,str]):
# 'location','filename', 'modulename', 'funcname', 'process', 'processName', 'thread','threadName', 'lineno',
    location["file_name"] = sysInfo["file_name"]
    location["module_name"] = sysInfo["module_name"]
    location["function_name"] = sysInfo["function_name"]
    location["process_id"] = sysInfo["process_id"]
    location["process_name"] = sysInfo["process_name"]
    location["thread_id"] = sysInfo["thread_id"]
    location["thread_name"] = sysInfo["thread_name"]
    location["line_id"] = sysInfo["line_id"]


def createEventHeader(logType, level, msgid, msgoffset, sysInfo, event_header:List[str]):
    # 1. version

    event_header.append('V.1.1.1-01')
    # 2. asctime

    event_header.append(sysInfo["timestamp"])
    # 3. levelname

    event_header.append(logging.getLevelName(level))
    # 4. location
    location: Dict[str, str] = {}
    createLocation(sysInfo,location)
    event_header.append(location)

    # 5. logtype
    event_header.append(logType)
    # 6. msgid offset
    if msgid is not None and msgid != "":
        event_header.append(msgid)
        if msgoffset is not None:
            event_header.append(msgoffset)

def createEventEntity(message, extra:dict, event_entity:dict):
    #1.组装六要素
    event_entity_keys = ["event_domain", "event_action", "event_object", "event_service", "event_status", "event_subject"]
    for event_entity_key in event_entity_keys:
        if event_entity_key in extra.keys():
            event_entity[event_entity_key] = extra[event_entity_key]
        else:
            event_entity[event_entity_key] = ""
    #2. 添加自定义字段
    for custom_key in extra.keys():
        if custom_key not in event_entity_keys:
            event_entity[custom_key] = extra[custom_key]

    #3. 添加addition_msg
    event_entity["addition_msg"] = message

def logingRuntimeStatus(logType, level, message,extra={}, msgid="", msgoffset=""):
    #0.准备系统信息
    sysInfo = findCaller()
    #1. 组装event_header
    event_header: List[str] = []
    createEventHeader(logType, level, msgid, msgoffset, sysInfo, event_header)
    #2. 组装实体event_entity
    event_entity: Dict[str, Any]
    event_entity = OrderedDict()
    createEventEntity(message, extra, event_entity)
    #3. 组装event_header、event_entity
    log_record: Dict[str, Any]
    log_record = OrderedDict()
    log_record["event_header"] = event_header
    log_record["event_entity"] = event_entity
    #4. 序列化
    return json.dumps(log_record).__str__()
