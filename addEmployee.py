import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


# Getting databse information from env file

load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USERNAME')

# Getting default values from defaults.env
load_dotenv(Path('./defaults.env'))
DEFAULT_VACATION=os.getenv('REMAINING_VACATION_DAYS')
DEFAULT_SICK = os.getenv('REMAINING_SICK_DAYS')
DEFAULT_STATUS= os.getenv('STATUS')
# Establishing databse connection
db = mysql.connector.connect(
host=DB_IP,
port=DB_PORT,
user=DB_USER,
database="WFM_MAIN_INFO",
password=DB_PASSWORD
)
mycursor = db.cursor()

def addToDB(data):
    date = datetime.today().strftime('%Y-%m-%d')
    try:
        mycursor.execute("INSERT INTO employeeInfo (email,phoneNum,firstName,middleName,lastName,sinNum,remainingSickDays,remainingVacationDays,teamNum,permissionType,employeeStatus,dateJoined) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data['email'],data['phoneNum'],data['fName'],data['mName'],data['lName'],data['sinNum'],DEFAULT_SICK,DEFAULT_VACATION,0,0,DEFAULT_STATUS,date))
        db.commit()
    except:
        db.rollback()
    print("Added to db")
def getInfo():
    data = {}
    data['email'] = input("Enter email: ")
    data['password'] = input("Enter password: ")
    data['phoneNum'] = input("Enter Phone number: ")
    data['fName'] = input("Enter First name: ")
    data['mName'] = input("Enter Middle name: ")
    if data['mName'] == "":
        data['mName'] = None
    data['lName'] = input("Enter Last name: ")
    if data['lName'] == "":
        data['lName'] = None
    data['sinNum'] = input("Enter sin number: ")
    data['position'] = input("Enter position: ")
    if data['position'] == "":
        data['position'] = None
    return data
print("Welcome to the employee adding system\n--------------------------------------------------------")
addToDB(getInfo())
db.close()

