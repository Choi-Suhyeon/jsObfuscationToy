from random import randrange, choices
from hashlib import sha512


def get_hash_with_random(identifier: str) -> str:
    suffix:   str = ''.join(chr(i) for i in choices(range(0x21, 0x7F), k=randrange(3, 7)))
    hash_val: str = sha512((identifier + suffix).encode("utf-8")).hexdigest()
    
    return f'${hash_val}'


if __name__ == '__main__':
    print(get_hash_with_random('temp'))
    print(get_hash_with_random('temp'))