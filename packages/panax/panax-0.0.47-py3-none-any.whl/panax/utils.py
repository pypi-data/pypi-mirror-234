import datetime
import jwt
import os, sys


sys.path.append(os.getcwd())
from config import APP_SETTING


def serializer_dict(d):
    data = {}
    for k in d.keys():
        if isinstance(d[k], datetime.datetime):
            data[k] = d[k].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(d[k], datetime.date):
            data[k] = d[k].strftime('%Y-%m-%d')
        else:
            data[k] = d[k]
    return data


def row_to_dict(cursor, row):
    """将返回结果转换为dict"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        if isinstance(row[idx], datetime.datetime):
            d[col[0]] = row[idx].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(row[idx], datetime.date):
            d[col[0]] = row[idx].strftime('%Y-%m-%d')
        else:
            d[col[0]] = row[idx]
    return d


def jwt_encode(user):
    # 把需要用来做权限校验的字段 都加入token中
    # 例如：{ "id": user.id, "role": user.role， "org_id": user.org_id }
    user_dict = user.to_dict()
    data = {}
    for item in APP_SETTING["jwt"]["column"]:
        data[item] = user_dict[item] if item in user_dict else ""
    
    return jwt.encode(data, APP_SETTING["jwt"]["secret"], algorithm='HS256')


def jwt_decode(token):
    return jwt.decode(token, APP_SETTING["jwt"]["secret"], algorithms=['HS256'])
