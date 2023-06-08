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

def addToDB(data):
    # Establishing databse connection
    db = mysql.connector.connect(
    host=DB_IP,
    port=DB_PORT,
    user=DB_USER,
    database="WFM_MAIN_INFO",
    password=DB_PASSWORD
    )

    mycursor = db.cursor()
    cursor2 = db.cursor()
    date = datetime.today().strftime('%Y-%m-%d')
    print(data)
    # Getting employee into main employee info table
    try:
        mycursor.execute("INSERT INTO employeeInfo (email,phoneNum,firstName,middleName,lastName,sinNum,remainingSickDays,remainingVacationDays,teamNum,permissionType,employeeStatus,dateJoined) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data['email'],data['phoneNum'],data['fName'],data['mName'],data['lName'],data['sinNum'],DEFAULT_SICK,DEFAULT_VACATION,0,0,DEFAULT_STATUS,date))
        db.commit()
        print("Added to employeeInfo")
    except:
        db.rollback()
        print("Failed to add employee to database")
    
    # Getting employee into employee pay information table
    try:
        mycursor.execute("SELECT employeeID FROM employeeInfo WHERE sinNum = %s", (data['sinNum'],))
        empID = (mycursor.fetchone())[0]
        
        mycursor.execute("INSERT INTO employeePay (employeeID, payStructure, wage, bankCode, transitNum, accountNum) VALUES (%s,%s,%s,%s,%s,%s)",(empID, data['payStructure'],data['wage'],data['bankCode'],data['transitNum'],data['accountNum']))
        db.commit()
        print("Added to employeePay")
    except:
        db.rollback()
        print("Failed to add employeePay to database")
        
    # Putting employee login information into user table
    try:
        mycursor.execute("SELECT employeeID FROM employeeInfo WHERE sinNum = %s",(data['sinNum'],))
        empID = (mycursor.fetchone())[0]

        # Password hashing
        ph = PasswordHasher()
        hashedPassword = ph.hash(data['password'])

        cursor2.execute("INSERT INTO user (email,password,employeeID) VALUES (%s,%s,%s)",(data['email'],hashedPassword,empID))
        db.commit()
        print("Added to user")
    except:
        db.rollback()
        print("Failed to add login to database")

    mycursor.close()
    cursor2.close()
    db.commit()
    db.close()


def checkData(data):
    works = True
    if data['email'] == "":
        works = False
    if data['phoneNum'] == "":
        works = False
    if data['fName'] == "":
        works = False
