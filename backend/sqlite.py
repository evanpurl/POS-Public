import sqlite3
from sqlite3 import Error

customer_table = """CREATE TABLE IF NOT EXISTS customers ( customerid integer primary key autoincrement, company text, first_name text, last_name text, email text, phone text);"""
workorder_table = """CREATE TABLE IF NOT EXISTS workorders ( workorderid integer primary key autoincrement, date text, customerid integer, items json, total real);"""
item_table = """CREATE TABLE IF NOT EXISTS items ( itemid integer primary key autoincrement, itemname text, itemprice real);"""


def load_all(conn):
    create_itemtable_sqlite(conn)
    create_customertable_sqlite(conn)
    create_wotable_sqlite(conn)
    conn.close()


def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error or Exception as e:
        print(f"create db: {e}")


def create_wotable_sqlite(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(workorder_table)
        c.close()

    except Error or Exception as e:
        print(f"create table: {e}")


def create_customertable_sqlite(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(customer_table)
        c.close()

    except Error or Exception as e:
        print(f"create table: {e}")


def create_itemtable_sqlite(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(item_table)
        c.close()

    except Error or Exception as e:
        print(f"create table: {e}")


def createuniqueindex(conn, datatoinsert):
    try:
        c = conn.cursor()
        c.execute(datatoinsert)
        conn.commit()
        c.close()
        conn.close()
    except Error or Exception as e:
        print(f"createuniqueindex: {e}")


def insert_customer(conn, datalist):
    # config list should be a length of 2.
    try:
        datatoinsert = f""" REPLACE INTO customers(company, first_name, last_name, email, phone) VALUES( ?, ?, ?, ?, ?)"""
        c = conn.cursor()
        c.execute(datatoinsert, (datalist[0], datalist[1], datalist[2], datalist[3], datalist[4]))
        conn.commit()
        c.close()

    except Error or Exception as e:
        print(f"insert insert customer: {e}")


def insert_workorder(conn, datalist):
    # config list should be a length of 3.
    try:
        datatoinsert = f""" REPLACE INTO workorders(date, customerid, items, total) VALUES(?, ?, ?, ?)"""
        c = conn.cursor()
        c.execute(datatoinsert, (datalist[0], datalist[1], datalist[2], datalist[3]))
        conn.commit()
        c.close()

    except Error or Exception as e:
        print(f"insert work order: {e}")


def insert_item(conn, datalist):
    # config list should be a length of 3.
    try:
        datatoinsert = f""" REPLACE INTO items(itemname, itemprice) VALUES( ?, ?)"""
        c = conn.cursor()
        c.execute(datatoinsert, (datalist[0], datalist[1]))
        conn.commit()
        c.close()

    except Error or Exception as e:
        print(f"insert item: {e}")


def update_customer(conn, datalist):
    # config list should be a length of 6.
    try:
        datatoinsert = f""" Update customers SET company = ?, first_name = ?, last_name = ?, email = ?, phone = ? WHERE customerid = ?"""
        c = conn.cursor()
        c.execute(datatoinsert, (datalist[0], datalist[1], datalist[2], datalist[3], datalist[4], datalist[5]))
        conn.commit()
        c.close()

    except Error or Exception as e:
        print(f"update config: {e}")


def update_item(conn, datalist):
    # config list should be a length of 3.
    try:
        datatoinsert = f""" Update items SET itemname = ?, itemprice = ? WHERE itemid = ?"""
        c = conn.cursor()
        c.execute(datatoinsert, (datalist[0], datalist[1], datalist[2]))
        conn.commit()
        c.close()

    except Error or Exception as e:
        print(f"update config: {e}")


def get(conn, param, data=None):
    if param == "items":
        try:
            c = conn.cursor()
            c.execute(""" SELECT * FROM items """)
            option = c.fetchall()
            return option
        except Exception as e:
            print(f"get items: {e}")
    elif param == "customer":
        try:
            c = conn.cursor()
            c.execute(f""" SELECT * FROM customers WHERE customerid={data} """)
            option = c.fetchone()
            return option
        except Exception as e:
            print(f"get customer: {e}")
    elif param == "customers":
        try:
            c = conn.cursor()
            c.execute(""" SELECT * FROM customers """)
            option = c.fetchall()
            return option
        except Exception as e:
            print(f"get customers: {e}")
    elif param == "workorders":
        try:
            c = conn.cursor()
            c.execute(""" SELECT * FROM workorders """)
            option = c.fetchall()
            return option
        except Exception as e:
            print(f"get work orders: {e}")


def load_db(file):
    db = create_db(f"storage/PurlPOS.db")
    if file == "items":
        get_info = get(db, "items")
        db.close()
        return get_info
    elif file == "customers":
        get_info = get(db, "customers")
        db.close()
        return get_info
    elif file == "workorders":
        get_info = get(db, "workorders")
        db.close()
        return get_info


def open_db():
    db = create_db(f"storage/PurlPOS.db")
    return db


def delete(conn, datatype, queryid):
    try:
        if datatype == "items":
            datatoinsert = f""" delete from items WHERE itemid = ?"""
            c = conn.cursor()
            c.execute(datatoinsert, (queryid,))
            conn.commit()
            c.close()
        elif datatype == "customers":
            datatoinsert = f""" delete from customers WHERE customerid = ?"""
            c = conn.cursor()
            c.execute(datatoinsert, (queryid,))
            conn.commit()
            c.close()
        elif datatype == "workorder":
            datatoinsert = f""" delete from workorders WHERE workorder = ?"""
            c = conn.cursor()
            c.execute(datatoinsert, (queryid,))
            conn.commit()
            c.close()

    except Error or Exception as e:
        print(f"update config: {e}")
