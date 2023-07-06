import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta, date

load_dotenv(Path('./database.env'))
DB_IP = os.getenv('IP')
DB_PORT = os.getenv('PORT')
DB_PASSWORD = os.getenv('PASSWORD')
DB_USER = os.getenv('USERNAME')


def getAmountDue(employee):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor(dictionary=True)
    # Getting time worked
    mycursor.execute(
        'SELECT dateAndTime, punchType FROM timetable WHERE employeeID = %s ORDER BY dateAndTime DESC', (employee,))
    punches = mycursor.fetchall()

    mycursor.execute(
        'SELECT * FROM employeePay where employeeID = %s', (employee,)
    )

    employeePay = mycursor.fetchone()
    print(employeePay)
    rate = employeePay['wage']
    # Ignores shift if in progress
    if len(punches) % 2 == 1:
        punches.pop(0)
    punches = punches[::-1]
    shiftStart = None
    totalTime = timedelta(0)
    for idx, punch in enumerate(punches):
        if idx % 2 == 0:
            shiftStart = punch
        else:
            totalTime += punch['dateAndTime'] - shiftStart['dateAndTime']
    for punch in punches:
        print(punch['dateAndTime'])
    owed = totalTime.seconds()//3600 * rate
