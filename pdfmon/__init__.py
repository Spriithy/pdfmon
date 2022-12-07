import os
import sys
import time

from .pdf import *
from .db import *


def monitor_directory(directory, words):
    # check if the directory exists
    if not os.path.isdir(directory):
        print("Error: The specified directory does not exist.")
        sys.exit(1)

    while True:
        # connect to the SQLite database
        conn = connect_to_db("pdfmon.db")

        # get a list of all PDF files in the directory
        files = [
            os.path.join(root, name) for root, _, files in os.walk(directory)
            for name in files if name.endswith((".pdf", ".PDF"))
        ]

        for file in files:
            # if the file is not already in the database, add it
            file_inserted, file_sha256 = is_file_inserted(conn, file)
            if not file_inserted:
                insert_file(conn, file, file_sha256)
                print(f"{file_sha256} - '{file}' was added to the database.")

                # read the file and check if any of the words are present
                text = read_pdf(file).upper()
                for word in [w.upper() for w in words]:
                    if word in text:
                        print(
                            f"The word '{word}' was found in the file '{file}'."
                        )
            else:
                print(
                    f"Warning: {file_sha256} is already present in database.")

        # close the database connection
        conn.close()

        # and wait for next cycle
        time.sleep(10)
