

import json
from panax.utils.rsa import encryption as rsa_en, decryption as rsa_de
from panax.utils.aes import encrypt as aes_en, decrypt as aes_de


def request_process(r):
    d = r.get('d', None)
    k = r.get('k', None)
    t = r.get('t', None)
    if not d or not k or not t:
        return {}
    key = rsa_de(k)
    iv = str(t)[5:] + str(t)[0:8]
    data = aes_de(d, key, iv)
    res = json.loads(data) if data else {}
    return res
