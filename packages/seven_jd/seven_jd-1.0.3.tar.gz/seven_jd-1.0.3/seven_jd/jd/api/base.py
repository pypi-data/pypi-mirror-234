# -*- coding: utf-8 -*-
import time
import pytz
import datetime
import json
import itertools
import mimetypes
import hashlib
import requests
from urllib import parse
from seven_jd import jd

P_APPKEY = "app_key"
P_API = "method"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_JSON_PARAM_KEY = "360buy_param_json"

P_CODE = 'code'
P_SUB_CODE = 'sub_code'
P_MSG = 'msg'
P_SUB_MSG = 'sub_msg'

N_REST = '/routerjson'


def sign(secret, parameters):
    if hasattr(parameters, "items"):
        keys = parameters.keys()
        # keys.sort()
        keys = sorted(keys)
        parameters = "%s%s%s" % (secret, str().join('%s%s' % (key, parameters[key]) for key in keys), secret)
    return hashlib.md5(parameters.encode('utf-8')).hexdigest().upper()


def mixStr(pstr):
    if (isinstance(pstr, str)):
        return pstr
    elif (isinstance(pstr, bytes)):
        return pstr.encode('utf-8')
    else:
        return str(pstr)


class FileItem(object):
    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""
    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = "PYTHON_SDK_BOUNDARY"
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, str(value)))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((mixStr(fieldname), mixStr(filename), mixStr(mimetype), mixStr(body)))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend([
            part_boundary,
            'Content-Disposition: form-data; name="%s"' % name,
            'Content-Type: text/plain; charset=UTF-8',
            '',
            value,
        ] for name, value in self.form_fields)

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
             'Content-Type: %s' % content_type,
             'Content-Transfer-Encoding: binary',
             '',
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.extend(('--' + self.boundary + '--', ''))
        return '\r\n'.join(flattened)


class JdException(Exception):
    def __init__(self):
        self.errorcode = None
        self.message = None
        self.subcode = None
        self.submsg = None
        self.application_host = None
        self.service_host = None

    def __str__(self, *args, **kwargs):
        sb = "errorcode=" + mixStr(self.errorcode) + \
             " message=" + mixStr(self.message) + \
             " subcode=" + mixStr(self.subcode) + \
             " submsg=" + mixStr(self.submsg) + \
             " application_host=" + mixStr(self.application_host) + \
             " service_host=" + mixStr(self.service_host)
        return sb


class RequestException(Exception):
    pass


class RestApi(object):
    def __init__(self, domain='gw.api.360buy.net', port=80):
        self.__domain = domain
        self.__port = port
        self.__httpmethod = "POST"
        if (jd.getDefaultAppInfo()):
            self.__app_key = jd.getDefaultAppInfo().appkey
            self.__secret = jd.getDefaultAppInfo().secret

    def get_request_header(self):
        return {
            'Content-type': 'application/x-www-form-urlencoded',
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

    def set_app_info(self, appinfo):
        self.__app_key = appinfo.appkey
        self.__secret = appinfo.secret

    def getapiname(self):
        return ""

    def get_version(self):
        return '2.0'

    def getMultipartParas(self):
        return []

    def getTranslateParas(self):
        return {}

    def _check_requst(self):
        pass

    def process_with_url_before_request(self, url):
        pass

    def getResponse(self, accessToken=None, version=None, timeout=30, ssl=False):
        hour_diff = time.localtime()[3] - datetime.datetime.now(tz=pytz.timezone('UTC')).hour
        if 0 < hour_diff < 10:
            zone_str = '+0' + str(hour_diff) + '00'
        elif hour_diff > 10:
            zone_str = '+' + str(hour_diff) + '00'
        elif 0 > hour_diff > -10:
            zone_str = '-0' + str(-hour_diff) + '00'
        else:
            zone_str = '-' + str(-hour_diff) + '00'
        time_str = time.strftime("%Y-%m-%d %H:%M:%S.000", time.localtime()) + zone_str
        sys_parameters = {
            P_APPKEY: self.__app_key,
            P_VERSION: self.get_version() if version is None else version,
            P_API: self.getapiname(),
            P_TIMESTAMP: time_str,
        }
        if accessToken is not None:
            sys_parameters[P_ACCESS_TOKEN] = accessToken
        if not self.__domain.startswith('http'):
            url = 'https://' if ssl else 'http://'
            url += self.__domain
        else:
            url = self.__domain
        if not url.endswith(N_REST) and not url.endswith(N_REST + '/'):
            url = url[:-1] if url.endswith('/') else url
            url = url + N_REST
        self.process_with_url_before_request(url)
        application_parameter = self.getApplicationParameters()
        sys_parameters[P_JSON_PARAM_KEY] = json.dumps(application_parameter, ensure_ascii=False, default=lambda value: value.__dict__)
        sys_parameters[P_SIGN] = sign(self.__secret, sys_parameters)
        if self.__httpmethod == 'POST':
            return requests.post(url, data=sys_parameters, timeout=timeout).json()
        url = url + "?" + parse.urlencode(sys_parameters)
        return requests.get(url, timeout=timeout).json()

    def getApplicationParameters(self):
        application_parameter = {}
        for key, value in self.__dict__.items():
            # for key, value in self.__dict__.iteritems():
            if (not key.startswith("__") and key not in self.getMultipartParas() and not key.startswith("_RestApi__") and value is not None):
                if key.startswith("_"):
                    application_parameter[key[1:]] = value
                else:
                    application_parameter[key] = value
        translate_parameter = self.getTranslateParas()
        # for key, value in application_parameter.iteritems():
        for key in application_parameter:
            if key in translate_parameter:
                application_parameter[translate_parameter[key]] = application_parameter[key]
                del application_parameter[key]
        return application_parameter