#!/usr/bin/env python3
''' encrypt password module '''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' hash password '''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' checks if password matches hash '''
    return bcrypt.checkpw(password.encode(), hashed_password)
