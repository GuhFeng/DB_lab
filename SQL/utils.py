import pyodbc
import datetime
from decimal import Decimal

sql_server_conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=BBS;UID=fgh;PWD=1234")
cursor = sql_server_conn.cursor()


def process_str(row):
    return [str(i) for i in row]


def pack(rows, columns):
    return {
        columns[i]: [rows[j][i] for j in range(len(rows))]
        for i in range(len(columns))
    }


def get_columns_name(table):
    cursor.execute(
        f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
    )
    rows = list(cursor.fetchall())
    rows = [str(i).split("'")[1] for i in rows]
    return rows


def get_user_info_by_uid(uid):
    cursor.execute(f"SELECT * from [User] where [User ID]={uid}")
    rows = list(cursor.fetchall())
    columns = get_columns_name("User")
    rows = [process_str(row) for row in rows]
    return pack(rows, columns)


def get_post_info_by_pid(pid):
    cursor.execute(f"SELECT * from [Post] where [Post ID]={pid}")
    rows = list(cursor.fetchall())
    rows = [process_str(row) for row in rows]
    columns = get_columns_name("Post")
    cursor.execute(
        f"SELECT Content from [Post Content] WHERE [Post ID]={pid} ORDER BY [index] "
    )
    dct = pack(rows, columns)
    dct["Content"] = ["".join([c[0] for c in cursor.fetchall()])]
    return dct


def get_recent_posts(num):
    cursor.execute(
        f"SELECT TOP {num} [Post ID],[Post time] from [Post] ORDER BY [Post time] DESC"
    )
    rows = list(cursor.fetchall())
    columns = get_columns_name("Post")
    dct = {c: [] for c in columns}
    dct["Content"] = []
    for i in [int(row[0]) for row in rows]:
        for k, v in get_post_info_by_pid(i).items():
            dct[k] += v
    return dct


def get_following(uid):
    cursor.execute(
        f"SELECT [Followed ID],[Following Time] from [Follow] where [Following ID]={uid} ORDER BY [Following Time]"
    )
    rows = list(cursor.fetchall())
    columns = get_columns_name("User")
    dct = {c: [] for c in columns}
    dct["Following Time"] = [row[1] for row in rows]
    for i in [int((row[0])) for row in rows]:
        for k, v in get_user_info_by_uid(i).items():
            dct[k] += v
    return dct


def close_conn():
    sql_server_conn.close()