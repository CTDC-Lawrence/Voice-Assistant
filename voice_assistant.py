import speech_recognition as sr
import pyttsx3
import datetime as dt
import webbrowser
import os
import wikipedia
import spotipy
from spotipy.oauth2 import SpotifyOAuth

engine = pyttsx3.init()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="4db543dcdb4449c1b1c4596fa274fab9",
                                               client_secret="d7e989b88a2c4f4ebd9c894545f0a381",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = dt.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Please say that again...")
        return "None"
    return query

def play_music():
    results = sp.current_user_saved_tracks()
    track = results['items'][0]['track']
    track_uri = track['uri']
    sp.start_playback(uris=[track_uri])

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            url = 'https://www.youtube.com'
            webbrowser.open(url)

        elif 'open google' in query:
            url = 'https://www.google.com'
            webbrowser.open(url)

        elif 'play music from spotify' in query:
            play_music()

        elif 'what time is it' in query:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'exit' in query:
            speak("Goodbye!")
            break
