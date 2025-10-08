from email.mime import multipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(subject,template,email):
        with open(template,'r') as f:
            html=f.read()   
            FROM="fablyteam@gmail.com"
            PASS="vvpyklnooevpzgbs"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(FROM,PASS)
            message = f"Subject: {subject}\nFrom: {FROM}\nTo: {email} \nContent-Type: text/html\n\n {html}"
            server.sendmail(FROM,email,message)
            server.close()
            
send_email('You DId Amazing Job','templates/index.html',['uoszohaib@gmail.com','dildarhusain310@gmail.com','zh2935461@gmail.com','fabulously2021@gmail.com'])

