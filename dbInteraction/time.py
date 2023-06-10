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
                "SELECT MAX(timeID) FROM timetable WHERE employeeID = %s", (ID,))
        lastTimeID = mycursor.fetchone()
        TimeID = lastTimeID[0] + 1
        mycursor.execute(
            "INSERT INTO timetable (timeID, punchType, dateAndTime ,employeeID) VALUES (%s, %s,%s,%s)", (TimeID, 'IN', punchTime, ID))
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
            "SELECT MAX(timeID) FROM timetable WHERE employeeID = %s", (ID,))
        lastTimeID = mycursor.fetchone()
        timeID = lastTimeID[0] + 1        
        mycursor.execute(
            "INSERT INTO timetable ( timeID, punchType, dateAndTime ,employeeID) VALUES (%s,%s,%s,%s)", (timeID,'OUT', punchTime, ID))
        db.commit()
        mycursor.close()
        print("Added punch out to user")
        
    except mysql.connector.Error as error:
        db.rollback()
        print("Failed to add punch to the database:", error)
    except Exception as e:
        db.rollback()
        print("Failed to add punch to the database:", e)


def lastPunchTime(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute("SELECT MAX(dateAndTime) FROM timetable WHERE employeeID = %s", (ID,))
    lastPunch = mycursor.fetchone()
    lastPunchT = lastPunch[0] if lastPunch[0] else None
    return lastPunchT