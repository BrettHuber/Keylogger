# Multi-Type Python Keylogger
The program is a python keylogger that reports at a set time interval. In main, there are multiple keylogger threads each with a different report type. These report types include File, Email, Slack, Discord, SMS, and Skype. In the report method, its calls createFileIndentifier, which uses datetime to construct an id of the keylog interval. This value is used to name the file when reported through File. createID is used as the subject when reported through Email, and used as the first line before entering for Discord and Slack. 

To utilize this program you must set the specific time interval (in seconds) to the value of LOG_INTERVAL. Right now its set to 60 seconds. Also, set EMAIL to your email address and EMAIL_PW to your email password. When choosing which report method to utilize uncomment that intended method and comment the rest. 
Create .env file and added the following lines to the file: 
    export SLACK_BOT_TOKEN = "Insert-Token"
    export DISCORD_WEBHOOK = "Insert Webhook URL"
    export PHONE_NUMBER = "Insert AT&T Phone Number (ex: 9731234567)". 
Replace Insert-Token with actual slack bot token, Insert Webhook URL with discord webhook url, and Insert AT&T Phone Number (ex: 9731234567) with actual phone number.
