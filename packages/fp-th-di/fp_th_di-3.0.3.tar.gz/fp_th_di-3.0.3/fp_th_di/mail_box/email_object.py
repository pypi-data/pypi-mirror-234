from fp_th_di.mail_box.email_attachment import EmailAttachment
from typing import List, Union
from fp_th_di.logger import logger
import datetime

class Email:
  def __init__(self, emailFrom, emailDate, emailSubject:str, 
  emailContent:str = None, emailAttachments: List[EmailAttachment] = []):
    self.emailFrom = emailFrom
    self.emailDate = emailDate # received datetime
    self.emailSubject = emailSubject
    self.emailContent = emailContent
    self.emailAttachments = emailAttachments

  def __str__(self) -> str:
    return str({
        'emailFrom': self.emailFrom,
        'emailDate': self.get_received_on_datetime(),
        'emailSubject': self.emailSubject,
        'emailContent': self.emailContent,
        'emailAttachments': [str(each_attachment) \
          for each_attachment in self.emailAttachments] 
    })

  def add_attachment(self, attachment:EmailAttachment) -> None:
    """add an attachment to attachment list 

    Args:
        attachment (EmailAttachment)
    """    
    if attachment not in self.emailAttachments:
      self.emailAttachments.append(attachment)
    
  def has_attachment(self) -> bool:
    """Check whether email has attachment

    Returns:
        bool: True if it has at least one attachments, otherwise false
    """    
    return bool(self.emailAttachments)

  def get_attachment(self, index:int = 0) -> Union[EmailAttachment, None]:
    """Get email attachment from attachment list

    Args:
        index (int, optional): index of attachment. Defaults to 0.

    Returns:
        Union[EmailAttachment, None]: An instance of EmailAttachment if exists; otherwise, None
    """    
    if self.has_attachment():
      return self.emailAttachments[index]
    return None

  def get_received_on_datetime(self) -> datetime.datetime:
    """Get datetime timestamp of emailDate

    Returns:
        datetime.datetime: datetime of emailDate 
    """    
    return (datetime.datetime(self.emailDate[0], 
      self.emailDate[1], self.emailDate[2], self.emailDate[3], 
      self.emailDate[4], self.emailDate[5]) + datetime.timedelta(hours=0))

  def was_received_on(self, tergetedDate:datetime.datetime) -> bool:
    """Check whether the email was received on a targeted date or not

    Args:
        tergetedDate (datetime.datetime): targeted date to compare

    Returns:
        bool: True if email's received on targeted date; otherwise, False
    """    
    logger.info(self.get_received_on_datetime())
    return self.get_received_on_datetime().date == tergetedDate.date
