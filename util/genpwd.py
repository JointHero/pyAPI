#!/usr/bin/env python

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == '__main__':
    plain_password = 'bgt56yhn'
    hashed_password = get_password_hash(plain_password)
    print('The hashed password of [ %s ] is [ %s ]' % (plain_password,hashed_password))
    print('Verify again: [ %s ]' % verify_password(plain_password,hashed_password))


"""
print(get_password_hash('admin'))
print(verify_password('admin','$2b$12$NL3bGbzvcULj5Y05Qzhh1e25IuAexUhfSm5IvXe2rms3hVZ605knO'))
print(get_password_hash('passw0rd'))
print(verify_password('passw0rd','$2b$12$bBi.x9FJ/RkRTNH8NSLu9eiNZpgpobZLb4Jj3Zug2GUiiFisft5iC'))
print(get_password_hash('reader'))
print(verify_password('reader','$2b$12$q/YGudr8OHBSOZugpb/7AuuW5yXjmV9lQ5oTc943If16Z.IbkiBGC'))
print(get_password_hash('writer'))
print(verify_password('writer','$2b$12$n0vuGdK1cfUrkyYzUWFtkOjGqY0oroQyEh9QefzBhDok/fmF9XYFO'))
"""