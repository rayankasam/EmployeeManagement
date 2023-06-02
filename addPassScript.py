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


# Establishing databse connection
db = mysql.connector.connect(
host=DB_IP,
port=DB_PORT,
user=DB_USER,
database="WFM_MAIN_INFO",
password=DB_PASSWORD
)

mycursor = db.cursor()

mycursor.execute("SELECT ")
