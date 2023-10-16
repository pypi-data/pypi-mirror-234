'''
This library is provided to allow standard python logging
to output log data as JSON formatted strings
'''
import logging
import json
import re
from datetime import date, datetime, time, timezone
import traceback
import importlib

from typing import Any, Dict, Union, List, Tuple

from inspect import istraceback

from collections import OrderedDict


# skip natural LogRecord attributes
# http://docs.python.org/library/logging.html#logrecord-attributes


RESERVED_ATTRS: Tuple[str, ...] = (
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module',
    'msecs', 'message', 'msg', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName')

STATIC_ATTRS: Tuple[str, ...] = (
    'event_head', 'version', 'asctime', 'levelname',
    'location', 'filename', 'modulename', 'funcname', 'process', 'processName', 'thread',  'threadName', 'lineno',
    'logtype',
    'msgid', 'msgoffset',
    'event_entity', 'event_domain', 'event_action', 'event_object', 'event_service', 'event_status', 'event_subject',
    'addition_msg')


def merge_record_extra(record: logging.LogRecord, target: Dict, reserved: Union[Dict, List]) -> Dict:
    """
    Merges extra attributes from LogRecord object into target dictionary

    :param record: logging.LogRecord
    :param target: dict to update
    :param reserved: dict or list with reserved keys to skip
    """
    for key, value in record.__dict__.items():
        # this allows to have numeric keys
        if (key not in reserved
                and not (hasattr(key, "startswith")
                         and key.startswith('_'))):
            target[key] = value
    return target


class JsonEncoder(json.JSONEncoder):
    """
    A custom encoder extending the default JSONEncoder
    """

    def default(self, obj):
        if isinstance(obj, (date, datetime, time)):
            return self.format_datetime_obj(obj)

        elif istraceback(obj):
            return ''.join(traceback.format_tb(obj)).strip()

        elif type(obj) == Exception \
                or isinstance(obj, Exception) \
                or type(obj) == type:
            return str(obj)

        try:
            return super(JsonEncoder, self).default(obj)

        except TypeError:
            try:
                return str(obj)

            except Exception:
                return None

    def format_datetime_obj(self, obj):
        return obj.isoformat()


class JsonFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as json strings.
    Extra values will be formatted as str() if not supported by
    json default encoder
    """

    def __init__(self, *args, **kwargs):
        """
        :param json_default: a function for encoding non-standard objects
            as outlined in https://docs.python.org/3/library/json.html
        :param json_encoder: optional custom encoder
        :param json_serializer: a :meth:`json.dumps`-compatible callable
            that will be used to serialize the log record.
        :param json_indent: an optional :meth:`json.dumps`-compatible numeric value
            that will be used to customize the indent of the output json.
        :param prefix: an optional string prefix added at the beginning of
            the formatted string
        :param rename_fields: an optional dict, used to rename field names in the output.
            Rename message to @message: {'message': '@message'}
        :param static_fields: an optional dict, used to add fields with static values to all logs
        :param json_indent: indent parameter for json.dumps
        :param json_ensure_ascii: ensure_ascii parameter for json.dumps
        :param reserved_attrs: an optional list of fields that will be skipped when
            outputting json log record. Defaults to all log record attributes:
            http://docs.python.org/library/logging.html#logrecord-attributes
        :param timestamp: an optional string/boolean field to add a timestamp when
            outputting the json log record. If string is passed, timestamp will be added
            to log record using string as key. If True boolean is passed, timestamp key
            will be "timestamp". Defaults to False/off.
        """
        self.json_default = self._str_to_fn(kwargs.pop("json_default", None))
        self.json_encoder = self._str_to_fn(kwargs.pop("json_encoder", None))
        self.json_serializer = self._str_to_fn(kwargs.pop("json_serializer", json.dumps))
        self.json_indent = kwargs.pop("json_indent", None)
        self.json_ensure_ascii = kwargs.pop("json_ensure_ascii", True)
        self.prefix = kwargs.pop("prefix", "")
        self.rename_fields = kwargs.pop("rename_fields", {})
        # self.static_fields = kwargs.pop("static_fields", {})
        static_attrs = kwargs.pop("static_fields", STATIC_ATTRS)
        self.static_attrs = dict(zip(static_attrs, static_attrs))
        reserved_attrs = kwargs.pop("reserved_attrs", RESERVED_ATTRS)
        self.reserved_attrs = dict(zip(reserved_attrs, reserved_attrs))
        # self.timestamp = kwargs.pop("timestamp", False)
        self.logtype        =  kwargs.pop("logtype", None)
        skip_attrs = kwargs.pop("skip_fields", [])
        self._skip_fields = dict(zip(skip_attrs,
                                     skip_attrs))
        # super(JsonFormatter, self).__init__(*args, **kwargs)
        logging.Formatter.__init__(self, *args, **kwargs)
        if not self.json_encoder and not self.json_default:
            self.json_encoder = JsonEncoder

        # self._required_fields = self.parse()

        # self._skip_fields.update(self.reserved_attrs)

    def _str_to_fn(self, fn_as_str):
        """
        If the argument is not a string, return whatever was passed in.
        Parses a string such as package.module.function, imports the module
        and returns the function.

        :param fn_as_str: The string to parse. If not a string, return it.
        """
        if not isinstance(fn_as_str, str):
            return fn_as_str

        path, _, function = fn_as_str.rpartition('.')
        module = importlib.import_module(path)
        return getattr(module, function)

    def parseSpecialFields(self) -> List[str]:
        """
               Parses extra:dict  looking for substitutions

               This method is responsible for returning a list of fields (as strings)
               to include need skip fields.
        """
        pass

    def parse(self) -> List[str]:
        """
        Parses format string looking for substitutions

        This method is responsible for returning a list of fields (as strings)
        to include in all log messages.
        """
        if isinstance(self._style, logging.StringTemplateStyle):
            formatter_style_pattern = re.compile(r'\$\{(.+?)\}', re.IGNORECASE)
        elif isinstance(self._style, logging.StrFormatStyle):
            formatter_style_pattern = re.compile(r'\{(.+?)\}', re.IGNORECASE)
        # PercentStyle is parent class of StringTemplateStyle and StrFormatStyle so
        # it needs to be checked last.
        elif isinstance(self._style, logging.PercentStyle):
            formatter_style_pattern = re.compile(r'%\((.+?)\)', re.IGNORECASE)
        else:
            raise ValueError('Invalid format: %s' % self._fmt)

        if self._fmt:
            return formatter_style_pattern.findall(self._fmt)
        else:
            return []

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            if field in self.rename_fields:
                log_record[self.rename_fields[field]] = record.__dict__.get(field)
            else:
                log_record[field] = record.__dict__.get(field)
        log_record.update(self.static_fields)
        log_record.update(message_dict)
        merge_record_extra(record, log_record, reserved=self._skip_fields)

        if self.timestamp:
            key = self.timestamp if type(self.timestamp) == str else 'timestamp'
            log_record[key] = datetime.fromtimestamp(record.created, tz=timezone.utc)

    def process_log_record(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        return log_record

    def jsonify_log_record(self, log_record):
        """Returns a json string of the log record."""
        return self.json_serializer(log_record,
                                    default=self.json_default,
                                    cls=self.json_encoder,
                                    indent=self.json_indent,
                                    ensure_ascii=self.json_ensure_ascii)

    def serialize_log_record(self, log_record: Dict[str, Any]) -> str:
        """Returns the final representation of the log record."""
        return "%s%s" % (self.prefix, self.jsonify_log_record(log_record))

    def __add_field_in_list_from_record(self, field, event_header: List[str], record: logging.LogRecord,
                                        defaultval='NILVAL'):

        if field in self.static_attrs.keys():
            if field not in self._skip_fields.keys() \
                    and record.__dict__.get(field):
                event_header.append(record.__dict__.get(field))
            else:
                event_header.append(defaultval) if defaultval is not None else None
        else:
            event_header.append(defaultval) if defaultval is not None else None

    def __add_elem_in_dict_from_record(self, field, location: Dict[str, str], record: logging.LogRecord, newfieldname):
        if record.__dict__.get(field)\
                and field not in self._skip_fields.keys():
            location[newfieldname] = record.__dict__.get(field)

    def create_location(self, location: Dict[str, str], record: logging.LogRecord):
        #     'location','filename', 'modulename', 'funcname', 'process', 'processName', 'thread', 'lineno',
        self.__add_elem_in_dict_from_record('filename', location, record,'file_name')
        self.__add_elem_in_dict_from_record('modulename', location, record,'module_name')
        self.__add_elem_in_dict_from_record('funcname', location, record,'function_name')
        self.__add_elem_in_dict_from_record('process', location, record,'process_id')
        self.__add_elem_in_dict_from_record('processName', location, record, 'process_name')
        self.__add_elem_in_dict_from_record('thread', location, record, 'thread_id')
        #self.__add_elem_in_dict_from_record('threadName', location, record, 'thread_name')
        self.__add_elem_in_dict_from_record('lineno', location, record, 'line_id')

    def add_msgid_and_offset_in_event_header(self, event_header: List[str], record: logging.LogRecord):
        if 'msgid' in self.static_attrs.keys():
            if 'msgid' not in self._skip_fields.keys() \
                    and record.__dict__.get('msgid'):
                event_header.append(record.__dict__.get('msgid'))
                if 'msgoffset' in self.static_attrs.keys():
                    if 'msgoffset' not in self._skip_fields.keys() \
                            and record.__dict__.get('msgoffset'):
                        event_header.append(record.__dict__.get('msgoffset'))
                    else:
                        event_header.append('0')

    def create_event_header(self, event_header: List[str], record: logging.LogRecord):

        # 1. version
        if self.static_attrs['version'] == 'version':
            self.static_attrs['version'] = 'V.1.0.0'
        event_header.append(self.static_attrs['version'])
        # 2. asctime
        if not record.__dict__.get('asctime'):
            record.asctime = self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S+08:00")
        self.__add_field_in_list_from_record('asctime', event_header, record)

        # 3. levelname
        self.__add_field_in_list_from_record('levelname', event_header, record)

        # 4. location
        location: Dict[str, str] = {}
        self.create_location(location, record)
        if not record.__dict__.get('location'):
            #record.location = location.__str__()
            #record.location = json.dumps(location)
            record.location = str(location).replace("{","").replace("}","").replace(",",";").replace("'","").replace(": ",":")
        self.__add_field_in_list_from_record('location', event_header, record)

        # 5. logtype
        if not record.__dict__.get('logtype'):
            record.logtype = self.logtype
        self.__add_field_in_list_from_record('logtype', event_header, record)
        # 6. msgid offset
        self.add_msgid_and_offset_in_event_header(event_header, record)

    def __add_field_in_log_from_record(self, field, event_entity: Dict[str, Any], record: logging.LogRecord,
                                       defaultval='NILVAL'):

        if field in self.static_attrs.keys():
            if field not in self._skip_fields.keys() \
                    and record.__dict__.get(field):
                event_entity[field] = (record.__dict__.get(field))
            else:
                event_entity[field] = (defaultval) if defaultval is not None else None
        else:
            event_entity[field] = (defaultval) if defaultval is not None else None

    def __add_custom_field_in_dict_from_record(self, event_entity: Dict[str, Any], record: logging.LogRecord):
        '''
        add custom fields, not in skip and not in reserved
        :param event_entity: dictionary record mimic device`s security event in json
        :param record: logging.LogRecord
        :return: no return val
        '''
        for k, v in record.__dict__.items():
            if k not in self._skip_fields.keys() \
                    and k not in self.reserved_attrs.keys() \
                    and k not in self.static_attrs.keys():
                event_entity[k] = record.__dict__[k]

    def __add_custom_field_in_dict_from_extra_record(self, event_entity: Dict[str, Any], extra_record:Dict[str, Any]):
        '''
        add custom fields, not in skip and not in reserved
        :param event_entity: dictionary record mimic device`s security event in json
        :param record: logging.LogRecord
        :return: no return val
        '''
        for k, v in extra_record.items():
            if k not in self._skip_fields.keys() \
                    and k not in self.reserved_attrs.keys() \
                    and k not in self.static_attrs.keys():
                event_entity[k] = v

    def create_event_entity(self, event_entity: Dict[str, Any], record: logging.LogRecord, extra_record:Dict[str, Any]):

        # 1.  'event_domain', 'event_action', 'object', 'service', 'status', 'subject'
        default_value = 'NILVAL'
        if 'event_domain' in extra_record.keys():
            default_value = extra_record['event_domain']
        self.__add_field_in_log_from_record('event_domain', event_entity, record, default_value)

        if 'event_action' in extra_record.keys():
            default_value = extra_record['event_action']
        self.__add_field_in_log_from_record('event_action', event_entity, record, default_value)

        if 'event_object' in extra_record.keys():
            default_value = extra_record['event_object']
        self.__add_field_in_log_from_record('event_object', event_entity, record, default_value)

        if 'event_service' in extra_record.keys():
            default_value = extra_record['event_service']
        self.__add_field_in_log_from_record('event_service', event_entity, record, default_value)

        if 'event_status' in extra_record.keys():
            default_value = extra_record['event_status']
        self.__add_field_in_log_from_record('event_status', event_entity, record, default_value)

        if 'event_subject' in extra_record.keys():
            default_value = extra_record['event_subject']
        self.__add_field_in_log_from_record('event_subject', event_entity, record, default_value)
        # 2. add custom fields, not in skip and not in reserved
        self.__add_custom_field_in_dict_from_record(event_entity, record)
        if extra_record is not None and extra_record != {}:
            self.__add_custom_field_in_dict_from_extra_record(event_entity, extra_record)

        # 3. add message field
        if 'addition_msg' in extra_record.keys():
            self.__add_field_in_log_from_record('addition_msg', event_entity, record)


    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record and serializes to json"""
        message_dict: Dict[str, Any] = {}
        # FIXME: logging.LogRecord.msg and logging.LogRecord.message in typeshed
        #        are always type of str. We shouldn't need to override that.
        if isinstance(record.msg, dict):  # type: ignore
            message_dict = record.msg  # type: ignore
            record.message = None
        else:
            record.message = record.getMessage()

        log_record: Dict[str, Any]
        log_record = OrderedDict()
        # 1. create event_header
        event_header: List[str] = []
        self.create_event_header(event_header, record)
        log_record['event_header'] = event_header
        # 2. create event_entity
        event_entity: Dict[str, Any]
        event_entity = OrderedDict()
        self.create_event_entity(event_entity, record, message_dict)
        log_record['event_entity'] = event_entity
        #self.create_internal_request(log_record)

        return self.serialize_log_record(log_record)
