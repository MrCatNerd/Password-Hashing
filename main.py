import hashlib
import sqlite3 as sqlite
import string
import secrets

from settings import *
from os.path import join as join_path

con = sqlite.connect(join_path("data", "users.db"))
cur = con.cursor()
hasher = hashlib.sha1()


def get_random_salt(length: int) -> str:
    return "".join(secrets.choice(string.ascii_letters) for _ in range(length))


def to_hash(
    ctx: str,
    salt: str,
    encoding: str = "utf-8",
) -> str:
    hasher.update((ctx + salt).encode(encoding))

    hash_ctx: str = hasher.hexdigest()

    return hash_ctx


def clear_users(are_you_sure: bool) -> None:
    if not are_you_sure:
        return
    cur.execute("DELETE FROM users;")
    con.commit()


def get_data(username: str) -> tuple:
    data = cur.execute(
        f'SELECT * FROM users WHERE name LIKE "{username}"'
    ).fetchone()  # indexes: [   0:name 1:salt 2:hashed password   ]

    return data


def write_user(username: str, password: str) -> None:
    salt: str = get_random_salt(100)
    password = to_hash(password, salt)

    cur.execute(
        f'INSERT INTO users VALUES("{username}","{salt}","{password}");'
    ).fetchone()  # indexes: [   0:name 1:salt 2:hashed password   ]

    con.commit()


def delete_user(username: str) -> None:
    cur.execute(f'DELETE FROM users WHERE name LIKE "{username}"')
    con.commit()


def try_login(username: str, password: str) -> bool:
    userdata = get_data(username)

    if userdata is None:
        return False

    salt = userdata[1]

    hashedpassword = to_hash(password, salt)  # encoding is always UTF-8

    return hashedpassword == userdata[2]


if __name__ == "__main__":
    uname = input("Gimmmie da username: ")
    password = input("Gimmie da password: ")
    try_login(uname, password)
