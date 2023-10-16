# 全局配置


APP_SETTING = {
    # 数据库链接
    "db": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "passwd": "",
        "database": ""
    },
    # jwt 配置
    "jwt": {
        # jwt中 包含的用户列, 至少包含["id", "username", "name", "role"]，可以按需增加其他列
        "column": ["id", "username", "name", "role"],
        # jwt加密解密使用的密钥串
        "secret": "123!@#"
    },
    "file": {
        # 配置文件上传接口 可以上传的文件类型，调用方式：/api/file/image, /api/file/video
        "image": ["jpg", "jpeg", "bmp", "gif", "png"],
        "video": ["mp4"],
        "doc": ["doc", "docx"],
        "pdf": ["pdf"],
        "txt": ["txt"],
    },
    "request": {
        "secret": True
    }
}

# anymore 所有用户，包含匿名用户
# all 所有用户（登录）
# 角色
# 用户字段__表字段

# 权限配置
API_PERMISSION = {
    "__default": {
        "list": ["all"],
        "get": ["all"],
        "post": ["all"],
        "put": ["all"],
        "delete": ["all"],
        "drop": [],
        "__other": []
    },
    "file": {
        "image": ["anymore"],
        "video": ["anymore"],
        "doc": ["anymore"],
        "pdf": ["anymore"],
        "txt": ["anymore"],
    },
    "users": {
        "post": ["admin", "teacher"],
        "put": ["admin", "teacher", "id__id"],
        "delete": ["admin"],
        "login": ["anymore"]
    },
    # 权限示例，并没有创建experiment表
    "experiment": {
        "post": ["admin", "teacher"],
        # 管理员、 教师、 负责人、 所属组织的用户、 教学团队中的用户
        "put": ["admin", "teacher", "id__master_id", "org_id__org_id", "org_id__team_id"],
        "delete": ["admin", ],
        "pub": ["admin", ],
        "cancel": ["admin", ]
    }
}
