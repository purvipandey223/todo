import time
import requests
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
from bs4 import BeautifulSoup
import smtplib
import cv2
import os
from ecapture import ecapture as ec
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishME():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
        print("Good Morning")
    elif 12 <= hour < 18:
        speak("good afternoon!")
        print("good afternoon!")
    else:
        speak("Good evening!")
        print("Good Evening!!")
    speak("hello there! i am todo!how may i help you.")
    print("hello there! i am todo!how may i help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"user said:{query}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return query


def top_news():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    unwanted = ['BBC World News TV', 'BBC World Service Radio',
                'News daily newsletter', 'Mobile app', 'Get in touch']
    for x in list(dict.fromkeys(headlines)):
        if x.text.strip() not in unwanted:
            speak(x.text.strip())
            print(x.text.strip())


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('ppurvi170@gmail.com', '')
    server.sendmail('ppurvi170@gmail.com', to, content)
    server.close()


def weather(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    speak(location)
    speak(time)
    speak(info)
    speak(weather+"°C")


if __name__ == "__main__":
    wishME()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak("searching wikipedia.....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=4)
            speak("according to wikipedia")
            print(results)
            speak(results)

        elif "good bye" in query or "ok bye " in query or "shut down" in query:
            speak("your personal assistant todo is shutting down...")
            break

        elif 'open youtube' in query:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Youtube is open..")
            time.sleep(5)

        elif "open google" in query:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is open..")
            time.sleep(5)

        elif "open gmail" in query:
            webbrowser.open_new_tab("gmail.com")
            speak("Google mail is open..")
            time.sleep(5)

        elif "news" in query:
            top_news()

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")


        elif 'email to purvi' in query:
            try:
                speak("what should i say?")
                content = takeCommand()
                to = "purvipandey063@gmail.com"
                sendEmail(to, content)
                speak("email is sent!")
            except Exception as e:
                print(e)
                speak("sorry email can't be sent")


        elif 'thank you' in query or 'stop' in query:
            speak("You are welcome!")
            break


        elif "take a photo" in query:
            ec.capture(0, "robo camera", "img.jpg")


        elif 'alarm' in query:
            speak("Please tell me the time to set alarm?")
            tt = takeCommand()
            tt = tt.replace("set alarm to ", "")
            tt = tt.upper()
            import myalarm

            myalarm.alarm(tt)

        elif 'how to much battery left ' in query or 'how power' in query or 'battery' in query:
            import psutil

            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f" our system have {percentage} percent battery")


        elif 'camera' in query or 'picture' in query:
            cap = cv2.VideoCapture()
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
                cap.release()
                cv2.destroyAllWindows()


        elif 'internet speed' in query:
            import speedtest

            try:
                os.system('cmd /k "speedtest"')
            except:
                speak("There is no internet connection")


        elif 'send message' in query:
            speak("What should i say?")
            msg = takeCommand()

            from twilio.rest import Client

            account_sid = 'ACb88a2beee5819c9bccd3d840e563400c'
            auth_token = '13de74f4d35a68d984e5a55c48adf8ed'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=msg,
                from_='+15075025948',
                to='+917587169427'
            )

            print(message.sid)
            speak("Message is sent!!")



        elif 'call' in query:

            from twilio.rest import Client

            accountSid = 'ACb88a2beee5819c9bccd3d840e563400c'
            authToken = '13de74f4d35a68d984e5a55c48adf8ed'

            client = Client(accountSid, authToken)

            message = client.calls.create(
                twiml='<Response><Say>Hello Purvi!...</Say></Response>',
                from_='+15075025948',
                to='+917587169427'
            )
            print(message.sid)

        elif 'current temperature' in query:

            speak("what location weather?")
            search = takeCommand()
            weather(search)

