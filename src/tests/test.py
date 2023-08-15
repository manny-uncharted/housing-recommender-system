import os
from io import StringIO
import re
import sys
sys.path.append('..') 
from modules.utils import send_emails_recommender
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv



load_dotenv()
sender = os.getenv("MAIL_USERNAME")

password = os.getenv("MAIL_PASSWORD")

subject = "My Recommended property"
email = input("Enter email : ")
receipients = [email]
output = "Hello, "
try:
    send_emails_recommender(email_list=receipients , body_content=output, subject=subject, email_from=sender, pswd=password)
except:
    Exception("Error sending email")