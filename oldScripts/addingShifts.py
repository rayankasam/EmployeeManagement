import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from argon2 import PasswordHasher
import string
import random

db = mysql.connector.connect(
    host="99.229.135.158",
    port="3307",
    user='root',
    password="DaddyRayan$1",
    database="WFM_MAIN_INFO"
)

mycursor = db.cursor()

with open("shifts.txt", "r") as file:
    for line in file:
        element = line.split()
        
        punchType = element[0]
        dateTime = element[1] + " " + element[2]
        
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO timetable ( punchType, dateAndTime ,employeeID) VALUES (%s,%s,%s)", (punchType, dateTime, '1246'))
        db.commit()
        mycursor.close()
