import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Users 테이블 생성
c.execute('''
    CREATE TABLE users (
        uid TEXT,
        upw TEXT
    )
''')
c.execute("INSERT INTO users VALUES ('admin', 'password')")
c.execute("INSERT INTO users VALUES ('user', '1234')")

# Flag 테이블 생성
c.execute('''
    CREATE TABLE onlyflag (
        svalue TEXT,
        sflag TEXT,
        sclose TEXT
    )
''')
c.execute("INSERT INTO onlyflag VALUES ('hint', 'YBG{crypt0_1s_3asy}', 'end')")

conn.commit()
conn.close()

print("Database initialized successfully.")
