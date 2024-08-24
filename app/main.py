import sys

from dataclasses import dataclass

import sqlparse

database_file_path = sys.argv[1]
command = sys.argv[2]

if command == ".dbinfo":
    with open(database_file_path, "rb") as database_file:
        # You can use print statements as follows for debugging, they'll be visible when running tests.
        # print("Logs from your program will appear here!") 

        # Uncomment this to pass the first stage
        database_file.seek(16)  # Skip the first 16 bytes of the header
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        db_desc = database_file.read()
        number_of_tables = db_desc.count(b"CREATE TABLE")
        print(f"database page size: {page_size}")
        print(f"number of tables: {number_of_tables}")
elif command == ".tables":
    with open(database_file_path, "rb") as database_file:
        table_names = []
        db_desc = database_file.read()
        number_of_tables = db_desc.count(b"CREATE TABLE")
        start = 0
        for i in range(number_of_tables):
            idx = db_desc.index(b'CREATE TABLE', start)
            database_file.seek(13+idx)
            idx_space = db_desc.index(b'(', 13+idx)
            name = str(database_file.read(idx_space-13-idx))
            name = name[2:len(name)-1]
            if(name[len(name)-2] == '\\'):
                name = name[:len(name)-2]
            table_names.append(name)
            start = idx+1
        # table_names = []
        # db_main_file_string = ""
        # print(database_file)
        # for db_file_bytes_stream in database_file:
        #     db_file_bytes_stream
        # print(db_main_file_string)
        for name in table_names:
            print(name, end=" ")
        print()
else:
    print(f"Invalid command: {command}")
