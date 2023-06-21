import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from argon2 import PasswordHasher

load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USERNAME')


def punchIN(ID):
    print(ID)
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    punchTime = datetime.now()
    print(punchTime)
    try:
        
        mycursor.execute(
            "INSERT INTO timetable ( punchType, dateAndTime ,employeeID) VALUES (%s,%s,%s)", ( 'IN', punchTime, ID))
        mycursor.close()
        db.commit()
        db.close()
        print("Added punch IN")
    except mysql.connector.Error as error:
        db.rollback()
        print("Failed to add punch to the database:", error)
    except Exception as e:
        db.rollback()
        print("Failed to add punch to the database:", e)

def punchOut(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    try:
        mycursor = db.cursor()
        punchTime = datetime.now()
          
        mycursor.execute(
            "INSERT INTO timetable ( punchType, dateAndTime ,employeeID) VALUES (%s,%s,%s)", ('OUT', punchTime, ID))
        db.commit()
        mycursor.close()
        print("Added punch out to user")
        
    except mysql.connector.Error as error:
        db.rollback()
        print("Failed to add punch to the database:", error)
    except Exception as e:
        db.rollback()
        print("Failed to add punch to the database:", e)


def lastPunch(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT punchType FROM timetable WHERE employeeID = %s AND dateAndTime = (SELECT MAX(dateAndTime) FROM timetable WHERE employeeID = %s)", (ID, ID))

    lastPunch = mycursor.fetchone()
    if lastPunch is None or lastPunch[0] is None:
        return 'OUT'

    else:
        return lastPunch[0]
#Ignore this function
#gonna have to figure out a way to make it work later, like self update.
def currentShift(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT punchType, dateAndTime FROM timetable WHERE employeeID = %s ORDER BY dateAndTime DESC LIMIT 1", (ID,))
    lastPunch = mycursor.fetchone()
    if lastPunch is None or lastPunch[0] is None or lastPunch[1] is None or lastPunch[0]=='OUT':
        return '0'

    else:
        return (datetime.now() - lastPunch[1])



