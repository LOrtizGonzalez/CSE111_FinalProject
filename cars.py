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

# xxxxx HOME PAGE xxxxx 
def frontPage(_conn):
    print("\n+=============== HOME PAGE =================+")
    out =("""Are you buying or selling a vehicle?:\n
    1. Buying
    2. Selling
    3. End Program \n
    """)
    print(out)
    choice = input("Enter choice: ")
    if(choice == '1'):
        buyerPage(_conn)
    elif(choice == '2'):
        sellerPage(_conn)
    elif(choice == '3'):
        end()
    else:
        print("Enter a valid option")
        frontPage(_conn)

def end():
    print("\nProgram ended.\n")
    exit()

#BUYER side
def buyerPage(_conn):
    print("\n+=============== CHOOSE MAKE: ===============+")
    cursor = _conn.cursor()
    print('{:>10}'.format(""" 
        1. Ford
        2. Dodge
        3. Chevrolet
        4. Honda
        5. Toyota
        6. BMW
        7. Mercedes
        """))
    while True:
        try:
            choice = int(input('Enter MAKE choice: '))
            assert 0 < choice <= 7
        except ValueError:
            print("Enter an integer!\n")
        except AssertionError:
            print("Invalid Integer input!\n")
        else:
            break
    if(choice == 1):
        Make = 'Ford'
    elif(choice == 2):
        Make = 'Dodge'
    elif(choice == 3):
        Make = 'Chevrolet'
    elif(choice == 4):
        Make = 'Honda'
    elif(choice == 5):
        Make = 'Toyota'
    elif(choice == 6):
        Make = 'BMW'
    else:
        Make = 'Mercedes'
    
    while True:
        try:
            choice2 = int(input("\n1. Enter Model or 2. Search up now?: "))
            assert 0 < choice2 <= 2
        except ValueError:
            print("Enter an Integer!\n")
        except AssertionError:
            print("Enter a Valid Integer!\n")
        else:
            break
    if(choice2 == 1):
        modelPage(_conn,Make)
    else:
        search1(_conn,Make)


def modelPage(_conn, Make):
    cursor = _conn.cursor()
    print("\n+=========== CHOOSE MODEL ===========+\n")

    cmd = ("""SELECT a_model FROM Automobile WHERE a_make = ?
        AND a_VIN IN(SELECT w_VIN FROM Warehouse)
        GROUP BY a_model;""")
    args = [Make]
    cursor.execute(cmd,args)
    res = cursor.fetchall()
    n = 0
    res1 = []
    for row in res:
        n+=1 #keeps track of the number of options
        res1 += res[n-1]
        a = res1[n-1].replace("'", '') #removed the '' from the return string1
        print('{:>9}'.format(n),a) ###------changed from row
   
    while True:
        try: 
            choice = int(input('\nEnter MODEL choice: '))
            assert 0 < choice <= n
        except ValueError:
            print('Invalid entry!!')
        except AssertionError:
            print("Enter an integer!")
        else:
            break

    Model = res1[choice - 1]
    #print("This is the model: ",Model)
    while True:
        try:
            choice1 = int(input("\n\n1. Enter Year OR 2. Search Now: "))
            assert 0 < choice1 <= 2
        except ValueError:
            print("Enter an Integer!")
        except AssertionError:
            print("Enter a valid Integer!")
        else:
            break
    
    if(choice1 == 1):
        yearPage(_conn,Make,Model)
    else:
        search2(_conn,Make,Model)


def yearPage(_conn,Make,Model):
    cursor = _conn.cursor()
    print("\n+=============== CHOOSE YEAR ===============+")
    print("""
        1. 2019
        2. 2020
        3. 2021
        4. 2022
        """)
    while True:
        try:
            choice = int(input("Enter Year choice: "))
            assert 0 < choice <= 4
        except ValueError:
            print("Enter an Integer choice: \n")
        except AssertionError:
            print("Enter valid Integer!\n")
        else: 
            break
    if(choice == 1):
        Year = 2019
    elif(choice == 2):
        Year = 2020
    elif(choice == 3):
        Year = 2021
    else:
        Year = 2022

    search3(_conn,Make,Model,Year)

