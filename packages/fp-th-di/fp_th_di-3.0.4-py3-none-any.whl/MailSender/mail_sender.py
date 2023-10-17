#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This script contains function required for sending email
"""
# emailutils
import os
import re
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def is_valid_email_address(email):
    ''' This function checks the format of email using regular expression
        PARAMETER:
            email (string): an email address
        RETURN:
            (re match object): an object for string that match the email pattern
    '''
    regex = '[^@]+@[^@]+\.[^@]+'
    return re.search(regex, email)


def send_mail(email_from, email_password, email_to, subject, content, is_html=False, attachments=None):
    ''' This function sends email with attachment (if any)
        PARAMETER:
            email_from (string): an email address for from part
            email_password (string): a password for email address, it should be app password generated in google account 
            email_to (string): an email add to send email to
            subject (string): a string as subject for email
            content (string): a string (html format is ok) as email content
            is_html (bool): True if the email content is in html format. Otherwise, False. Default value is False.
            attachments (list): a list of path to file to be attached
        RETURN:
            None
    '''
    
    # validate input
    if not bool(email_from):
        raise Exception('Invalid input - email_from is required')
    if not is_valid_email_address(email_from):
        raise Exception('Invalid input - email_from is invalid')
    if not bool(email_password):
        raise Exception('Invalid input - email_password is required')
    if not bool(email_to):
        raise Exception('Invalid input - email_to is required')
    
    # if email_to contains more than 1 email, split using ,
    if isinstance(email_to, str):
        email_to = email_to.split(',')
    else:
        email_to = ','.join(email_to).split(',')

    email_to = list(dict.fromkeys(email_to))
    cc_to = None
    if len(email_to) > 1:
        cc_to = ','.join(email_to[1:])
        email_to = email_to[0:1]
    email_to = ','.join(email_to)
    
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    if cc_to is not None:
        msg["CC"] = cc_to

    msg["Subject"] = subject
    msg.attach(MIMEText(content, 'html' if is_html else 'plain')) 

    # process attachment
    if attachments:
        
        # for each file
        for fileToSend in attachments:
            
            # create attachment object associated to mimetype
            ctype, encoding = mimetypes.guess_type(fileToSend)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)
            if maintype == "text":
                fp = open(fileToSend)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(fileToSend, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(fileToSend, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(fileToSend, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)

            filepath, filename = os.path.split(fileToSend)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attachment)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_from, email_password)
    text = msg.as_string()
    
    # send the mail
    s.sendmail(email_from, email_to if cc_to is None else [email_to] + cc_to.split(','), text) 
    s.quit()
