import sys, os

sys.path.append(os.getcwd())
from config import APP_SETTING

import cgi
import threading
from urllib.parse import parse_qs
from panax.utils.jwt_helper import jwt_decode

from panax.utils.request_helper import request_process


class Request(threading.local):
    def bind(self, environ):
        self._environ = environ

        # GET
        query_string = self._environ.get('QUERY_STRING', '')
        raw_dict = parse_qs(query_string, keep_blank_values=1)
        self._GET = {}
        for key, value in raw_dict.items():
            if len(value) == 1:
                self._GET[key] = value[0]
            else:
                self._GET[key] = value

        # POST FILES
        raw_data = cgi.FieldStorage(fp=self._environ['wsgi.input'], environ=self._environ)
        self._POST = {}
        self._FILES = {}
        if raw_data.list:
            for key in raw_data:
                if raw_data[key].filename:
                    self._FILES[key] = raw_data[key]
                elif isinstance(raw_data[key], list):
                    self._POST[key] = [v.value for v in raw_data[key]]
                else:
                    self._POST[key] = raw_data[key].value
        
        self._headers = None
        self._user = None

        if APP_SETTING["request"]["secret"]:
            self._POST = request_process(self._POST)

    @property
    def path(self):
        return '/' + self._environ.get('PATH_INFO', '').lstrip('/')

    @property
    def GET(self):
        return self._GET

    @property
    def POST(self):
        return self._POST

    @property
    def FILES(self):
        return self._FILES

    @property
    def method(self):
        return self._environ.get('REQUEST_METHOD', 'GET').upper()

    @property
    def headers(self):
        if self._headers == None:
            self._headers = {}
            for key, value in dict(self._environ).items():
                if str(key).startswith("HTTP_"):
                    self._headers[str(key).replace("HTTP_", "")] = value
        return self._headers

    @property
    def user(self):
        if self._user == None:
            token = self.headers["AUTHORIZATION"] if "AUTHORIZATION" in self.headers and self.headers["AUTHORIZATION"] else ""
            if token:
                self._user = jwt_decode(token)
            else:
                self._user = {
                    "id": "",
                    "username": "anymore",
                    "name": "匿名用户",
                    "role": "anymore"
                }
                for item in APP_SETTING["jwt"]["column"]:
                    if item not in self._user:
                        self._user[item] = ""
        return self._user
