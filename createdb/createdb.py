#!/usr/bin/env python3
#Import dependencies
import mysql.connector
from mysql.connector import errorcode

#Connect to database
try:
    db = mysql.connector.connect(host = 'pandora',
                             db = 'biodb',
                             port = '',
                             user = '',
                             passwd = ''
                             )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    db.close()
    
#Check if tables exist   
    