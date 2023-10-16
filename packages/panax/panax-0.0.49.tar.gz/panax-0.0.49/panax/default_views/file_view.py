import json, time, datetime, sys, os, uuid

sys.path.append(os.getcwd())
try:
    from config import APP_SETTING
except Exception:
    APP_SETTING = {}

def file_file(request, operation):
    field_storage = request.FILES.get("file")

    allow_file_type = APP_SETTING["file"][operation]
    file_type = field_storage.filename.split('.')[-1]
    if str(file_type).lower() not in allow_file_type:
        return {
            "code": 400,
            "msg": "File Type Error!"
        }

    file_name = uuid.uuid4().hex + '.' + file_type

    root_path = os.getcwd()
    dt_path = datetime.datetime.now().strftime("%Y%m%d")
    full_path = os.path.join(root_path, 'static/files', dt_path)

    if not os.path.isdir(full_path):
        os.makedirs(full_path)

    with open(os.path.join(full_path, file_name), "wb") as f:
        f.write(field_storage.value)

    return {
        "code": 200,
        "data": '/static/files/' + dt_path + '/' + file_name,
        "msg": "Success"
    }