import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA


public_key = b'-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJS5j93Uijwvd9oT9caNQY6Dmfdml5AV\nSopG7IQ+iWa+WDMVI2TJoXqG4AA4rl7L2SQh8w1W3dwU8ztuIutVffcCAwEAAQ==\n-----END PUBLIC KEY-----'
private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAlLmP3dSKPC932hP1\nxo1BjoOZ92aXkBVKikbshD6JZr5YMxUjZMmheobgADiuXsvZJCHzDVbd3BTzO24i\n61V99wIDAQABAkAtvGrrswLXw1k+LUk1yBbS9tGQbXJKkuGbaHgvqvOiLoeNQc4U\nWPVhrtITxtnB5QdZ4D96zUdgNdj8ihwTPrvBAiEA96Ui0F8q/vN8mziO3WCfef4T\neF7eHpciZGIirl9fjpECIQCZvhIWlT4tiDtG2wJ7zXAO/IAFBT5QlsJtSOHd6CsY\nBwIhAL8T7MvIUn2LU77Uoe8QKZzQPSeoU0xZItE/ozDWJ/3xAiBOwPl9Dfgq1MUg\nl6GfD25ejuN5LuVr3L49wv7IcFxa0wIgdjlX7KyKN6O2h+wlzbKT9RONlKs3geUM\nKxRcu4K/oUo=\n-----END RSA PRIVATE KEY-----'



# ------------------------生成密钥对------------------------
def create_rsa_pair(is_save=False):
    '''
    创建rsa公钥私钥对
    :param is_save: default:False
    :return: public_key, private_key
    '''
    f = RSA.generate(2048)
    private_key = f.exportKey("PEM")  # 生成私钥
    public_key = f.publickey().exportKey()  # 生成公钥
    if is_save:
        with open("crypto_private_key.pem", "wb") as f:
            f.write(private_key)
        with open("crypto_public_key.pem", "wb") as f:
            f.write(public_key)
    return public_key, private_key


