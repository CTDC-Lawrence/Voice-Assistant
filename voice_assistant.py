#importing libraries
import speech_recognition as sr
import pyttsx3
import datetime as dt
import webbrowser
import os
import wikipedia
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json

#initialize text to speech engine
engine = pyttsx3.init()

#initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="4db543dcdb4449c1b1c4596fa274fab9",
                                               client_secret="d7e989b88a2c4f4ebd9c894545f0a381",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

#initialize OpenWeatherMap API
owm_api_key = "INSERT_YOUR_OWM_API_KEY_HERE"

#speak function to output text as audio
def speak(text):
    engine.say(text)
    engine.runAndWait()

#wishMe function to greet user based on the time of day
def wishMe():
    hour = dt.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("You are so awesome. How may I help you?")

#takeCommand function to capture audio input from user and convert to text
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

#play_music function to stream user's saved tracks from Spotify
def play_music():
    results = sp.current_user_saved_tracks()
    track = results['items'][0]['track']
    track_uri = track['uri']
    sp.start_playback(uris=[track_uri])

#get_weather function to check the weather and chance of rain in user's location from OpenWeatherMap API
def get_weather():
    #use requests module to get user's location using ipinfo.io API
    ipinfo_response = requests.get("https://ipinfo.io/json?token=INSERT_YOUR_IPINFO_API_KEY_HERE")
    location_data = json.loads(ipinfo_response.text)
    city = location_data['city']
    region = location_data['region']

    #use requests module to get weather data from OpenWeatherMap API
    weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},{region}&appid={owm_api_key}&units=metric")
    weather_data = json.loads(weather_response.text)
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    rain_chance = weather_data.get('rain', {}).get('1h', 0)

    #output weather information
    speak(f"The temperature in {city} is {temp} degrees Celsius, and it feels like {feels_like} degrees Celsius. The sky is {description}. The humidity is {humidity} percent, and the wind speed is {wind_speed} meters per second. The chance of rain in the next hour is {rain_chance} millimeters.")
    print(f"The temperature in {city} is {temp} degrees Celsius, and it feels like {feels_like} degrees Celsius. The sky is {description}. The humidity is {humidity} percent, and the wind speed is {wind_speed} meters per second. The chance of rain in the next hour is {rain_chance} millimeters.") 


if name == 'main':
    wishMe()
    while True:
        query = takeCommand().lower()

    #searches for information on Wikipedia
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    #opens YouTube
    elif 'open youtube' in query:
        url = 'https://www.youtube.com'
        webbrowser.open(url)

    #opens Google
    elif 'open google' in query:
        url = 'https://www.google.com'
        webbrowser.open(url)

    #plays music from Spotify
    elif 'play music from spotify' in query:
        play_music()

    #responds with current time
    elif 'what time is it' in query:
        strTime = dt.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    #exits program
    elif 'exit' in query:
        speak("Goodbye!")
        break
