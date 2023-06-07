
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

# Getting default values from defaults.env
load_dotenv(Path('./defaults.env'))
DEFAULT_VACATION=os.getenv('REMAINING_VACATION_DAYS')
DEFAULT_SICK = os.getenv('REMAINING_SICK_DAYS')
DEFAULT_STATUS= os.getenv('STATUS')

def getData(email):
    
    # Establishing databse connection
    db = mysql.connector.connect(
    host=DB_IP,
    port=DB_PORT,
    user=DB_USER,
    database="WFM_MAIN_INFO",
    password=DB_PASSWORD
    )

    mycursor = db.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM employeeInfo WHERE email = %s",(email,))
    try:    
        data = mycursor.fetchall()[0]
        return data
    except:
        return ValueError
