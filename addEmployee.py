import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

# Getting databse information from env file

load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USER')
print(DB_USER)
# Establishing databse connection
db = mysql.connector.connect(
host=DB_IP,
port=DB_PORT,
user='root',
database="WFM_MAIN_INFO",
password=DB_PASSWORD
)
def addToDB():
  ...
def getInfo():
    # 0: email 1: phone number 2: First name 3: Middle name 4: Last name 5: sin number 6: Posiiton
    data = []
    data[0] = input("Enter email: ")
    data[1] = input("Enter Phone number: ")
    data[2] = input("Enter First name: ")
    data[3] = input("Enter Middle name: ")
    data[4] = input("Enter Last name: ")
    data[5] = input("Enter sin number: ")
    data[6] = input("Enter position: ")
