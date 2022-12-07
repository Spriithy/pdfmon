import datetime
import hashlib
import sqlite3


def connect_to_db(db):
    # connect to the SQLite database
    conn = sqlite3.connect(db)

    # create the files table if it does not exist
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS files (file_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sha256 TEXT, date_added DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    cur.close()

    return conn


def file_hash(file):
    # compute the SHA-256 hash of the file
    sha256 = hashlib.sha256()
    with open(file, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def is_file_inserted(conn, file):
    # compute the SHA-256 hash of the file
    sha256 = file_hash(file)

    # query the database for the file
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE name = ? OR sha256 = ?",
                (file, sha256))

    # if the file exists in the database, return True
    if cur.fetchone() is not None:
        return True, sha256

    # if the file does not exist in the database, return False
    return False, sha256


def insert_file(conn, file, sha256=None):
    if sha256 is None:
        # compute the SHA-256 hash of the file
        sha256 = file_hash(file)

    values = (file, sha256)

    try:
        # insert the file name and SHA-256 hash into the database
        cur = conn.cursor()
        cur.execute("INSERT INTO files (name, sha256) VALUES (?,?)", values)
        conn.commit()
    except:
        conn.rollback()

    return sha256
