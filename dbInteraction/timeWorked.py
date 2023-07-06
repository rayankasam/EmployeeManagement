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


def timeWorked(shifts):

    # case where last punch is a punchin, this would get the next punch after.
    if shifts[-1][3] == 'IN':
        db = mysql.connector.connect(
            host=DB_IP,
            port=DB_PORT,
            user=DB_USER,
            database="WFM_MAIN_INFO",
            password=DB_PASSWORD
        )
        mycursor = db.cursor()
        mycursor.execute(
            "SELECT * FROM timetable WHERE dateAndTime > %s AND employeeID = %s ORDER BY dateAndTime ASC LIMIT 1", (shifts[-1][2], ID))
        lastPunch = mycursor.fetchall()
        shifts.append(lastPunch)
        mycursor.close()
        db.close()

    if shifts[0][3] == 'OUT':
        shifts = shifts[1:]

    timeWorked = timedelta(hours=0, minutes=0, seconds=0)

    for x in range(len(shifts) - 1):
        if (shifts[x][3] == 'IN' and shifts[x+1][3] == 'OUT'):
            print(str(shifts[x+1][1]))
            print(str(shifts[x][1]))
            diff = (datetime.strptime(str(
                shifts[x+1][1]), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(shifts[x][1]), "%Y-%m-%d %H:%M:%S"))
            print(diff)
            timeWorked += diff
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
    mycursor.close()
    db.close()
    if len(shifts) == 0:
        return "no shifts"
    totalTime = timedelta(hours=0, minutes=0, seconds=0)
    print(shifts)
    if shifts[0][3] == 'OUT':
        totalTime += (datetime.strptime(str(shifts[0][1]), "%Y-%m-%d %H:%M:%S") -
                      datetime.now().replace(hour=0, minute=0, second=0))
        shifts = shifts[1:]

    if shifts[-1][3] == 'IN':
        totalTime += (datetime.now() -
                      datetime.strptime(str(shifts[-1][1]), "%Y-%m-%d %H:%M:%S"))
        shifts = shifts[:-1]
    if len(shifts) > 1:
        totalTime += timeWorked(shifts)
    return totalTime


def weekToDay(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )

    currentDate = date.today()
    weekBack = currentDate - timedelta(days=7)

    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) <= %s AND DATE(dateAndTime) >= %s AND  employeeID = %s", (currentDate, weekBack, ID,))
    shifts = mycursor.fetchall()
    mycursor.close()
    db.close()
    if len(shifts) == 0:
        return 0
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)


def monthToDay(ID):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )

    currentDate = date.today()
    weekBack = currentDate - timedelta(days=30)

    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) <= %s AND DATE(dateAndTime) >= %s AND  employeeID = %s", (currentDate, weekBack, ID,))
    shifts = mycursor.fetchall()
    mycursor.close()
    db.close()
    if len(shifts) == 0:
        return 0
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)


def custom(ID, start, end):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )

    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) <= %s AND DATE(dateAndTime) >= %s AND  employeeID = %s", (end, start, ID,))
    shifts = mycursor.fetchall()
    if len(shifts) == 0:
        return 0
    mycursor.close()
    db.close()
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)


def certainDate(ID, certainDate):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )

    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) = %s AND employeeID = %s", (certainDate, ID,))
    shifts = mycursor.fetchall()
    mycursor.close()
    db.close()
    if len(shifts) == 0:
        return "no shifts"
    totalTime = timedelta(hours=0, minutes=0, seconds=0)
    print(shifts)
    if shifts[0][3] == 'OUT':
        totalTime += (datetime.strptime(str(shifts[0][1]), "%Y-%m-%d %H:%M:%S") -
                      datetime.now().replace(hour=0, minute=0, second=0))
        shifts = shifts[1:]

    if shifts[-1][3] == 'IN':
        totalTime += (datetime.now() -
                      datetime.strptime(str(shifts[-1][1]), "%Y-%m-%d %H:%M:%S"))
        shifts = shifts[:-1]
    if len(shifts) > 1:
        totalTime += timeWorked(shifts)
    return totalTime


def beforeDate(ID, dateEntered):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )

    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) <= %s AND  employeeID = %s", (dateEntered, ID,))
    shifts = mycursor.fetchall()
    if len(shifts) == 0:
        return 0
    mycursor.close()
    db.close()
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)


def afterDate(ID, dateEntered):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE(dateAndTime) >= %s AND  employeeID = %s", (dateEntered, ID,))
    shifts = mycursor.fetchall()
    if len(shifts) == 0:
        return 0
    mycursor.close()
    db.close()
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)


def certainMonth(ID, dateEntered):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE_FORMAT(dateAndTime, '%Y-%m') = %s AND  employeeID = %s", (dateEntered, ID,))
    shifts = mycursor.fetchall()
    if len(shifts) == 0:
        return 0
    mycursor.close()
    db.close()
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)


def certainYear(ID, dateEntered):
    db = mysql.connector.connect(
        host=DB_IP,
        port=DB_PORT,
        user=DB_USER,
        database="WFM_MAIN_INFO",
        password=DB_PASSWORD
    )
    mycursor = db.cursor()
    mycursor.execute(
        "SELECT * FROM timetable WHERE DATE_FORMAT(dateAndTime, '%Y') = %s AND  employeeID = %s", (dateEntered, ID,))
    shifts = mycursor.fetchall()
    if len(shifts) == 0:
        return 0
    mycursor.close()
    db.close()
    for c in shifts:
        print(c[0], " ", c[1], " ", c[2])
    return timeWorked(shifts)
