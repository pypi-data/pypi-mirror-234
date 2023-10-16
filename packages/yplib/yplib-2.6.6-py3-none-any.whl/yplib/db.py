from yplib.index import *
import pymysql


# 有关数据库操作的类
def get_connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset='utf8mb4', port=3306, host='192.168.40.230'):
    # return pymysql.connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset="utf8mb4",
    #                        port=3307,
    #                        host='192.168.40.230')
    return pymysql.connect(db=db, user=user, passwd=passwd, charset=charset, port=port, host=host)


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_sql(db_conn, sql='', commit=True):
    if db_conn is None or sql is None or sql == '':
        to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    db_cursor = db_conn.cursor()
    if isinstance(sql, list) or isinstance(sql, set):
        for s in sql:
            to_log_file(s)
            db_cursor.execute(s)
    else:
        to_log_file(sql)
        db_cursor.execute(str(sql))
    if commit:
        db_conn.commit()


# 执行 sql 语句, 不提交
def exec_sql_un_commit(db_conn, sql=''):
    exec_sql(db_conn=db_conn, sql=sql, commit=False)


# 执行 sql 获得 数据
def get_data_from_sql(db_conn, sql=''):
    if db_conn is None or sql is None or sql == '':
        to_log_file("db_conn is None or sql is None or sql == '', so return")
        return
    db_cursor = db_conn.cursor()
    to_log_file(sql)
    db_cursor.execute(str(sql))
    return db_cursor.fetchall()
