import mysql.connector
import os
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
mycursor = db.cursor()

def checkPassword(email,password):
    mycursor.execute("SELECT password FROM user WHERE email = %s",(email,))
    print("Query Executed")
    hashedPass = mycursor.fetchone()[0]
    print(f"password is {hashedPass}")
    ph = PasswordHasher()
    passwordMatch = False
    try:
        passwordMatch = ph.verify(hashedPass,password)
    except:
        ...
    return passwordMatch
def getLogin():
    email = input("Enter E-mail: ")
    password = input("Enter Password: ")
    return email, password


