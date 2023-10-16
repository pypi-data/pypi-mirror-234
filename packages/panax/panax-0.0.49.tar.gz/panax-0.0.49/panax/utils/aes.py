import base64
import ast
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def encrypt(text, key, iv):
    # 加密函数
    mode = AES.MODE_CBC
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return str(base64.b64encode(b2a_hex(cipher_text)), encoding='utf-8')


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text, key, iv):
    text = base64.b64decode(text)
    key = str(key).encode('utf-8')
    iv = str(iv).encode('utf-8')
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    # plain_text = cryptos.decrypt(a2b_hex(text))
    plain_text = cryptos.decrypt(text)
    # return bytes.decode(plain_text).rstrip('\0')
    data = bytes.decode(plain_text)
    return data[0: data.rfind("}") + 1]


if __name__ == '__main__':
    e = encrypt("""{"username":"test"}""")  # 加密
    d = decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)
    # print(type(d))
    print(ast.literal_eval(d)['username'])
