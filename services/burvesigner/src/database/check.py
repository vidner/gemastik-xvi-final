#!/usr/bin/env python3
import sqlite3

db = "database.db"
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT * FROM users")

rows = cur.fetchall()
for row in rows:
    print(row)
