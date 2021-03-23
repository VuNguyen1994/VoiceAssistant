Name: Vu Nguyen
Project: Voice Assistant App in Python3

The app is designed to assist visual impaired users with daily tasks by voice commands. Once registered, it will remain
at standby mode and continuously listen for wake-word 'computer' using Porcupine API to be activated. After that, it
uses Google Speech Recognition API to detect the voice commands. Depending on the input voice commands, it will call to
different API micro-services and use Google Text-to-Speech to speak up the data to answer or perform the assistance
features for the users such as answer questions, find locations, search webs or read the news...

It will return to standby or listening mode when it hears a 'Good Bye' command. After that, it can be reactivated by the
wake-word 'Computer' or closed by 'Terminator' command.


Step 1: Start Python3 venv and install the required libraries and packages in requirements.txt file
Init virtual env by python3 -m venv venv
Activate venv by Linux: source ./venv/bin/activate. Windows: .\venv\Scripts\activate
Install the packages by pip install -r requirements.txt

Note:
The pyaudio will send an error for not finding the wheels file for installation.
To download the wheel file to install pyaudio (use with microphone) with correct python version and 64/32 bit:
Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
Download specific python version and the bit version of Windows
Locate to the downloaded location/folder
Run command: pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl

Step 2: From the venv, run the script by python voice.py

Step 3: Register with your Name, Email and Password and click save to start using the app.

Step 4: The app will start at standby mode and waiting for wake word: "Computer". Say "Computer" and the app activates.
It will keep listening for commands such as search, what is your name, what time, who is Bill Gates, what is an apple...

Step 5: To set the app back to standby mode, say "Good Bye".

Step 6: To reactivate the app, say the keyword "Computer". Or to close the app, say "Terminator"

******************

Note:
The email and messaging feature is not fully implemented. Some configurations on the provided emails must be automated
in order to get access and permission to send emails or messages for the users.
