import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
import requests
import json

login_url = "https://libseat.njfu.edu.cn/ic-web/login/user"
public_key_url = "https://libseat.njfu.edu.cn/ic-web/login/publicKey"


def encrpt(password, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()


def login(username, password):
    sess = requests.Session()

    resp = sess.get(public_key_url).text
    resp = json.loads(resp)

    key = resp["data"]["publicKey"]
    public_key = "-----BEGIN PUBLIC KEY-----\n" + key + "\n-----END PUBLIC KEY-----"

    password = password + ";" + resp["data"]["nonceStr"]
    print(password)

    password = encrpt(password, public_key)

    data = {
        "logonName": username,
        "password": password,
        "captcha": "",
        "privacy": True,
        "consoleType": 16,
    }

    print(data)

    login_response = sess.post(login_url, json=data)

    return {"session": sess, "userinfo": login_response.text}