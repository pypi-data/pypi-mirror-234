import hashlib
from peewee import *
from panax.database import BaseModel


# IntegerField, DecimalField, CharField, TextField, DateTimeField, DateField, BooleanField


class Users(BaseModel):
    """用户"""
    username = CharField(max_length=128, unique=True, index=True, help_text="用户名")
    _password = CharField(max_length=128)
    name = CharField(max_length=100)
    role = CharField(max_length=50)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # 建议加入混淆字符串，防止md5碰撞
        self._password = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()

    def verify_password(self, password):
        # 建议加入混淆字符串，防止md5碰撞
        return hashlib.md5(password.encode(encoding='utf-8')).hexdigest() == self._password


MODEL_MAPPING = {
    "users": Users
}
