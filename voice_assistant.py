#importing libraries
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import requests
import openai
import re

#initialize text to speech engine
engine = pyttsx3.init()

#initialize OpenWeatherMap API
owm_api_key = "7adbd8fc202a95b42705fc9bb2f95470"

# Authenticate with your API key and organization ID
openai.api_key = "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"
openai.organization = "org-gHdIY8iFlQ3XWGjF4Jsxalio"

#speak function to output text as audio
def speak(text):
    engine.say(text)
    engine.runAndWait()

#wishMe function to greet user based on the time of day
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("You are so awesome. How may I help you?")

def handle_sales_objections():
    while True:
        speak("Sure, what's the question?")
        objection = takeCommand().lower()

        # Define the prompt for the GPT-3 API
        prompt = f"Overcome the following customer objection:\n\nQ: {objection}\nA: "

        # Generate a response using the GPT-3 API
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=250,
            n=1,
            stop=None,
            temperature=0.3,
        )

        # Extract the response text from the API response
        answer = response.choices[0].text.strip()

        # Print and speak the answer without the prompt
        print(answer)
        speak(answer)

        # Ask the user if they have any additional questions
        speak("Do you have any additional questions?")
        additional_question = takeCommand().lower()

        # Exit the sales objection loop if the user says "exit" or "no"
        if "stop" in additional_question or "no" in additional_question or "exit" in additional_question:
            break

#get the time
def get_current_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    return time_str

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

# get_weather function to check the weather and chance of rain in user's location from OpenWeatherMap API
def get_weather():
    zip_code = "33309"
    country_code = "us"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={owm_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("main"):
        weather = data["main"]
        temperature_c = weather["temp"]
        temperature_f = (temperature_c * 9/5) + 32 #convert to Fahrenheit
        humidity = weather["humidity"]
        pressure = weather["pressure"]
        print(f"The temperature is {temperature_f:.1f}°F and humidity is {humidity}% with a pressure of {pressure}hPa")
        speak(f"The temperature is {temperature_f:.1f}°F and humidity is {humidity}% with a pressure of {pressure}hPa")
    else:
        print("Couldn't fetch weather data for given location")

if __name__ == '__main__':
    wishMe()

    while True:
        query = takeCommand().lower()

        # searches for information on Wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Handle Sales Objections
        elif 'sales question' in query:
            handle_sales_objections()

        # opens YouTube and search for a video
        elif 'youtube' in query:
            speak("What should I search for?")
            search_term = takeCommand().lower()
            speak("Here is what I found for " + search_term)
            webbrowser.get().open("https://www.youtube.com/results?search_query=" + search_term)

        # checks the weather
        elif 'weather' in query:
            speak("Checking the weather...")
            get_weather()

        # gets the current time
        elif 'time' in query:
            current_time = get_current_time()
            speak(f"The time is {current_time}")

        # exits the program
        elif 'exit' in query or 'stop' in query or 'no' in query:
            speak("Goodbye!")
            break
