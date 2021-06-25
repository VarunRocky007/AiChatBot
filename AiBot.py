import pyjokes
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time
import json,requests
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

BaseUrl="https://api.openweathermap.org/data/2.5/weather?"
City="Chennai"
ApiKey="5d9f72dd9cceeb8c9a5514f941deb615"
URL = BaseUrl + "q=" + City + "&appid=" + ApiKey + "&units=metric"
response=requests.get(URL)
listener = sr.Recognizer()
engine=pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.say('Hi Varun')
engine.runAndWait()
time_now = datetime.datetime.now().strftime('%H')
if(int(time_now)>=12):
    engine.say('Good Afternoon')
else:
    engine.say('Good Morning')
engine.runAndWait()
count=0
def sleep(i):
    time.sleep(i)

def talk(text):
    engine.say(text)
    engine.runAndWait()
def take_command():
    command=""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.record(source,duration = 5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if("friday" in command):
                command = command.replace('friday' ,'')


    except:
        pass
    return command
def run_friday():
    global count
    command = take_command()
    if 'play' in command:
        song = command.replace('play','')
        talk('playing'+song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        talk("Current time is "+time)
    elif 'weather' in command:
        if response.status_code==200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            feelslike= main['feels_like']
            weather = data['weather']
            report = weather[0]['description']
            talk('The weather condition is'+str(temperature)+'degrees celsius and feels like'+str(feelslike)+'degrees celsius')
            talk('it is reported'+str(report)+"today")
        else:
            talk('couldnt connect to the servers now try again later')


    elif 'tell me about' in command:
        person = command.replace('tell me about','')
        info = wikipedia.summary(person,2)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'very funny' in command:
        talk('Yeah! I know ')
    elif 'volume' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume_ = command.replace('volume','')
        if 'full' in command:
            volume.SetMasterVolumeLevel(0,None)
            talk('Volume set to max level')
        else:
            volume_int=int(''.join(filter(str.isdigit, volume_)))

            # volume.SetMasterVolumeLevel(volume_int, None)
            min_volume=64
            wanted_volume=int((volume_int*min_volume)/100)-64
            print(volume.GetVolumeRange())
            print(wanted_volume)
            volume.SetMasterVolumeLevel(wanted_volume,None)



            talk('volume set to'+str(volume_int))
    elif 'nice to have you' in command:
        talk('You too')
    elif 'thank you' in command:
        talk('my pleasure')
    elif 'turn off' in command:
        talk("Ok buy have a nice day")
        return 0
    elif count < 3:
        sleep(10)
        count+=1
    else:
        talk("Going to standby mode")
        return 0

    return 1
run=1
while run:
    run=run_friday()