def read_public_key(file_path="crypto_public_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


def read_private_key(file_path="crypto_private_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


# ------------------------加密------------------------
def encryption(text: str):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


# ------------------------解密------------------------
def decryption(text_encrypted_base64: str):
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted


if __name__ == '__main__':
    # 生成密钥对
    # create_rsa_pair(is_save=True)
    # public_key = read_public_key()
    # private_key = read_private_key()
    # public_key, private_key = create_rsa_pair(is_save=False)
    # print(public_key)
    # print(private_key)

    # python 中
    # public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu7cayQsL1ntHMyQX8zyS\n4gzsYjrP4t6oDK/WK5Iq4zLyYqE/oV7AEr0yhh2fJAe5FkFvVbxZuDXGb1I/5r0J\nNjx1DArABVwUZWXrVLjxbKmpVCiYkJJecZclACKk/JWMhZYeZEGs1BWrex3RvpLQ\nXKrSEdrYV8UEVDnAjkOUiRO5DalH+dHt3qvkGr751P7fxVMbIifC7JzdFgW+YMKJ\ntW6YxZkk7nqxvgBV7Y8ieDUQozPOCP7TzM2Qvx0LLLm0hM9WcJqrBXmSrxjA4BCC\n6SbsqxjU3OL8rNQTS+kgAhG4akQQe0Q8xHQagQCOE7BbWZd7eqMkiHAkHkOgfevo\nCQIDAQAB\n-----END PUBLIC KEY-----'
    # private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAu7cayQsL1ntHMyQX8zyS4gzsYjrP4t6oDK/WK5Iq4zLyYqE/\noV7AEr0yhh2fJAe5FkFvVbxZuDXGb1I/5r0JNjx1DArABVwUZWXrVLjxbKmpVCiY\nkJJecZclACKk/JWMhZYeZEGs1BWrex3RvpLQXKrSEdrYV8UEVDnAjkOUiRO5DalH\n+dHt3qvkGr751P7fxVMbIifC7JzdFgW+YMKJtW6YxZkk7nqxvgBV7Y8ieDUQozPO\nCP7TzM2Qvx0LLLm0hM9WcJqrBXmSrxjA4BCC6SbsqxjU3OL8rNQTS+kgAhG4akQQ\ne0Q8xHQagQCOE7BbWZd7eqMkiHAkHkOgfevoCQIDAQABAoIBABANUybMgUVk0tya\nckrcS/I1KTSoM1VC9YtqMO4WaID3vxb0k4ik3ddsYujpmQ1/dJIk49Soz+JLBO5J\nkgnU8ff3mQm/1JZQvrTCD6r1yr1gT8jQ1OUOAzIC+wjFLack0bitsukfXZxgQwL6\n9I/vpY47FE4vEO+Gez2Jl8ACou3Kwqn+ceHd+gT6AZ81jpWQ+g8Ya3ydjxQ+ouGs\nhmNFeOT/wI4QanxMG7sLM2CA2iXVqQyCNKHA9QXdaPgxeCYLJRjLlRRVkqiFOSNn\n/jmXa3dn5GBV4glv/bJMgVHUWZvrntAddfMxF7UFWdLcNdW7TKENIuNaR/Ctjj1a\naHnyviECgYEAznuVzr2ede/xVGe9rB/oM6zX7nNal+86S7HAQEyDQ7/4pEGWkOuv\nY7vZFR9cmUfZrA5UGwRUO1MAGBcKcM94K7U2+gRmxunQmkqiJmxLrKTDSju3D22I\nSemShQIWdIJ5Oy7D1NPwsEXHqNdKQTpxFMxgFILsvHbK67aEPAxGsjECgYEA6LtX\ntpGSP1la8B57JuWb5CE60dMOu20hYJplCA1g90EQtCxCx1J9SFwrDFVF4r8mGf2M\naFKOt+lYCV1mlK00av8MUCN/Ixt+gPrhWcEthUYTCvN5vGvkjaKBiT+ST2VddeDw\notwYhiD1j7L17zVDO7WkZYSO0ruS4jwd6UltBVkCgYAGiM6y3jlXjiJbA3VzLwdQ\nK1YiC7CAQmfb4WIuJr24tSiPOiwjpfHE/Drgej+Z8jYnRcTPnhF0VyoXmRMRgt9Q\nsslsnBsMjHW3jEkZYi/65LPxc3ZVnKfFfwjOAMTpJv/jKZW09IgXa/3nj/ifm9Pc\nTqNzwrjvNesyDnKc296Y4QKBgQCl3ugb+dKHDfNvUfop9dnOlRRr+YX1dUklpcS+\nIXLrplb2YtlRYGxkRzRzPM9rVRsdyQTqUXTghRG20vfKnUvPummXMEVryyu1V5mH\nM9RyuUfXNUKdVTR28cxq+oEXz0H2QtSe7kkYR6NcwIrh60843jQGGp0EeqWsUnZr\nD2cBOQKBgCkXY2QdMBb6mqGLuZnN60YFGuPjTW8skQNHOhIQErLC0bRfbqAWIts4\nPs2cn3o1aADCGfWxXKdfaJQ8VEQu2TgFCQCVRbUzDgusZyrZdvWxnrj/egrwrCx3\nNZgS1BdNZRzbIf1kD2Td0cQ5iCR2hxgL6Cut91YXTnJVC/iz8wEJ\n-----END RSA PRIVATE KEY-----'

    # js中
    # private_key = b'-----BEGIN RSA PRIVATE KEY-----MIIEowIBAAKCAQEAu7cayQsL1ntHMyQX8zyS4gzsYjrP4t6oDK/WK5Iq4zLyYqE/oV7AEr0yhh2fJAe5FkFvVbxZuDXGb1I/5r0JNjx1DArABVwUZWXrVLjxbKmpVCiYkJJecZclACKk/JWMhZYeZEGs1BWrex3RvpLQXKrSEdrYV8UEVDnAjkOUiRO5DalH+dHt3qvkGr751P7fxVMbIifC7JzdFgW+YMKJtW6YxZkk7nqxvgBV7Y8ieDUQozPOCP7TzM2Qvx0LLLm0hM9WcJqrBXmSrxjA4BCC6SbsqxjU3OL8rNQTS+kgAhG4akQQe0Q8xHQagQCOE7BbWZd7eqMkiHAkHkOgfevoCQIDAQABAoIBABANUybMgUVk0tyackrcS/I1KTSoM1VC9YtqMO4WaID3vxb0k4ik3ddsYujpmQ1/dJIk49Soz+JLBO5JkgnU8ff3mQm/1JZQvrTCD6r1yr1gT8jQ1OUOAzIC+wjFLack0bitsukfXZxgQwL69I/vpY47FE4vEO+Gez2Jl8ACou3Kwqn+ceHd+gT6AZ81jpWQ+g8Ya3ydjxQ+ouGshmNFeOT/wI4QanxMG7sLM2CA2iXVqQyCNKHA9QXdaPgxeCYLJRjLlRRVkqiFOSNn/jmXa3dn5GBV4glv/bJMgVHUWZvrntAddfMxF7UFWdLcNdW7TKENIuNaR/Ctjj1aaHnyviECgYEAznuVzr2ede/xVGe9rB/oM6zX7nNal+86S7HAQEyDQ7/4pEGWkOuvY7vZFR9cmUfZrA5UGwRUO1MAGBcKcM94K7U2+gRmxunQmkqiJmxLrKTDSju3D22ISemShQIWdIJ5Oy7D1NPwsEXHqNdKQTpxFMxgFILsvHbK67aEPAxGsjECgYEA6LtXtpGSP1la8B57JuWb5CE60dMOu20hYJplCA1g90EQtCxCx1J9SFwrDFVF4r8mGf2MaFKOt+lYCV1mlK00av8MUCN/Ixt+gPrhWcEthUYTCvN5vGvkjaKBiT+ST2VddeDwotwYhiD1j7L17zVDO7WkZYSO0ruS4jwd6UltBVkCgYAGiM6y3jlXjiJbA3VzLwdQK1YiC7CAQmfb4WIuJr24tSiPOiwjpfHE/Drgej+Z8jYnRcTPnhF0VyoXmRMRgt9QsslsnBsMjHW3jEkZYi/65LPxc3ZVnKfFfwjOAMTpJv/jKZW09IgXa/3nj/ifm9PcTqNzwrjvNesyDnKc296Y4QKBgQCl3ugb+dKHDfNvUfop9dnOlRRr+YX1dUklpcS+IXLrplb2YtlRYGxkRzRzPM9rVRsdyQTqUXTghRG20vfKnUvPummXMEVryyu1V5mHM9RyuUfXNUKdVTR28cxq+oEXz0H2QtSe7kkYR6NcwIrh60843jQGGp0EeqWsUnZrD2cBOQKBgCkXY2QdMBb6mqGLuZnN60YFGuPjTW8skQNHOhIQErLC0bRfbqAWIts4Ps2cn3o1aADCGfWxXKdfaJQ8VEQu2TgFCQCVRbUzDgusZyrZdvWxnrj/egrwrCx3NZgS1BdNZRzbIf1kD2Td0cQ5iCR2hxgL6Cut91YXTnJVC/iz8wEJ-----END RSA PRIVATE KEY-----'
    # public_key = b'-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu7cayQsL1ntHMyQX8zyS4gzsYjrP4t6oDK/WK5Iq4zLyYqE/oV7AEr0yhh2fJAe5FkFvVbxZuDXGb1I/5r0JNjx1DArABVwUZWXrVLjxbKmpVCiYkJJecZclACKk/JWMhZYeZEGs1BWrex3RvpLQXKrSEdrYV8UEVDnAjkOUiRO5DalH+dHt3qvkGr751P7fxVMbIifC7JzdFgW+YMKJtW6YxZkk7nqxvgBV7Y8ieDUQozPOCP7TzM2Qvx0LLLm0hM9WcJqrBXmSrxjA4BCC6SbsqxjU3OL8rNQTS+kgAhG4akQQe0Q8xHQagQCOE7BbWZd7eqMkiHAkHkOgfevoCQIDAQAB-----END PUBLIC KEY-----'

    # 加密
    text = '123456'
    text_encrypted_base64 = encryption(text)
    print('密文：', text_encrypted_base64)

    # 解密
    text_decrypted = decryption(text_encrypted_base64)
    print('明文：', text_decrypted)
