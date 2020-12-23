import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
#from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import sys

import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup

import pafy
import vlc
import urllib.request



name = "Genesis"
fullName = "Just a Rather Very Intelligent System"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)



def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello, Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")

    speak("My name is" + name)

def calAmbientNoise():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source, duration=7)

def takeCommand():
    # reCalTime = (int)(datetime.datetime.now().strftime("%H%M%S"))

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio)
            print(f"user said:{statement}\n")

        except Exception as e:
            # speak("Pardon me, please say that again")
            return ""
        return statement


def botcode():

    instance = vlc.Instance()
    player = instance.media_player_new()

    player.audio_set_volume(50)

    while True:

        reCalTime = datetime.datetime.now().strftime("%H%M%S")

        if (int)(reCalTime) % 3 == 0:
            print("Recal")
            #speak('Please give me a moment')
            calAmbientNoise()

        statement = takeCommand()

        somethingHappen = 0

        if 'stop music' in statement:
            somethingHappen = 1
            player.stop()

        elif 'pause music' in statement:
            somethingHappen = 1
            player.pause()

        elif 'resume music' in statement:
            somethingHappen = 1
            player.play()

        if name in statement:

            statement = statement.replace(name, "")

            while somethingHappen == 0:

                player.audio_set_volume(25)
                # speak("How can I help you now?")

                # statement = takeCommand()

                if "goodbye" in statement or "ok bye" in statement:
                    speak('Hope to assist you again in the future')
                    sys.exit()

                if 'Wikipedia' in statement :
                    somethingHappen = 1
                    speak('Searching Wikipedia...')
                    statement = statement.replace("Wikipedia", "")
                    results = wikipedia.summary(statement, sentences=3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                if 'explain' in statement :
                    somethingHappen = 1
                    speak('Searching Wikipedia...')
                    statement = statement.replace("explain", "")
                    try:
                        results = wikipedia.summary(statement, sentences=3)
                        speak("According to Wikipedia")
                        print(results)
                        speak(results)
                    except:
                        statement = 'compute' + statement

                elif 'open YouTube' in statement:
                    somethingHappen = 1
                    webbrowser.open_new_tab("https://www.youtube.com")
                    speak("youtube is open now")
                    time.sleep(5)

                elif 'open Google' in statement:
                    somethingHappen = 1
                    webbrowser.open_new_tab("https://www.google.com")
                    speak("Google chrome is open now")
                    time.sleep(5)

                elif 'open Gmail' in statement:
                    somethingHappen = 1
                    webbrowser.open_new_tab("gmail.com")
                    speak("Google Mail open now")
                    time.sleep(5)

                elif 'time' in statement:
                    somethingHappen = 1
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"the time is {strTime}")

                elif 'news' in statement:
                    somethingHappen = 1
                    news = webbrowser.open_new_tab("https://www.theglobeandmail.com/")
                    speak('Here are some headlines from the Globe and Mail')
                    time.sleep(6)

                elif 'compute' in statement:
                    somethingHappen = 1
                    #speak('I can answer to computational and geographical questions, Ask away!')
                    question = statement
                    app_id = "56TEK8-3VYL9PY445"
                    client = wolframalpha.Client('R2K75H-7ELALHR35X')

                    try:
                        res = client.query(question)
                        answer = next(res.results).text
                        speak(answer)
                        print(answer)
                    except:
                        speak('Does not compute')

                elif "weather" in statement:
                    somethingHappen = 1
                    api_key = "a31b9313e814f31c286e1f79e9481f56"
                    base_url = "https://api.openweathermap.org/data/2.5/weather?"
                    speak("what is the city name")

                    city_name = takeCommand()

                    while city_name == "":
                        city_name = takeCommand()

                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                    response = requests.get(complete_url)
                    x = response.json()
                    if x["cod"] != "404":
                        y = x["main"]
                        current_temperature = y["temp"]
                        current_humidiy = y["humidity"]
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        speak(" Temperature in celsius unit is " +
                              str((int)(current_temperature - 273.15)) +
                              "\n humidity in percentage is " +
                              str(current_humidiy) +
                              "\n description  " +
                              str(weather_description))
                        print(" Temperature in kelvin unit = " +
                              str(current_temperature) +
                              "\n humidity (in percentage) = " +
                              str(current_humidiy) +
                              "\n description = " +
                              str(weather_description))

                elif 'search' in statement:
                    somethingHappen = 1
                    statement = statement.replace("search", "")
                    webbrowser.open_new_tab('https://www.google.com/search?q=' + statement)
                    time.sleep(5)

                elif 'stop music' in statement:
                    somethingHappen = 1
                    player.stop()

                elif 'pause music' in statement:
                    somethingHappen = 1
                    player.pause()

                elif 'resume music' in statement:
                    somethingHappen = 1
                    player.play()

                elif 'play' in statement:

                    somethingHappen = 1

                    music_name = statement.replace('play', '')

                    while music_name == " ":
                        speak('Name the song')
                        music_name = takeCommand()

                    speak('playing' + music_name)

                    query_string = urllib.parse.urlencode({"search_query": music_name})

                    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

                    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())

                    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
                    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])

                    print(clip2)

                    inspect = BeautifulSoup(clip.content, "html.parser")
                    yt_title = inspect.find_all("meta", property="og:title")

                    for concatMusic1 in yt_title:
                        pass

                    url = clip2

                    #webbrowser.open_new_tab(url)

                    video = pafy.new(url)
                    best = video.getbest()
                    playurl = best.url

                    media = instance.media_new(playurl)
                    media.get_mrl()
                    player.set_media(media)
                    player.play()

                    player.audio_set_volume(50)

                    calAmbientNoise()

                elif 'files' in statement:
                    somethingHappen = 1
                    file1 = open('output.txt', "r+")

                    command = ""

                    while command != 'close file':
                        command = takeCommand()

                        if 'right' in command:
                            file1.write(command.replace('right', '') + "\n")

                        elif 'read' in command:
                            speak(file1.readlines())

                        elif command == 'close file':
                            break

                    file1.close()

                else:
                    speak('At your service')
                    statement = takeCommand()



#wishMe()

speak("How can I help you now?")


if __name__=='__main__':

    botcode()
