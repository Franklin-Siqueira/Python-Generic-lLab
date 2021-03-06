# Copyright 2021 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

'''
File name: runtimeUtils.py
Author: Franklin Siqueira
Date: 2019

'''
#####################################################################
#
#
#                                                           Libraries 
#####################################################################
from email.mime.text import MIMEText
import smtplib

# send mail
def send_email(email, height, average_height, count):
    from_email = "franklin.carrilho@gmail.com"
    from_password = "zglazwmbylsxkomi" # application password given by Google
    to_email = email

    subject = "Height Data Statistics"
    message = "Hi, your height is <strong>%s</strong>. <br> Average height of all is <strong>%s</strong> and that is calculated out of <strong>%s</strong> people. <br> Thanks!" % (height, average_height, count)

    msg = MIMEText(message, 'html')
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
