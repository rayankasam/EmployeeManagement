
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

# This function is to get the list of employees to be put in a drop down menu
def getPeople():
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT FirstName, lastName, employeeID  from  employeeInfo")
        data = mycursor.fetchall()
        mycursor.close()
        db.commit()
        db.close()
        #temp till i figure something better out
        data = [list(x) for x in data]
        # For the people that do not have a last name.
        for x in range(len(data)):
            if data[x][1] == None:
                data[x][1] =""
                

        print(data)
        return data
    except Exception as error:
       print(error)
       return "no employees found"


def addShifts(ID, startTime, endTime, shiftType):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    try:
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO shifts (employeeID,  startTime, endTime,lastName, entryType) VALUES (%s,%s,%s,%s)",
                         (ID,  startTime, endTime, shiftType))
        mycursor.close()
        db.commit()
        print("Added to employeeInfo")
        
        db.close()
        return "Shift Sussfully entered"
    
    except Exception as error:
       print(error)
       return "Failed to add shift, Please Try again."
def lastPunch(EMPID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    try:
        mycursor = db.cursor()
        mycursor.execute("SELECT punchType FROM timetable WHERE employeeID = %s ORDER BY dateAndTime DESC LIMIT 1",(EMPID,))
        punch = mycursor.fetchone()
        return punch[0]
    except Exception as e:
        print(e)
