import JarvisAI
import os
import re
import pprint
import random
import warnings
import datetime
import pytz
from restcountries import RestCountryApiV2 as rapi
import requests
import json

warnings.filterwarnings("ignore")
warnings.warn("second example of warning!")

obj = JarvisAI.JarvisAssistant()


def speak(text):
    obj.text2speech(text)


def greet_user():
    """In this function Jarvis will greet the user"""
    greetings = ['Howdy', 'Hello', 'Hi there', 'bonjour', 'hi', 'hello there']
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speek(random.choice(greetings))
        speak('good morning!')
    else:
        speak(random.choice(greetings))
        speak('Welcome back, how may I help you!')


def country_check(query):
    # split query
    words = query.split()
    last_index = len(words) - 1
    # for loop to iterate over words array
    for idx, word in enumerate(words, start=0):
        try:
            if not re.search("MANY|MUCH|CASES|ARE|IN|IS", word):
                country_list = rapi.get_countries_by_name(word)
                country = country_list[0].alpha2_code

                return country
            else:
                continue
        except Exception as e:
            if last_index is not idx:
                continue
            else:
                return None


def start():
    """In this function Jarvis will send a response based on the query given by the user"""

    greet_user()
    while True:
        query = input('Enter your command:')
        query = query.upper()

        if re.search("COVID|CORONA|COVID 19|COVID NINETEEN|COVID19|COVID-19|CIVUD|CORONA VIRUS|MANY CASES IN", query):
            country = country_check(query)
            if country is None:
                world_covid_stats_url = 'https://corona.lmao.ninja/v3/covid-19/all'
                response = requests.get(world_covid_stats_url, headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    results = json.loads(response.content.decode('utf-8'))
                    print(
                        f'\nWorld Totals For: \n Cases Today: {results["todayCases"]}\n Deaths Today: {results["todayDeaths"]}\n Recoveries Today: {results["todayRecovered"]}\n'
                        f'\nOverall Totals Are:\n Total Cases: {results["cases"]}\n Total Deaths: {results["deaths"]}\n Total Recoveries: {results["recovered"]}')
                    speak(
                        f'World Totals For \n Cases Today are: {results["todayCases"]}\n , Deaths are: {results["todayDeaths"]}\n and Recoveries Today are: {results["todayRecovered"]}\n')
            if country:
                country_covid_stats_url = f'https://corona.lmao.ninja/v3/covid-19/countries/{country}?strict=true'
                response = requests.get(country_covid_stats_url, headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    results = json.loads(response.content.decode('utf-8'))
                    print(
                        f'\nTotals For {country}\n Cases Today: {results["todayCases"]}\n Deaths Today: {results["todayDeaths"]}\n Recoveries Today: {results["todayRecovered"]}\n'
                        f'\nOverall Totals Are:\n Total Cases: {results["cases"]}\n Total Deaths: {results["deaths"]}\n Total Recoveries: {results["recovered"]}')
                    speak(
                        f'Totals For \n Cases Today in {country} are: {results["todayCases"]}\n , Deaths are: {results["todayDeaths"]}\n and Recoveries Today are: {results["todayRecovered"]}\n')

        if re.search("JOKE|JOKES", query):
            joke_ = obj.tell_me_joke('en', 'neutral')
            speak('here is a joke')
            print(joke_)
            speak(joke_)

        if re.search('WEATHER|TEMPERATURE', query):
            city = res.split(' ')[-1]
            weather_res = obj.weather(city=city)
            print(weather_res)
            speak(weather_res)

        if re.search('NEWS', query):
            news_res = obj.news()
            pprint.pprint(news_res)
            speak(f"I have found {len(news_res)} news. You can read it. I'll tell you bout the first two")
            speak(news_res[0])
            speak(news_res[1])

        if re.search('TELL ME ABOUT', query):
            topic = query[14:]
            wiki_res = obj.tell_me(topic, sentences=1)
            print(wiki_res)
            speak(wiki_res)

        if re.search('YOUR NAME|WHO YOU ARE', query):
            print("I am your personal assistant")
            speak("I am your personal assistant")

        if re.search('what can you do', query):
            li_commands = {
                "covid stats": "Example: 'How many covid cases are there'",
                "open websites": "Example: 'open youtube.com",
                "time": "Example: 'what time it is?'",
                "date": "Example: 'what date it is?'",
                "tell me": "Example: 'tell me about India'",
                "weather": "Example: 'what weather/temperature in Mumbai?'",
                "news": "Example: 'news for today' ",
            }
            ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
            I can open websites for you, launch application and more. See the list of commands-"""
            print(ans)
            pprint.pprint(li_commands)
            speak(ans)

        if re.search('DATE', query):
            date = obj.tell_me_date()
            print(date)
            print(speak(date))

        if re.search('TIME', query):
            time = obj.tell_me_time()
            print(time)
            speak(time)

        if 'WIKIPEDIA' in query:
            speak('One sec')
            query = query.replace("Wikipedia", "")
            search_results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(search_results)
            speak(search_results)


if __name__ == "__main__":
    if not os.path.exists("config/config.ini"):
        # do set up and write to file or something
        if res:
            print("Settings Saved. Restart your Assistant")
    else:
        start()
