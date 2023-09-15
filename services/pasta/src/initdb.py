#!/usr/bin/env python3
import hashlib
import os
import sqlite3
import sys

db = "src/pasta.db"


class User:
    def __init__(self, username, password, role):
        self.username: str = username
        self.password: str = password
        self.role: str = role


def main():
    try:
        os.remove(db)
    except BaseException:
        pass

    con = sqlite3.connect(db)
    con.execute("create table users(username varchar(200) primary key,password varchar(64),role varchar(30) default 'user')")

    def insert_person(person: User):
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (
                person.username,
                hashlib.sha256(
                    person.password.encode()
                ).hexdigest(),
                person.role,
            ),
        )
        con.commit()

    cur = con.cursor()
    admin = User(sys.argv[1], sys.argv[2], "admin")
    insert_person(admin)
    con.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <username> <password>")
        exit()
    main()
