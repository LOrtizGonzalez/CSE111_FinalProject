import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)
    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")
    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)
    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

#Create Tables for database
def createTables(_conn):
    print("Creating Tables")
    _conn.execute("BEGIN")

    try:
        sql = """CREATE TABLE customer (
            c_custkey decimal(5,0) not null PRIMARY KEY,
            c_VIN decimal(5,0) not null,
            c_lastname varchar(50) not null,
            c_firstname varchar(50) not null,
            c_phone varchar(50) not null,
            c_city varchar(50) not null,
            c_state varchar(10) not null,
            c_sellername varchar(50) not null
        )"""
        _conn.execute(sql)
        print("success customer table")
#--------------------------------------
        sql = """CREATE TABLE seller (
            s_sellerkey decimal(5,0) not null PRIMARY KEY,
            s_name varchar(50) not null,
            s_phone varchar(50) not null,
            s_city varchar(50) not null,
            s_state varchar(10) not null,
            s_email varchar(50) not null
        )"""
        _conn.execute(sql)
        print("success seller table")
#--------------------------------------
        sql = """CREATE TABLE manufacturer (
            m_mftrkey decimal(5,0) not null,
            m_make varchar(25) not null,
            m_model varchar(25) not null,
            m_type varchar(25) not null
        )"""
        _conn.execute(sql)
        print("success manufacturer table")
#--------------------------------------
        sql = """CREATE TABLE transactions (
            t_trkey varchar(50) not null PRIMARY KEY,
            t_VIN decimal(5,0) not null,
            t_custkey decimal(5,0) not null,
            t_sellername varchar(25) not null,
            t_price decimal(7,0) not null,
            t_date date not null
        )"""
        _conn.execute(sql)
        print("success transactions table")
#--------------------------------------
        sql = """CREATE TABLE automobile (
            a_VIN decimal(5,0) not null PRIMARY KEY,
            a_make varchar(25) not null,
            a_model varchar(25) not null,
            a_type varchar(25) not null,
            a_year decimal(5,0) not null,
            a_condition varchar(25) not null,
            a_color varchar(25) not null,
            a_price decimal(7,0) not null
        )"""
        _conn.execute(sql)
        print("success automobile table")
#--------------------------------------
        sql = """CREATE TABLE warehouse (
           w_VIN decimal(5,0) not null,
           w_sellerkey decimal(2,0) not null
        )"""
        _conn.execute(sql)
        _conn.execute("COMMIT")
        print("Tables created successfully!")
#=================================================
    except Error as e:
        _conn.execute("ROLLBACK")
        print(e)

def dropTables(_conn):
    _conn.execute("BEGIN")
    try:
        sql = """DROP TABLE customer"""
        _conn.execute(sql)

        sql = """DROP TABLE seller"""
        _conn.execute(sql)

        sql = """DROP TABLE manufacturer"""
        _conn.execute(sql)

        sql = """DROP TABLE transactions"""
        _conn.execute(sql)

        sql = """DROP TABLE automobile"""
        _conn.execute(sql)

        sql = """DROP TABLE warehouse"""
        _conn.execute(sql)
        _conn.execute("COMMIT")
        print("Tables deleted!")

    except Error as e:
        _conn.execute("ROLLBACK")
        print(e)

def main():
    database = r"automobiles.sqlite"
    # create a database connection
    conn = openConnection(database)
    with conn:
        #dropTables(conn)
        createTables(conn)
        #populateTables(conn)
       
    closeConnection(conn, database)
if __name__ == '__main__':
    main()
