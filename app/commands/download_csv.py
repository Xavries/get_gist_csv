import sqlite3
import csv
import os.path

from config import DB_TABLES_LIST


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database-dev-def.sqlite3")
conn = sqlite3.connect(db_path)
c = conn.cursor()

for table_name in DB_TABLES_LIST:
    c.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in c.description]
    results = []

    for row in c.fetchall():
        results.append(dict(zip(columns, row)))
    with open(f"{table_name}.csv", "w", newline='') as new_file:
        fieldnames = columns
        writer = csv.DictWriter(new_file,fieldnames=fieldnames)
        writer.writeheader()
        for line in results:
            writer.writerow(line)

conn.close()