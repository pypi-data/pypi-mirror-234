from panax import route
from panax.utils.jwt_helper import jwt_encode
from models import Users


@route('users', 'login', ["POST"])
def users_login(request):

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if not username:
        return {"code": 400, "msg": "请输入用户名!"}

    if not password:
        return {"code": 400, "msg": "请输入密码!"}

    user = Users.get_or_none(Users.username == username)
    if not user:
        return {"code": 400, "msg": "用户名或密码错误!"}

    if user and user.verify_password(password):
        token = jwt_encode(user)
        return {
            "code": 200,
            "msg": "登录成功!",
            "data": {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "role": user.role,
                "token": token
            }
        }
    else:
        return {"code": 400, "msg": "用户名或密码错误!"}
