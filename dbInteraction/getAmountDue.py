import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta, date


class NotInDatabase(Exception):
    ...


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

    # Getting wage
    mycursor.execute(
        'SELECT * FROM employeePay where employeeID = %s', (employee,)
    )
    try:
        employeePay = mycursor.fetchone()
        rate = int(employeePay['wage'])
    except:
        raise NotInDatabase

    # Ignores shift if in progress
    if len(punches) % 2 == 1:
        punches.pop(0)

    # Starts with first ever punch
    punches = punches[::-1]

    # Adds up the total time of each shift
    totalTime = timedelta(0)
    for idx, punch in enumerate(punches):
        if idx % 2 == 0:
            shiftStart = punch
        else:
            totalTime += punch['dateAndTime'] - shiftStart['dateAndTime']
    totalDue = totalTime.total_seconds() // 3600 * rate

    # Getting total already paid
    mycursor.execute(
        'SELECT paymentAmount FROM Payments WHERE employeeID = %s', (employee,))
    totalPaid = 0
    for payment in mycursor.fetchall():
        totalPaid += float(payment['paymentAmount'])

    # Returning all the data required
    data = {}
    data['amount'] = f"${totalDue - totalPaid}"
    data['payStructure'] = employeePay['payStructure']
    data['wage'] = float(employeePay['wage'])
    data['bankCode'] = employeePay['bankCode']
    data['transitNum'] = employeePay['transitNum']
    data['accountNum'] = employeePay['accountNum']
    return data
