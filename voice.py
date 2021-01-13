# Speech Assistant App

# Start virtual environment by python3 -m venv venv
# Linux: source ./venv/bin/activate. Windows: .\venv\Scripts\activate
# Ctrl Shift P, Python: Select Intepreter
# To run app, python voice.py

# Required Libraries:
# 1) Google Speech Recognition API by pip install speechrecognition
# 2) download the wheel file to install pyaudio (use with microphone) with correct python version and 64/32 bit:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Run install by go to C:\Users\levud\Downloads> 
# run command: pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
# 3) Google Translate Text-to-Speech API by pip install gTTS
# 4) Playsound to play the audio file immediately by pip install playsound
# 5) If MacOS, install PyObjC (for playsound to work) by pip install PyObjC. Can't install in Windows
# 6) Install pvporcupine for the Wake Word by pip3 install pvporcupine
# 7) Install pip install wikipedia, pip install ecapture (camera), pip install pyjokes, pip install twilio (phonecall, msg)
# pip install requests (GET and POST requests), pip install beautifulsoup4 (scrape info from webpages)

# python -m pip install kivy[full] kivy_examples
# pip install pygame

import speech_recognition as sr
import webbrowser
import time
import sys
import playsound
from gtts import gTTS
import os
import random
from time import ctime
import struct
import pyaudio
import pvporcupine
import wikipedia
import pyjokes
import smtplib
from twilio.rest import Client
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Init Speech Recognizer
r = sr.Recognizer()

# Global Variable
state = ''                              # Control the state machine of the application: Idle, Standby, Running, Close   
email_id = os.getenv('email_id')        # Get email ID - will be changed to server email so send noti to user
email_pw = os.getenv('email_pw')        # Get email password
username = ''                           # Get user name

