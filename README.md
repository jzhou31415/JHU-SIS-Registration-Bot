# JHU SIS Registration Bot
Up to date Selenium based registration bot for JHU SIS course registration, registering for courses right as the clock turns 7:00 AM. This bot will also add you to any waitlist for classes that are unavailable.
## Setup
Download Python 3 ([Windows](https://www.python.org/downloads/windows/), [MacOS](https://www.python.org/downloads/macos/))

Run the following in Powershell with Admin privileges (Windows) or Terminal (MacOS):

    pip install -U selenium
Next install ``chromedriver`` using a package installer such as Chocolatey (Chocolatey: [Windows](https://chocolatey.org/install#install-step1), Homebrew: [MacOS](https://brew.sh/)) with the following commands:

Chocolatey: ```choco install chromedriver```

Homebrew: ```brew install chromedriver```

Make sure your Google Chrome is also up to date. Then download the file ``SIS_bot.py`` . Next we have to change our computer's clock to be in sync with US Naval Time which is what SIS uses.
1. Go to settings and then date & time settings
2. Change the Time Server (under 'Sync Now' for Windows) from the default to "tick.usno.navy.mil"
3. Save changes and exit
## Usage
Make sure all of your classes are already in your SIS cart before running using. Then run the following command in Command Prompt/Terminal at least 1 minute before 7:00 AM on registration day

    python "path to SIS_bot.py"
Replacing "path to SIS_bot.py" with the actual path which on windows looks like the following:

    python "C:\Users\USERNAME\Downloads\SIS_Bot.py"
Now you can sit back and wait while the bot while automatically register you for all of your classes at 7:00 AM
