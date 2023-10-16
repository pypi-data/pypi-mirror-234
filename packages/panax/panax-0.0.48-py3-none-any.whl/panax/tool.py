import argparse

import sys
import os
import shutil
sys.path.append(os.getcwd())

from panax.database import db
try:
    from config import APP_SETTING
    import models
except:
    APP_SETTING = {}
    models = None

from peewee_migrate import Router


def init():
    print("==init==")
    old_path = os.path.abspath(__file__).replace("panax/tool.py", "panax/template")
    new_path = os.getcwd()
    shutil.copytree(old_path + "/", new_path + "/", dirs_exist_ok=True)
    print("==finished==")


def migrate():
    print("==migrateing==")

    db.connect()

    router = Router(db, ignore="basemodel")
    router.create(auto=models)
    router.run()

    db.close()

    print("==migrate finished==")


def create_super():
    model = models.Users.create(**{
        "username": "admin",
        "password": "Aa123456",
        "name": "管理员",
        "role": "admin",
    })
    print("==finished==")


# def upgrade():
#     print("==upgrade==")
#     repo = os.path.join(os.getcwd(), 'db_migrate')
#     if not os.path.exists(repo):
#         print("Repo Not Found!")
#
#     api.upgrade(APP_SETTING["connection"], repo)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-f", help="")
    parser.add_argument("exec", help="参数: [init, migrate, upgrade]")

    # 解析
    args = parser.parse_args()
    exec = args.exec
    # f = args.f

    if exec == "init":
        init()
    elif exec == "migrate":
        migrate()
    elif exec == "create_super":
        create_super()
    # elif exec == "upgrade":
    #     upgrade()
    else:
        print("参数错误")


if __name__ == '__main__':
    main()
