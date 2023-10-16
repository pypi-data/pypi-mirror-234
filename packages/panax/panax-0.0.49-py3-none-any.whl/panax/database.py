import json, uuid, sys, os, datetime
sys.path.append(os.getcwd())

import peewee as pw

try:
    from config import APP_SETTING
except Exception:
    APP_SETTING = {}


db = pw.MySQLDatabase(
    host=APP_SETTING["db"]["host"] if "db" in APP_SETTING else "",
    port=APP_SETTING["db"]["port"] if "db" in APP_SETTING else "",
    user=APP_SETTING["db"]["user"] if "db" in APP_SETTING else "",
    passwd=APP_SETTING["db"]["passwd"] if "db" in APP_SETTING else "",
    database=APP_SETTING["db"]["database"] if "db" in APP_SETTING else "",
    charset='utf8'
)


def gen_id():
    return uuid.uuid4().hex


class BaseModel(pw.Model):
    id = pw.CharField(primary_key=True, unique=True, max_length=128, default=gen_id, verbose_name="主键ID")
    created = pw.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    is_del = pw.IntegerField(default=0)

    class Meta:
        database = db

    def to_dict(self):
        data = {}
        for k in self.__dict__['__data__'].keys():
            if str(k).startswith('_'):
                continue
            if isinstance(self.__dict__['__data__'][k], datetime.datetime):
                data[k] = self.__dict__['__data__'][k].strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(self.__dict__['__data__'][k], datetime.date):
                data[k] = self.__dict__['__data__'][k].strftime('%Y-%m-%d')
            else:
                data[k] = self.__dict__['__data__'][k]
        return data
