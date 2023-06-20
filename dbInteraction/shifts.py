
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


def shifts(ID, startTime, endTime, shiftType):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    try:
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO shifts (employeeID,  startTime, endTime, entryType) VALUES (%s,%s,%s,%s)",
                         (ID,  startTime, endTime, shiftType))
        mycursor.close()
        db.commit()
        print("Added to shifts")
        
        db.close()
        return "Shift Sussfully entered"
    
    except Exception as error:
       print(error)
       return "Failed to add shift, Please Try again."
