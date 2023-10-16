import datetime
import jwt
import os, sys


sys.path.append(os.getcwd())
try:
    from config import APP_SETTING
except Exception:
    APP_SETTING = {}

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
