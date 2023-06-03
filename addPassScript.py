import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from argon2 import PasswordHasher
import string
import random


load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USERNAME')


# Establishing databse connection
db = mysql.connector.connect(
host="99.229.135.158",
port="3307",
user="root",
database="WFM_MAIN_INFO",
password="DaddyRayan$1"
)

mycursor = db.cursor()


def generatePass():
    password = ""
    chars = string.ascii_letters + string.digits
    for i in range(random.randint(7,12)):
        password = password + chars[random.randint(0, len(chars)-1)]
    return password

mycursor = db.cursor()

mycursor.execute("SELECT email, employeeID FROM employeeInfo")
data = mycursor.fetchall()


for row in data:
    employeeID = row[1]
    email = row[0]
    mycursor.execute("SELECT COUNT(1) FROM user WHERE employeeID = %s", (employeeID,))
    
    if mycursor.fetchone()[0] == 0:
         password = generatePass()   
         line = "\n"+ str(email) +"\t"+ str(password) +"\t" + str(employeeID)
         with open('password.txt', 'a') as fh:
            fh.writelines(line)  

         ph = PasswordHasher()
         hashedPassword = ph.hash(password)
        
         mycursor.execute("INSERT INTO user (email,password,employeeID) VALUES (%s,%s,%s)",(email,hashedPassword,employeeID))
         
mycursor.close()
db.commit()
db.close()