import pyodbc
from datetime import datetime
import re

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


def get_comment_info_by_pid(pid):
    cursor.execute(
        f"SELECT [Comment_Content],[Comment Time],[User ID] from Comment where [Post ID]={pid} ORDER BY [Comment Time]"
    )
    rows = list(cursor.fetchall())
    rows = [process_str(row) for row in rows]
    cursor.execute(
        f"SELECT Content from [Post Content] WHERE [Post ID]={pid} ORDER BY [index] "
    )
    dct = {
        "Comment_Content": [c[0] for c in rows],
        "Comment Time": [c[1] for c in rows],
        "User ID": [c[2] for c in rows]
    }
    return dct


def get_user_info_by_name(name: str):
    cursor.execute(f"SELECT * from [User] where [User Name]='{name}'")
    rows = list(cursor.fetchall())
    columns = get_columns_name("User")
    rows = [process_str(row) for row in rows]
    return pack(rows, columns)


def user_register(info: dict):
    cursor.execute("SELECT COUNT(*) FROM [User]")
    num = list(cursor.fetchall())
    info["User ID"] = num[0][0] + 1
    columns = ",".join([f"[{i}]" for i in info.keys()])
    values = ",".join(
        [str(i) if type(i) != str else f"'{i}'" for i in info.values()])
    cursor.execute(f"INSERT INTO [User] ({columns}) VALUES ({values})")
    cursor.commit()


def insert_item(table, itm: dict):
    columns = ",".join([f"[{i}]" for i in itm.keys()])
    values = ",".join(
        [str(i) if type(i) != str else f"'{i}'" for i in itm.values()])
    cursor.execute(f"INSERT INTO [{table}] ({columns}) VALUES ({values})")
    cursor.commit()


def get_time():
    current_time = datetime.now()
    return current_time.isoformat(sep=' ').split('.')[0]


def add_post(info: dict):
    cursor.execute("SELECT COUNT(*) FROM [Post]")
    num = list(cursor.fetchall())
    info["Post ID"] = num[0][0] + 1
    info["Post time"] = get_time()
    content = info.pop("Content")
    insert_item('Post', info)
    chunks = []
    for i in range(0, len(content), 200):
        chunks.append(content[i:i + 200])
    for i in range(len(chunks)):
        cursor.execute("SELECT COUNT(*) FROM [Post Content]")
        num = list(cursor.fetchall())
        insert_item(
            "Post Content", {
                "Post ID": info["Post ID"],
                "Index": num[0][0] + 1,
                "Content": chunks[i]
            })
    return info["Post ID"]


def add_comment(info):
    cursor.execute("SELECT COUNT(*) FROM [Comment]")
    num = list(cursor.fetchall())
    info["Coment ID"] = num[0][0] + 1
    info['Comment Time'] = get_time()
    insert_item('Comment', info)


def if_follow(uid1, uid2):
    cursor.execute(
        f"SELECT COUNT(*) FROM [Follow] WHERE [Followed ID]={uid1} and [Following ID]={uid2}"
    )
    num = list(cursor.fetchall())
    return num[0][0] != 0


def add_follow(info):
    print(info)
    info["Following Time"] = get_time()
    insert_item('Follow', info)


def remove_special_characters(input_string):
    # 使用正则表达式将特殊字符替换为空字符串
    sanitized_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    return sanitized_string


def close_conn():
    sql_server_conn.close()
