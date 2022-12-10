import hashlib
import sqlite3 as sqlite
import string
import random

from settings import *
from os.path import join as join_path

con = sqlite.connect(join_path("data", "users.db"))
cur = con.cursor()


def get_random_salt(length: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def to_hash(
    ctx: str, salt: str = None, salt_len: int = None, encoding: str = "utf-8"
) -> str:

    if salt is None:

        if salt_len is None:
            salt_len: int = 10
        else:
            salt_len: int = salt_len

        salt: str = get_random_salt(salt_len)
    else:
        salt: str = salt

    ctx: str = ctx

    encode = encoding

    final: str = bytes(f"{ctx}{salt}", encode)

    hash_ctx: str = hashlib.sha1(final).hexdigest()

    return hash_ctx


def clear_users(are_you_sure: bool) -> None:
    if not are_you_sure:
        return
    cur.execute("DELETE FROM users;")
    con.commit()


def to_hash_and_salt(
    ctx: str, salt: str = None, salt_len: int = None, encoding: str = "utf-8"
) -> tuple[str, str]:

    if salt is None:

        if salt_len is None:
            salt_len: int = 10
        else:
            salt_len: int = salt_len

        salt: str = get_random_salt(salt_len)
    else:
        salt: str = salt

    ctx: str = ctx

    encode = encoding

    final: str = bytes(f"{ctx}{salt}", encode)

    hash_ctx: str = hashlib.sha1(final).hexdigest()

    return (hash_ctx, salt)


def get_data(username: str) -> tuple:

    data = cur.execute(
        f'SELECT * FROM users WHERE name LIKE "{username}"'
    ).fetchone()  # indexes: [   0:name 1:salt 2:hashed password   ]

    return data


def write_user(username: str, password: str) -> None:
    password, salt = to_hash_and_salt(password, None, 100)

    cur.execute(
        f'INSERT INTO users VALUES("{username}","{salt}","{password}");'
    ).fetchone()  # indexes: [   0:name 1:salt 2:hashed password   ]

    con.commit()


def delete_user(username: str) -> bool:
    cur.execute(f'DELETE FROM users WHERE name LIKE "{username}"')
    con.commit()


def try_login(username: str, password: str) -> bool:
    userdata = get_data(username)
    salt = userdata[1]

    hashedpassword = to_hash(password, salt, None)  # encoding is always UTF-8

    return hashedpassword == userdata[2]
