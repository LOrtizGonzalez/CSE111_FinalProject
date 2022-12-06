import sqlite3
from sqlite3 import Error
from datetime import date


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

# Front Page
def frontPage(_conn):
    print("+================================+")
    out ="""Are you buying or selling a vehicle?:
    1. Buying
    2. Selling
    +==================================+
    """
    print(out)
    choice = input()
    if(choice == '1'):
        buyerPage(_conn)
    elif(choice == '2'):
        sellerPage(_conn)
    else:
        print("Enter a valid option")
        frontPage(_conn)

def buyerPage(_conn):
    print("\n+===== BROWNSE CARS: =====+")
    cursor = _conn.cursor()
    Make = input('Enter make: ')
    Model = input('Enter model: ')
    Year = input('Enter year: ')
    
    command = ("""SELECT * FROM Automobile WHERE a_make = ?
        AND a_model = ? AND a_year = ? AND a_VIN IN(SELECT w_VIN FROM warehouse);
        """)
    args = [Make,Model,Year]
    cursor.execute(command, args)
    print('Results: ')
    results = cursor.fetchall()
    print('VIN    Make   Model     Type    Condition  Year   Price')
    for row in results:
        print(row)
    
    choice = input("""\n\nWhat would you like to do?
    1. Buy
    2. Browse
    *Press Any key to return home*
    """)
    if(choice == '1'):
        purchasePage(_conn)
    elif(choice == '2'):
        buyerPage(_conn)
    else:
        frontPage(_conn)

def purchasePage(_conn):
    print('\n+===== Purchase Page =====+\n')
    cursor = _conn.cursor()
    vehicle = input('To purchase enter vehicle VIN: ')
    args = [vehicle]
    firstname = input('Enter your first name:')
    lastname = input('Enter your last name: ')
    city = input('Enter your city: ')
    state = input('Enter your state: ')
    phone = input('Enter your phone number(xxx-xxx-xxxx):')
    date1 = date.today()

    #Retrieve car data for tranaction table
    first = ("""SELECT a_VIN, 1100+count(c_custkey), s_name, a_price FROM automobile, warehouse, seller, customer
            WHERE w_VIN = ?
            AND a_VIN = w_VIN AND w_sellerkey = s_sellerkey;""")
    cursor.execute(first,args)
    result = cursor.fetchall()
    for row in result:
        print(row)
    results = row
    #print("The vin = ",results[0])

    #Create new customer tuple; custkey,vin,last/firstname,phone,city,state,seller
    cust = ("""INSERT INTO Customer(c_custkey,c_VIN,c_lastname,c_firstname,
        c_phone,c_city,c_state,c_sellername) VALUES(?,?,?,?,?,?,?,?)""")
    args1 = [results[1],results[0],lastname,firstname,phone,city,state,results[2]]
    cursor.execute(cust,args1)
    _conn.commit()

    #Remove car from warehouse
    rm = ("""DELETE FROM Warehouse WHERE w_VIN = ?;""")
    args2 = [vehicle]
    cursor.execute(rm,args2)
    _conn.commit()

    #Update Transactions table
    include = ("""INSERT INTO Transactions(t_trkey,t_VIN,t_custkey,t_sellername,t_price,t_date)
        VALUES(?,?,?,?,?,?);""") 
    conc = int(str(vehicle) + str(results[1]))
    print(conc)
    args3 = [conc,vehicle,results[1],results[2],results[3],date1]
    cursor.execute(include,args3)
    _conn.commit()   
    

    #command = ("""INSERT INTO transactions """)



def sellerPage(_conn):
    print("you chose 2")

def main():
    #database = r"automobiles.sqlite"
    database = r"cars.db"
    # create a database connection
    conn = openConnection(database)
    with conn:
        #dropTables(conn)
        #createTables(conn)
        #populateTables(conn)
        frontPage(conn)
       
    closeConnection(conn, database)
if __name__ == '__main__':
    main()
