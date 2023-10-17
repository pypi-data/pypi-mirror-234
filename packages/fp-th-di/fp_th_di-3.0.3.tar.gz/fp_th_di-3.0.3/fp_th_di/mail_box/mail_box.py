import imaplib
import email
import email.utils 
import os
from email.header import decode_header
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from fp_th_di.logger import logger
from typing import Callable, Union, List
from fp_th_di.mail_box.email_object import Email
from fp_th_di.mail_box.email_attachment import EmailAttachment
import fp_th_di.mail_sender  as ms

class MailBox:
  def __init__(self, username:str, password:str, directory:str) -> None:
    """Initialize mailbox

    Args:
        username (str): email address 
        password (str): email password
        directory (str): download directory for mail attachments
    """    
    self.username = username
    self.password = password
    self.directory = directory
    self.imap = None

  def login(self) -> None:
    """Login to Gmail"""
    try:
      self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
      self.imap.login(self.username, self.password)
    except Exception as e:
      logger.exception(e)
      self.imap = None

  def logout(self) -> None:
    """Logout from Gmail"""    
    try:
      self.imap.close()
      self.imap.logout()
      self.imap = None
    except Exception as e:
      logger.exception(e)

  def is_logged_in(self) -> bool:
    """Check whether the connection to IMAP server's ready

    Returns:
        bool: True if mailbox's logged in; otherwise, False
    """    
    return not (self.imap is None)

  def get_emails_from_inbox(self, searchCriteria:str = "ALL", fetchLimit: Union[int, None] = 1, 
      boxName:str='INBOX', filteringFunction:Callable[[Email], bool] = None) -> List[Email]:
    """Get latest emails that meet the filteringFunction from targeted mailbox 

    Args:
        searchCriteria (str, optional): IMAP Search criteria to apply. Defaults to "ALL".
        fetchLimit (Union[int, None]|, optional): limit number of emails to fetch. Defaults to 1.
        boxName (str, optional): Targeted mailbox or tag to search from. Defaults to 'INBOX'.
        filteringFunction (Callable[[Email], bool], optional): filter function to applied when search. Defaults to None.

    Raises:
        Exception: raises 'Connection to mailbox is not ready' if mailbox was not logged in to IMAP 

    Returns:
        List[Email]: list of emails that met the search criteria found in targeted mailbox
    """      
    if not self.is_logged_in():
      raise Exception("Connection to mailbox is not ready")

    # search for emails that meet the searchCriteria
    logger.info('LOG - MailBox: Searching for ' + searchCriteria + ' in ' + boxName)
    typ, selectdata = self.imap.select(boxName, readonly=True)
    if typ == 'NO':
      return []
    
    status, messages = self.imap.search(None, searchCriteria)
    messages = messages[0].split()
    messages.reverse()

    emails = []
    for i in messages:
      # stop fetching emails if reach fetch limit
      if (fetchLimit is not None and len(emails) == fetchLimit):
        break

      # fetch each email message by ID
      res, msg = self.imap.fetch(i, "(RFC822)")
      for response in msg:
        incomingMail = None
        if isinstance(response, tuple):
          # parse a bytes email into a message object
          msg = email.message_from_bytes(response[1])
          # decode the email subject
          subject = decode_header(msg["Subject"])[0][0]
          if isinstance(subject, bytes):
            # if it's a bytes, decode to str
            subject = subject.decode()
          
          # email sender and timestamp
          from_ = msg.get("From")
          receivedDate=email.utils.parsedate(msg.get('date'))
          
          # initialize email object
          incomingMail = Email(from_, receivedDate, subject)
          incomingMail.emailAttachments = []

          # if the email message is multipart
          if msg.is_multipart():
            # iterate over email parts
            for part in msg.walk():
              # extract content type of email
              content_type = part.get_content_type()
              content_disposition = str(part.get("Content-Disposition"))
              body = ""
              try:
                # get the email body
                body = part.get_payload(decode=True).decode()
              except:
                pass
              
              if content_type == "text/plain" and "attachment" not in content_disposition:
                incomingMail.email_content = body
              elif "attachment" in content_disposition:
                # download attachment
                filename = part.get_filename()
                filepath = f'{self.directory}/{filename}'
                dummy, fileExtension = os.path.splitext(filename)
                if filename:
                  with open(filepath, "wb") as attachmentPayload:
                    attachmentPayload.write(part.get_payload(decode=True))
                  
                  if (fileExtension.lower() in ('.zip', '.csv', '.txt', '.xlsx')):
                    incomingAttachment = EmailAttachment(filepath, filename, fileExtension)
                    incomingMail.add_attachment(incomingAttachment)
          else:
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":
              incomingMail.emailContent = body
          
          if incomingMail:
            # discard the email of not pass filtering funtion
            if filteringFunction is not None and not filteringFunction(incomingMail):
              break

            emails.append(incomingMail)
            break
          
    return emails

  def send_mail(self, receiver:Union[str,list], subject:str, 
    content:str, isHTML:bool = False, attachments:list = []) -> None:
    """Send outgoing email

    Args:
        receiver (Union[str,list]): receivers
        subject (str): email subject
        content (str): email body
        isHTML (boolean): is the email content in HTML format
        attachments (list, optional): list of path_to_attachments. Defaults to [].
    """    
    logger.info('LOG - mailbox: sendmail - ' + subject + ' - To:' + str(receiver) + ' Attachments: ' + str(attachments))
    try:
      ms.send_mail(
        email_from=self.username,
        email_password=self.password,
        email_to=receiver, 
        subject=subject,  
        content=content,    
        is_html=isHTML,        
        attachments=attachments
      )
    except Exception as e:
      logger.exception(e)
