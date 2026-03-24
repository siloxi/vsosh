from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    time_cost=2,     
    memory_cost=2**16,
    parallelism=2,
    hash_len=32,   
)

def get_hash(password):
    return ph.hash(password)

def check_hash(hashed, password):
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False
