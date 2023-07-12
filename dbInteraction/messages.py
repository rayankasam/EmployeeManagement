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


def getMessages(ID):
    try:
        db = mysql.connector.connect(
            host=DB_IP,
            port=DB_PORT,
            user=DB_USER,
            database="WFM_MAIN_INFO",
            password=DB_PASSWORD
        )
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM messages WHERE sender = %s", (currentDate, ID,))
        messages = mycursor.fetchall()
        mycursor.close()
        db.close()
        if len(messages) == 0:
            return ("No messages found")
        
        return messages
    
    except Exception as error:
        print(error)
        return ""
    
def sendMessages(SID, RID, subject, content):
    try:
        db = mysql.connector.connect(
            host=DB_IP,
            port=DB_PORT,
            user=DB_USER,
            database="WFM_MAIN_INFO",
            password=DB_PASSWORD
        )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO messages (sender, receiver, subject, content) VALUES (%s,%s,%s,%s)",(SID, RID, subject,content))
        mycursor.close()
        db.close()
        print("Message sent")
        return "Sent"
    except Exception as error:
        print(error)
        return "Failed to send "