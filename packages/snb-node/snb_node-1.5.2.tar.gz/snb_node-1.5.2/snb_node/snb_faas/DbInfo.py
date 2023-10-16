import sqlite3
import sys

if sys.platform == 'win32':
    con = sqlite3.connect('snb_node_apscheduler.sqlite')
else:
    con = sqlite3.connect('/home/snb_node_apscheduler.sqlite')



cur = con.cursor()
sql = """create table tb_snb_faas_data(
id varchar(64),
module varchar(64),
code_str TEXT,
status int(3),
create_time datetime,
nb_uid varchar(64),
ws_uid varchar(64),
nb_name varchar(64),
cell_uid varchar(64),
PRIMARY KEY (id) ON CONFLICT REPLACE,
CONSTRAINT module_unique UNIQUE (module)
)
"""
try:
    cur.execute(sql)
    print('创建表成功')
except Exception as e:
    print(e)
    print('创建表执行失败')
finally:
    cur.close()  # 关闭游标
