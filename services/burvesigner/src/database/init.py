#!/usr/bin/env python3
import hashlib
import os
import sqlite3
import sys

db = "database.db"


class User:
    def __init__(self, username, password, role):
        self.username: str = username
        self.password: str = password
        self.role: str = role


def main():
    try:
        os.remove(db)
    except:
        pass

    con = sqlite3.connect(db)
    con.execute("CREATE TABLE users (username TEXT, password TEXT, role TEXT)")

    def insert_person(person: User):
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (
                person.username,
                hashlib.sha256(
                    b"gema" + person.password.encode() + b"steg"
                ).hexdigest(),
                person.role,
            ),
        )
        con.commit()

    cur = con.cursor()
    admin = User(sys.argv[1], sys.argv[2], "admin")
    guest = User("guest", "guest", "guest")
    insert_person(admin)
    insert_person(guest)
    con.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <username> <password>")
        exit()
    main()
