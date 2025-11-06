# JHU SIS Registration Bot
Up to date Selenium based registration bot for JHU SIS course registration, registering for courses right as the clock turns 7:00 AM. This bot will also add you to any waitlist for classes that are unavailable.
## Setup
Download Python 3 ([Windows](https://www.python.org/downloads/windows/), [MacOS](https://www.python.org/downloads/macos/)) if you do not have it already installed.

Run the following in Powershell with Admin privileges (Windows) or Terminal (MacOS):

    pip install -U selenium

Make sure your Google Chrome is also up to date. Then download the file ``SIS_bot.py`` . Next we have to change our computer's clock to be in sync with US Naval Time which is what SIS uses.
1. Go to settings and then date & time settings
2. Change the Time Server (under 'Sync Now' for Windows) from the default to "tick.usno.navy.mil"
3. Save changes and exit

## Usage
Make sure all of your classes are already in your SIS cart before running using. Then run the following command in Command Prompt/Terminal on registration day at least 1 minute (ideally 5 minutes) before 7:00 AM on registration day

    python "path to SIS_bot.py"
Replacing "path to SIS_bot.py" with the actual path which on windows looks like the following:

    python "C:\Users\USERNAME\Downloads\SIS_Bot.py"
Now you can sit back and wait while the bot while automatically register you for all of your classes at 7:00 AM

Or simply launch the ``.py`` file.
