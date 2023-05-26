import pyodbc

# 连接到SQL Server数据库
sql_server_conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=BBS;UID=fgh;PWD=1234')

# SQL Server查询示例
sql_server_cursor = sql_server_conn.cursor()
sql_server_cursor.execute("SELECT * FROM Post Content")
rows = sql_server_cursor.fetchall()
for row in rows:
    print(row)

# 关闭连接
sql_server_conn.close()