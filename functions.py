import hashlib
import os

# 加密密码
def md5hex(password):
    if not isinstance(password, str):
        password = str(password)
    password = 'ThisIsPassWord' + password
    password = password.encode('utf-8')
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()

# 创建用户文件夹
def create_user_dir(user_id):
    path = os.getcwd()
    user_path = path + '\\static\\images\\' + str(user_id)
    os.mkdir(user_path)
