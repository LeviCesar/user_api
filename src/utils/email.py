from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_SERVER

class Email:
    __sender: str
    __to: list
    __subject: str
    __message: str
    
    __server: str
    
    def __init__(self, email_sender: str = EMAIL_ADDRESS, to: list = []) -> None:
        self.sender = email_sender
        self.to = to
    
    @property
    def sender(self) -> str:
        return self.__sender
    
    @sender.setter
    def sender(self, value: str) -> None:
        self.__sender = value
        
    @property
    def to(self) -> list:
        return self.__to
    
    @to.setter
    def to(self, to_list: list) -> None:
        self.__to = to_list
    
    @property
    def message(self) -> str:
        return self.__message
    
    @message.setter
    def message(self, value: str) -> None:
        self.__message = value
    
    @property
    def subject(self) -> str:
        return self.__subject
    
    @subject.setter
    def subject(self, value: str) -> None:
        self.__subject = value
    
    @property
    def server(self) -> SMTP:
        return self.__server
    
    @server.setter
    def server(self, value: str) -> None:
        self.__server = value
    
    def connect_server(self, password: str = EMAIL_PASSWORD) -> None:
        self.server = SMTP(host='smtp.gmail.com', port=587)
        self.server.starttls()
        print(self.sender)
        print(password)
        self.server.login(user=self.sender, password=password)
    
    def quit_server(self) -> None:
        self.server.quit()
        
    def send_email(self) -> bool:
        msg = MIMEMultipart()
        
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.to)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message, 'plain'))
        
        self.server.send_message(self.sender, self.to, msg.as_string())
        self.quit_server()
        
        return True