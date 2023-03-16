import time
import requests
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
from bs4 import BeautifulSoup
import smtplib

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
    server.login('ppurvi170@gmail.com', 'ap01122001')
    server.sendmail('ppurvi170@gmail.com', to, content)
    server.close()


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


        elif 'thank you' in query:
            speak("You are welcome!")
            break
