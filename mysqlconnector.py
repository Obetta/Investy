# !python3

import price_update
import mysql.connector
from mysql.connector import Error

def displayWatchlist(userid_):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')
        
        sql_select_Query = "select WatchList.CompanyName, Company.Price from USERS Natural join WatchList join Company on Company.CompanyName = WatchList.CompanyName where USERS.userID = {}".format(userid_)

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return records

def authorizeUser(email_, password):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')
        
        sql_select_Query = "SELECT * FROM USERS WHERE Email = {} AND Password_ = {}".format(email_, password)

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return records

def checkUserExists(email_,):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')
        
        sql_select_Query = "SELECT * FROM USERS WHERE Email = {}".format(email_)

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return records

# can use this to search for a stock then return the price given the name
def createNewUser(fname, lname, phone_number, email, password):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')

        sql_select_Query = "INSERT INTO USERS (FirstName, LastName, PhoneNumber, Email, Password_) VALUES ({},{},{},{},{})".format(fname, lname, phone_number, email, password)

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def GetCompanyPrice(stock):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')

        
        sql_select_Query = "SELECT Price From Company where CompanyName = " + stock 

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        price = 0
        price =  records[0][0]
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return price

def callProcedureInsert(userid, company_name):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')
        cursor = connection.cursor()
        cursor.callproc('updateWatchlist', [userid, company_name])
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def callProcedureDelete(userid, company_name):

    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')
        cursor = connection.cursor()
        cursor.callproc('deleteWatchlist', [userid, company_name])
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def updateallprices(name, price):
    try:
        connection = mysql.connector.connect(host='database-1.crilyi7ijefu.us-east-2.rds.amazonaws.com',
                                            database= 'Investy_Data',
                                            user='admin',
                                            password='asdfghjk')
        cursor = connection.cursor()
        cursor.callproc('new_procedure', [name, price])
        connection.commit()
        print("Printing laptop details")
        for result in cursor.stored_results():
            print(result.fetchall())

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")