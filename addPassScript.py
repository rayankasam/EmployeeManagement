import mysql.connector
import os
import string
import random
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from argon2 import PasswordHasher


load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USERNAME')


# Establishing databse connection
db = mysql.connector.connect(
host=DB_IP,
port=DB_PORT,
user=DB_USER,
database="WFM_MAIN_INFO",
password=DB_PASSWORD
)
def generatePass():
    password = ""
    chars = string.ascii_letters + string.digits
    for i in range(random.randint(7,12)):
        password = password + chars[random.randint(0,len(chars))-1]
    return password

mycursor = db.cursor()

mycursor.execute("SELECT email, employeeID FROM employeeInfo")
data = mycursor.fetchall()

for i in data:
    employeeID = i[1]
    email = i[0]
    mycursor.execute("SELECT COUNT(1) FROM user WHERE employeeID = %s",(employeeID,))
    
    if mycursor.fetchone()[0] == 0:
        ...

#    if mycursor.fetchone()[0] == 0:
#        #Add to user
#        mycursor.execute("INSERT INTO user (email,password,employeeID) VALUES (%s,%s,%s)",(email,password,employeeID))

mycursor.close()
db.close()


