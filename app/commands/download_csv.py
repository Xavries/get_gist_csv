import sqlite3
import csv
from config import DB_TABLES_LIST, DATABASE_PATH


conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()

for table_name in DB_TABLES_LIST:
    c.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in c.description]
    results = []

    for row in c.fetchall():
        results.append(dict(zip(columns, row)))
    with open(f"{table_name}.csv", "w", newline='') as new_file:
        fieldnames = columns
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()
        for line in results:
            writer.writerow(line)

conn.close()
