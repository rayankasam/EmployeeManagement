import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from argon2 import PasswordHasher


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

    # Getting employee into main employee info table
    try:
        mycursor.execute("INSERT INTO employeeInfo (email,phoneNum,firstName,middleName,lastName,sinNum,remainingSickDays,remainingVacationDays,teamNum,permissionType,employeeStatus,dateJoined) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data['email'],data['phoneNum'],data['fName'],data['mName'],data['lName'],data['sinNum'],DEFAULT_SICK,DEFAULT_VACATION,0,0,DEFAULT_STATUS,date))
        db.commit()
        print("Added to employeeInfo")
    except:
        db.rollback()
        print("Failed to add employee to database")
    mycursor.execute("SELECT employeeID FROM employeeInfo WHERE sinNum = %s",(data['sinNum'],))
    empID = mycursor.fetchone()
    empID = empID[0]
    

    # Putting employee login information into user table
    try:
        ph = PasswordHasher()
        mycursor.execute("INSERT INTO user (email,password,employeeID) VALUES (%s,%s,%s)",(data['email'],ph.hash("Password"),empID))
        db.commit()
        print("Added to user")
    except:
        db.rollback()
        print("Failed to add login to database")




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
print(f"Welcome to the employee adding system\n{'-'*12}")
addToDB(
        {
            'email': 'rayankasam12@gmail.com',
            'password': 'rayan123',
            'phoneNum': '6477706663',
            'fName':'Rayan',
            'mName': None,
            'lName': 'Kasam',
            'sinNum': '234567891',
            'position': None
            }
        )
mycursor.close()
db.commit()
db.close()

