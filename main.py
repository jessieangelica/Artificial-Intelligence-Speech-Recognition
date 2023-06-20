import speech_recognition as sr
import webbrowser
import time
import random
import pyttsx3
import pywhatkit
import requests
import psutil
import speedtest
from bs4 import BeautifulSoup

class person:
    name = ''
    def setName(self, name):
        self.name = name
        
def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer()

def record_audio(ask = False):
    with sr.Microphone() as source: # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source) # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio) # convert audio to text
        except sr.UnknownValueError:   # error: recognizer does not understand
            speak('Sorry, I did not get that')
        except sr.RequestError:
            speak('Sorry, my speech service is down')  # error: recognizer is not connected
        return voice_data
    
    
    
engine = pyttsx3.init('sapi5')
voice_data = engine.getProperty('voices')
engine.setProperty('rate', 130)
engine.setProperty('voice', voice_data[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    
def respond(voice_data):
    # 1: greeting
    if there_exists(['hey','hi','hello']):
        greetings = [f"what's up? {person_obj.name}", 
                     f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)
        
    # 2: name
    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name) # remember name in person object
        
    # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    # 4: time
    if there_exists(["what's the time","tell me the time","what time is it"]):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        speak(f'The current time is {current_time}')

    # 5: search google
    if there_exists(["search on Google"]):
        search = record_audio('What do you want to search for')
        url = f"https://www.google.com/search?q={search}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search} on Google')

    # 6: search for location
    if  there_exists(["find location"]):
        location = record_audio('What is the location')
        url = 'https://www.google.com/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speak('Here is the location of ' + location)

    # 7: search youtube
    if there_exists(["search on YouTube"]):
        youtube = record_audio('What do you want to search for')
        url = f"https://www.youtube.com/results?search_query={youtube}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {youtube} on youtube')

    # 8: play youtube
    if there_exists(["Play on YouTube"]):
        youtube = record_audio('What do you want me to play?')
        speak(f'Playing {youtube} on youtube')
        pywhatkit.playonyt(youtube)

    # 9: temperature
    if there_exists(["what is the temperature in "]):
        temperature = 'temperature in ' + voice_data.split("in")[-1].strip()
        url = f"https://www.google.com/search?q={temperature}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"The current {temperature} is {temp}")

    # 10: battery
    if there_exists(["battery check"]):
        battery = psutil.sensors_battery()
        percentage = battery.percent
        speak(f"You have {percentage} percent battery left")
        if percentage >= 50:
            speak("You have enough battery to continue your work")
        elif percentage >= 25 and percentage < 50:
            speak("You should prepare to charge your device because the battery will be on low power soon")
        elif percentage >= 15 and percentage < 25:
            speak("You don't have enough power to do rough work with your device, please charge it as soon as possible")
        elif percentage < 15:
            speak("Your device is on very low power, please charge it now or the device will shutdown very soon")

    # 11: internet speed
    if there_exists(["internet speed check"]):
        st = speedtest.Speedtest()
        dl = st.download()
        up = st.upload()
        speak(f"You have {dl} bit per second downloading speed and {up} bit per second uploading speed")
        
    if 'thank you' in voice_data:
        speak('You are welcome')
        exit()


time.sleep(1)

person_obj = person()
speak('Hello, my name is Dita. How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)