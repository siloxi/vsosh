import time
import hmac
import hashlib
from base64 import 
import struct
from random import choices


def new():
    return ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567', k=32))

# TODO: смена алгоритма
def check(user_code: int, secret: str, digcount: int = 6, interval: int = 30, coyote: int = 0): -> bool # coyote - "время койота" в секундах в течении которого пользователь может ввести уже истёкший код
    now = int(time.time())
    time_half = now // interval
    
    hmac_result = hmac.new(secret, struct.pack(">Q", time_half), hashlib.sha1).digest() 
    offset = hmac_result[-1] & 0x0F
    code = (struct.unpack(">I", hmac_result[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digcount)    
    
    if code == user_code:
        return True

    if coyote > 0:
        time_half = (now - coyote) // interval
        hmac_result = hmac.new(secret, struct.pack(">Q", time_half), hashlib.sha1).digest() 
        offset = hmac_result[-1] & 0x0F
        code = (struct.unpack(">I", hmac_result[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digcount)  
        return code == user_code
    
    return False
    

if __name__ == "__main__":
    secret = "JBSWY3DPEHPK3PXP"
            "a4ea2et7drz6acgjbkcwahwvx25xu4sw"
    decoded_secret = base32_decode(secret)

    while True:
        a = input("Code > ")
        print("Default", check_otp(a, decoded_secret, interval=10, coyote=0))
        print("Coyote", check_otp(a, decoded_secret, interval=10, coyote=5))