# Utilities functions
def record_audio(ask = False):
    """
    record audio and turn it into text
    """
    with sr.Microphone() as source:
        if ask:
            speakup(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            print('Unknown Value Error. Could not recognize speech!')
        except sr.RequestError:
            speakup('Sorry, my speech service is down')
        return voice_data


def speakup(audio_string):
    """
    call google text to speech to build the audio file and speak up the text string
    """
    text2speech = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 100000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    text2speech.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def sendEmail(receiver_name, content):
    global email_id, email_pw
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Enable low security in gmail
    server.login(email_id, email_pw)
    server.sendmail(email_id, record_audio, content)
    server.close()


def respond(voice_data):
    """
    handle voice data inputs and call speakup() to convert the text responds to speech
    """
    global state
    print (voice_data)
    if 'what is your name' in voice_data:
        speakup('My name is Google assistant')
    elif 'how are you' in voice_data:
        speakup('I am happy to help you')
    elif 'what time is it' in voice_data:
        speakup(ctime())
    elif 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        speakup('Here is what I found for ' + search)
    elif 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speakup('Here is the location of ' + location)
    elif 'what is' in voice_data:
        try:
            voice_data = voice_data.replace("what is", "")
            results = wikipedia.summary(voice_data, sentences=3)
            speakup("According to Wikipedia, " + results)
        except:
            speakup('Sorry. I did not get that.')
    elif 'who is' in voice_data:
        try:
            voice_data = voice_data.replace("who is", "")
            results = wikipedia.summary(voice_data, sentences=3)
            speakup("According to Wikipedia, " + results)
        except:
            speakup('Sorry. I did not get that.')
    elif 'Wikipedia' in voice_data:
        voice_data = voice_data.replace("Wikipedia", "")
        if voice_data in [ " " , "" ]:
            speakup("Opening wikipedia")
            webbrowser.get().open('https://en.wikipedia.org/wiki/Main_Page')
        else:
            try:
                results = wikipedia.summary(voice_data, sentences=3)
                speakup("According to Wikipedia, " + results)
            except:
                speakup('Sorry. I did not get that.')
    elif 'YouTube' in voice_data:
        speakup("Opening Youtube.")
        webbrowser.get().open("https://www.youtube.com")
    elif 'joke' in voice_data:
        speakup(pyjokes.get_joke())
    elif 'weather' in voice_data:
        # Get Google weather API to implement this
        pass
    elif 'news' in voice_data:
        try:
            jsonObj = urlopen('''https://newsapi.org/v2/top-headlines?country=us&apiKey=0be76b6239244410b3440ccfd51cc17d''')
            data = json.load(jsonObj)
            i = 1
            
            speakup('here are some top news in the US')
            print('''=============== UNITED STATES NEWS ============'''+ '\n')
            
            for item in data['articles']:
                #print(str(i) + '. ' + item['title'] + '\n')
                speakup(str(i) + '. ' + item['title'] + '\n')
                print(item['description'] + '\n')
                i += 1
        except Exception as e:
            print(str(e))
    elif ('email' in voice_data) or ('mail' in voice_data):
        try:
            receiver_name = record_audio('Who should I send it to?')
            content = record_audio('What should I say?')
            sendEmail(receiver_name, content)
            speakup("The email has been sent!")
        except Exception as e:
            print(e)
            speakup("I am not able to send this email")
    elif "send message" in voice_data:
        # Create an acct on Twilio to use this
        try:
            account_sid = 'Account Sid Key'
            auth_token = 'Auth token'
            client = Client(account_sid, auth_token)
            message = client.messages.create(body = record_audio('what should I say in the content?'),
                                            from_= record_audio('Sender Number'),
                                            to = record_audio('Receiver Number') 
                                            ) 
        except Exception as e:
            print(e)
            speakup("I am not able to send this message")
    elif 'goodbye' in voice_data:
        speakup('OK. See you later!')
        speakup('Application change to standby mode.')
        state = 'Standby'
    elif voice_data in [ " " , "" ]:
        speakup('Sorry. I did not get that.')
    else:
        url = 'https://google.com/search?q=' + voice_data
        webbrowser.get().open(url)
        speakup('Here is what I found for ' + voice_data)


# App Layout by Kivy
class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Name: "))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.inside.add_widget(Label(text="Password: "))
        self.pw = TextInput(multiline=False)
        self.inside.add_widget(self.pw)

        self.add_widget(self.inside)

        self.saveBtn = Button(text="Save", font_size=40)
        self.saveBtn.bind(on_press=self.BtnPressed)
        self.add_widget(self.saveBtn)

    def BtnPressed(self, instance):
        global email_id, email_pw, username
        email_id = self.email.text          # Get email ID - will be changed to server email so send noti to user
        email_pw = self.pw.text             # Get email password
        username = self.name.text           # Get user name
        print('Info Saved: Name: ' + username + ', Email ID: ' + email_id + ', Email Password: ' + email_pw)
        self.name.text = ""
        self.email.text = ""
        self.pw.text = ""
        self.mainProcedure()
    
    def mainProcedure(self):
        global email_id, email_pw, username, state
        porcupine = None
        pa = None
        audio_stream = None
        state = 'Standby'
        try:
            speakup('Start application for username: ' + username)
            porcupine = pvporcupine.create(keywords=["blueberry", "terminator"],
                                                        sensitivities=[0.7, 0.7])
            # For DEBUG
            # print(pvporcupine.KEYWORDS)
            # Getting Audio Stream and sample it into frames with default values of porcupine
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                            rate=porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=porcupine.frame_length)
            while state == 'Standby':
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                # Call porcupine to process each PCM for wake word
                keyword_index = porcupine.process(pcm)
                if keyword_index == 0:
                    print("Wake Word Detected")
                    state = 'Running'
                    speakup('Hi. How can I help you?')
                if keyword_index == 1:
                    speakup("Application Closed.")
                    state = 'Close'
                #time.sleep(0.5)
                while state == 'Running':
                    voice_data = record_audio()
                    respond(voice_data)
        finally:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()
            sys.exit(0)


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    # Start the App, wait for user inputs and Start Button
    MyApp().run()
