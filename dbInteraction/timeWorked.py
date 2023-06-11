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


def timeWorked(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE MONTH(dateAndTime) = 5 AND YEAR(dateAndTime) = YEAR(CURDATE()) AND employeeID = %s", (ID,))
    shifts = mycursor.fetchall()
    mycursor.close()
    db.close()
    
    for x in range(len(shifts)):
        print(shifts[x][0]," ", shifts[x][1]," " , shifts[x][3])
    return "done"

print(timeWorked(str(1246)))