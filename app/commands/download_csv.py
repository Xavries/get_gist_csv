import os
from io import BytesIO, StringIO
import datetime
import time
import zipfile
import sqlite3
import csv
from config import DB_TABLES_LIST, DATABASE_PATH


def get_csv_bites(top_dir=f"study-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    top_dir_path = os.path.expanduser(f'~/Documents/{top_dir}')
    csv_bites = BytesIO()

    with zipfile.ZipFile(csv_bites, 'w') as zf:
        zip_info = zipfile.ZipInfo(
            f"study-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        )
        zip_info.date_time = time.localtime(time.time())[:6]

        for table_name in DB_TABLES_LIST:
            c.execute(f"SELECT * FROM {table_name}")
            columns = [column[0] for column in c.description]
            results = []

            for row in c.fetchall():
                results.append(dict(zip(columns, row)))
            csv_io = StringIO()

            writer = csv.DictWriter(csv_io, fieldnames=columns)
            writer.writeheader()
            for line in results:
                writer.writerow(line)
            zf.writestr(f'{table_name}.csv', csv_io.getvalue())

    # Go back to the start of the BytesIO object
    csv_bites.seek(0)

    return csv_bites