def search1(_conn,Make):
    cursor = _conn.cursor()
    sql = ("""SELECT * FROM automobile WHERE a_make = ?
        AND a_VIN IN (SELECT w_VIN FROM warehouse);""")
    args = [Make]
    cursor.execute(sql,args)
    results = cursor.fetchall()
    print("\n\nResults for",Make,":\n")
    print('{:<10}{:<12}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}'.format('VIN',    'Make',   'Model'    ,'Type'   ,'Year'   ,'Condition'  ,'Color',  'Price'))
    for row in results:
        print('{:<10}{:<12}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}'.format(row[0],
        row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    option(_conn,row[1],row[2],row[4])

def search2(_conn,Make,Model):
    cursor = _conn.cursor()
    sql = ("""SELECT * FROM automobile WHERE a_make = ? 
        AND a_model = ? AND a_VIN IN (SELECT w_vin FROM warehouse);""")
    args = [Make,Model]
    cursor.execute(sql,args)
    results = cursor.fetchall()
    print("\n\nResults for ",Make,Model,": ")
    print('{:<10}{:<12}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}'.format('VIN','Make','Model','Type','Year','Condition','Color','Price'))

    for row in results:
        print('{:<10}{:<12}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}'.format(row[0],
        row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    option(_conn,row[1],row[2],row[4])


def search3(_conn,Make,Model,Year):
    cursor = _conn.cursor()
    command = ("""SELECT * FROM Automobile WHERE a_make = ?
        AND a_model = ? AND a_year = ? AND a_VIN IN(SELECT w_VIN FROM warehouse);
        """)
    args = [Make,Model,Year]
    cursor.execute(command, args)
    print('\nResults: ')
    results = cursor.fetchall()
    #count = 0
    #arr = results
    print("\nResults for",Make,Model,Year,":\n")
    print('{:<10}{:<12}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}'.format('VIN','Make','Model','Type','Year','Condition','Color','Price'))
 #Added formatting
    for row in results:
        print('{:<10}{:<12}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}'.format(row[0],
        row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        #print(row)
    option(_conn,Make,Model,Year)


def option(_conn,Make,Model,Year):
    print("\n\n+=============================================+")
    print("""\nWhat would you like to do?\n
    1. Continue Browsing
    2. Buy Vehicle
    (*Press Any key to return home*)
    """)
    choice = input("Enter your choice: ")
    if(choice == '1'):
        buyerPage(_conn)
    elif(choice == '2'):
        purchasePage(_conn,Make,Model,Year)
    else:
        frontPage(_conn)


def purchasePage(_conn,Make,Model,Year):
    print('\n+===== Purchase Page =====+\n')
    cursor = _conn.cursor()
    make = Make
    model = Model
    year = Year
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
         print("")
         #print(row)
    results = row
    #print("The vin = ",results[0])
    #Create new customer tuple; custkey,vin,last/firstname,phone,city,state,seller
    cust = ("""INSERT INTO Customer(c_custkey,c_VIN,c_lastname,c_fistname,
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
    #print(conc)
    args3 = [conc,vehicle,results[1],results[2],results[3],date1]
    cursor.execute(include,args3)
    _conn.commit()   
    print("Congratulations ",firstname, " ",lastname," on your ",
    year, " ", make, " ", model, "!!")

#==========================================================================
#Seller Log in
def sellerPage(_conn):
    choice = input('Do you have a seller ID?: Y/N \n')
    if (choice == 'Y' or choice == 'y'):
        cursor = _conn.cursor()
        Seller_ID = input('Enter Seller ID: ')
        statement = f"SELECT * FROM Seller WHERE s_sellerkey = '{Seller_ID}';"
        cursor.execute(statement)
        if not cursor.fetchone():
            print("Seller ID does not exist")
            sellerPage(_conn)
        else:
            sellerCatalog(_conn, Seller_ID)
    
    elif(choice == 'N' or choice == 'n'):
        PATH = input('Would you like to add yourself as a seller?: Y/N \n')
        if (PATH == 'Y' or PATH == 'y'):
            cursor = _conn.cursor()
            Name = input('Insert company name: ')
            Phone = input('Insert main phone number: ')
            City = input('Insert city name: ')
            State = input('Insert state name ')
            Email = input('Insert main email address: ')

            c = _conn.cursor()
            c.execute("""SELECT count(distinct s_sellerkey) + 1
             FROM Seller;""")
            res = c.fetchall()
            for row in res:
                print(format(row))
            results = format(row)
            num = results[1]

            cursor.execute("""INSERT INTO Seller(s_sellerkey,s_name, s_phone, s_city, s_state, s_email)
            VALUES (?,?,?,?,?,?)""", (int(num),Name, Phone, City, State, Email))
            _conn.commit()

            # cursor.execute("""INSERT INTO Seller(s_sellerkey, s_name, s_phone, s_city, s_state, s_email)
            # VALUES (?,?,?,?,?,?)""", (results, Name, Phone, City, State, Email))
            # _conn.commit()

            print('Seller created')
            sellerPage(_conn)

        else:
            print("Thank you, come again\n")
            frontPage(_conn)

    # elif(choice == 'N' or choice == 'n'):
    #     cursor = _conn.cursor()
    #     Name = input('Insert company name: ')
    #     Phone = input('Insert main phone number: ')
    #     City = input('Insert city name: ')
    #     State = input('Insert state name ')
    #     Email = input('Insert main email address: ')

    #     c = _conn.cursor()
    #     c.execute("""SELECT count(distinct s_sellerkey) + 1
    #      FROM seller;""")
    #     res = c.fetchall()
    #     for row in res:
    #         print(format(*row))
    #     results = format(*row)

    #     cursor.execute("""INSERT INTO seller(s_sellerkey, s_name, s_phone, s_city, s_state, s_email)
    #     VALUES (?,?,?,?,?,?)""", (results, Name, Phone, City, State, Email))
    #     _conn.commit()

        # print('Seller created')
        # sellerPage(_conn)

    #For deleting tables, do not use---       
    elif(choice == '8000'):

        cursor = _conn.cursor()
        cursor.execute("""delete from seller Where s_sellerkey = '6';""")
        _conn.commit()

        sellerPage(_conn)

    else:
        print("Invalid option!")
        sellerPage(_conn)


#Seller Catalog
def sellerCatalog(_conn, Seller_ID):
    cursor = _conn.cursor()
    command = ("""SELECT * FROM seller WHERE s_sellerkey = ?;""")
    args = [Seller_ID]
    cursor.execute(command, args)

    print('Results: ')
    results = cursor.fetchall()
    print(' ID  Name        Phone           City     State  Email')
    for row in results:
        print(row)
    print('\nChoose an option\n')
    print('To view current inventory press: 1')
    print('To add a vehicle press: 2')
    print('To view past transactions press: 3')
    print('To go back to home page press: 4')

    choice = input()
    if(choice == '1'):
        cursor = _conn.cursor()
        command = ("""SELECT a_VIN, a_make, a_model, a_type, a_year, a_condition, a_color, a_price
         FROM seller, automobile, warehouse WHERE s_sellerkey = ? AND w_sellerkey = s_sellerkey
         AND w_VIN = a_VIN;""")
        args = [Seller_ID]
        cursor.execute(command, args)

        print('Results: ')
        results = cursor.fetchall()
        print(' VIN    Make    Model     Type    Condition  Year   Price')
        for row in results:
            print(row)

        sellerCatalog(_conn, Seller_ID)

        
    elif(choice == '2'):
        cursor = _conn.cursor()
        Maker = input('Insert vehicle maker: ')
        if (Maker == 'Ford' or Maker == 'Chevrolet' or Maker == 'Dodge' or Maker == 'Toyota' or Maker == 'Honda' or Maker == 'BMW' or Maker == 'Mercedes'):
            Model = input('Insert vehicle model: ')
            Type = input('Insert vehicle type: ')
            Year = input('Insert vehicle year: ')
            Condition = input('Insert vehicle condition: ')
            Color = input('Insert vehicle color: ')
            Price = input('Insert vehicle price: ')
        else:
            print("Invalid maker")
            sellerCatalog(_conn, Seller_ID)
        # Model = input('Insert vehicle model: ')
        # Type = input('Insert vehicle type: ')
        # Year = input('Insert vehicle year: ')
        # Condition = input('Insert vehicle condition: ')
        # Color = input('Insert vehicle color: ')
        # Price = input('Insert vehicle price: ')


        c = _conn.cursor()
        c.execute("""SELECT count(distinct a_VIN) + 3100
         FROM automobile;""")
        res = c.fetchall()
        for row in res:
            print(format(*row))
        results = format(*row)
        

        cursor.execute("""INSERT INTO automobile(a_VIN, a_make, a_model, a_type, a_year, a_condition, a_color, a_price)
        VALUES (?,?,?,?,?,?,?,?)""", (results, Maker, Model, Type, Year, Condition, Color, Price))
        _conn.commit()


        cursor.execute("""INSERT INTO warehouse(w_VIN, w_sellerkey)
        VALUES (?,?)""", (results, Seller_ID))
        _conn.commit()
        print('Added New Automobile')

        sellerCatalog(_conn, Seller_ID)


    elif(choice == '3'):
        cursor = _conn.cursor()
        command = ("""SELECT t_trkey, t_VIN, t_custkey, t_sellername, t_price, t_date
            FROM seller, transactions WHERE s_sellerkey = ? AND t_sellername = s_name;
            """)
        args = [Seller_ID]
        cursor.execute(command, args)

        print('Results: ')
        results = cursor.fetchall()
        print('  Key        VIN  Custkey  Sellername  Price  Date')
        for row in results:
            print(row)

        sellerCatalog(_conn, Seller_ID)

    elif(choice == '4'):
        frontPage(_conn)

    #For deleting tables, do not use---       
    elif(choice == '8000'):

        cursor = _conn.cursor()
        cursor.execute("""delete from automobile Where a_VIN = '3220';""")
        _conn.commit()

        cursor = _conn.cursor()
        cursor.execute("""delete from warehouse Where w_VIN = '3220';""")
        _conn.commit()


        sellerCatalog(_conn, Seller_ID)
    else:
        print("Enter a valid option")
        sellerCatalog(_conn, Seller_ID)

#Manufacturer page
def manufacturerPage(_conn):
    cursor = _conn.cursor()
    print('\nChoose your favorite manufacturer')
    Make = input('Input either Ford, Chevrolet, Dodge, Toyota, Honda, BMW, or Mercedes to view model types\n')

    if (Make == 'Ford' or 'Chevrolet' or 'Dodge' or 'Toyota' or 'Honda' or 'BMW' or 'Mercedes'):
        cursor = _conn.cursor()
        command = ("""SELECT *
         FROM manufacturer WHERE m_make = ?;
         """)
        args = [Make]
        cursor.execute(command, args)

        print('Results: ')
        results = cursor.fetchall()
        print(' Key    Maker    Model     Type')
        for row in results:
            print(row)

        frontPage(_conn)

    else:
        frontPage(_conn)


# def sellerPage(_conn):
#     print("you chose 2")

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
