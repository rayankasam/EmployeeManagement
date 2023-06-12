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


ID = "1246"
print('Hello')

currentDate = datetime.now()
mycursor = db.cursor()
mycursor.execute(
        "SELECT * FROM timetable WHERE MONTH(dateAndTime) = 5 AND employeeID = %s", (ID,))
    
shifts = mycursor.fetchall()
print(shifts[0][3])

#case where last punch is a punchin, this would get the next punch after.
if shifts[-1][3] == 'IN':
    mycursor.execute(
        "SELECT * FROM timetable WHERE dateAndTime > %s AND employeeID = %s ORDER BY dateAndTime ASC LIMIT 1", (shifts[-1][2], ID))
    shifts.append(shifts[-1][3])
    
if shifts[1][3] == 'OUT':
    shifts=shifts[1:]
    
timeWorked = timedelta(hours=0, minutes=0, seconds=0)
                       
for x in range(len(shifts) - 1):
    if (shifts[x][3] == 'IN' and shifts[x+1][3] == 'OUT'):
        print(str(shifts[x+1][1]))
        print(str(shifts[x][1]))
        diff = (datetime.strptime(str(shifts[x+1][1]), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(shifts[x][1]), "%Y-%m-%d %H:%M:%S"))
        print(diff)
        timeWorked+=diff
print(f"Total time worked: {timeWorked}")


mycursor.close()
db.close()


