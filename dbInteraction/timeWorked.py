import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta, date
from argon2 import PasswordHasher

load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USERNAME')



def timeWorked(shifts):
    #case where last punch is a punchin, this would get the next punch after.
    if shifts[-1][3] == 'IN':
        mycursor.execute(
            "SELECT * FROM timetable WHERE dateAndTime > %s AND employeeID = %s ORDER BY dateAndTime ASC LIMIT 1", (shifts[-1][2], ID))
        shifts.append(shifts[-1][3])


    if shifts[0][3] == 'OUT':
        shifts=shifts[1:]
        
    timeWorked = timedelta(hours=0, minutes=0, seconds=0)
                        
    for x in range(len(shifts) - 1):
        if (shifts[x][3] == 'IN' and shifts[x+1][3] == 'OUT'):
            print(str(shifts[x+1][1]))
            print(str(shifts[x][1]))
            diff = (datetime.strptime(str(shifts[x+1][1]), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(shifts[x][1]), "%Y-%m-%d %H:%M:%S"))
            print(diff)
            timeWorked+=diff
    mycursor.close()
    db.close()
    return timeWorked

def today(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    
    currentDate = date.today()
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) = %s AND employeeID = %s", (currentDate, ID,))
    shifts = mycursor.fetchall()
    
    if len(shifts) == 0: return "no shifts"
    totalTime = timedelta(hours=0, minutes=0, seconds=0)
    print(shifts)
    if shifts[0][3] == 'OUT':
        totalTime += (datetime.strptime(str(shifts[0][1]), "%Y-%m-%d %H:%M:%S") - datetime.now().replace(hour=0, minute=0, second=0))
        shifts=shifts[1:]
        
    if shifts[-1][3] == 'IN':
        totalTime += (datetime.now() -
                       datetime.strptime(str(shifts[-1][1]), "%Y-%m-%d %H:%M:%S") )
        shifts=shifts[:-1]
    if len(shifts) > 1:
        totalTime + timeWorked(shifts)
    return totalTime
