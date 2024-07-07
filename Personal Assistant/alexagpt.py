import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import sys
import wikipediaapi
from googlesearch import search
from gtts import gTTS
from googletrans import Translator
from playsound import playsound
import os

# Initialize the recognizer and the text-to-speech engine
assistant_name = input("Enter the name of your Assistant: ")
listener = sr.Recognizer()
engine = pyttsx3.init()
mic = str(input("Is your mic working properly? Type (yes/no): "))

# Set the voice
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

# Initialize the translator and Wikipedia API
translator = Translator()
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="YourAppName/1.0 (YourContactInfo or URL)"
)

def engine_talk(text, lang='ta'):
    print(f"{assistant_name} is saying: {text}")
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

def user_commands():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Start Speaking!!")
            voice = listener.listen(source)
            try:
                command = listener.recognize_google(voice, language='ta-IN')
                print(f"Recognized Tamil command: {command}")
                return command.lower(), 'ta'
            except sr.UnknownValueError:
                command = listener.recognize_google(voice, language='en-IN')
                print(f"Recognized English command: {command}")
                return command.lower(), 'en'
    except Exception as e:
        print(f"Error: {e}")
        return "", ""

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def get_wikipedia_summary(name):
    page = wiki_wiki.page(name)
    if page.exists():
        return page.summary.split('\n')[0]  # Return the first paragraph
    else:
        return "Sorry, I could not find any information on Wikipedia."

def handle_command(command, lang):
    if 'play' in command:
        song = command.replace('play', '').strip()
        translated_text = translator.translate(f'Playing {song}', src='en', dest='ta').text
        engine_talk(translated_text)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        translated_text = translator.translate(f'The current time is {time}', src='en', dest='ta').text
        engine_talk(translated_text)
    elif 'who is' in command:
        name = command.replace('who is', '').strip()
        try:
            summary = get_wikipedia_summary(name)
            translated_text = translator.translate(summary, src='en', dest='ta').text
            engine_talk(translated_text)
        except Exception as e:
            translated_text = translator.translate(f'I encountered an error: {e}', src='en', dest='ta').text
            engine_talk(translated_text)
    elif 'what is' in command:
        name = command.replace('what is', '').strip()
        try:
            summary = get_wikipedia_summary(name)
            translated_text = translator.translate(summary, src='en', dest='ta').text
            engine_talk(translated_text)
        except Exception as e:
            translated_text = translator.translate(f'I encountered an error: {e}', src='en', dest='ta').text
            engine_talk(translated_text)
    elif 'define' or 'Define 'in command:
        name = command.replace('define', '').strip()
        try:
            summary = get_wikipedia_summary(name)
            translated_text = translator.translate(summary, src='en', dest='ta').text
            engine_talk(translated_text)
        except Exception as e:
            translated_text = translator.translate(f'I encountered an error: {e}', src='en', dest='ta').text
            engine_talk(translated_text)
    
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        translated_joke = translator.translate(joke, src='en', dest='ta').text
        engine_talk(translated_joke)
    elif 'stop' in command:
        translated_text = translator.translate('Goodbye!', src='en', dest='ta').text
        engine_talk(translated_text)
        sys.exit()
    else:
        response = get_chatgpt_response(command)
        translated_response = translator.translate(response, src='en', dest='ta').text
        engine_talk(translated_response)

def handle_command_with_input():
    command = str(input("Enter the command: "))
    handle_command(command, 'en')

def run_alexa():
    print(f"Hi, I'm {assistant_name}. How can I help you today?")
    while True:
        if mic.lower() == "yes":
            command, lang = user_commands()
            if command:
                handle_command(command, lang)
        elif mic.lower() == "no":
            handle_command_with_input()
        else:
            print("Please enter yes or no only.")
            break

if __name__ == "__main__":
    run_alexa()

'''import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import sys
from googlesearch import search

# Initialize the recognizer and the text-to-speech engine
assistant_name = input("Enter the name of your Assistant: ")
listener = sr.Recognizer()
engine = pyttsx3.init()
mic = str(input("Is your mic working properly? Type (yes/no): "))

# Set the voice
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

# Set up OpenAI API key
openai.api_key = ''

def engine_talk(text):
    print(f"{assistant_name} is saying: {text}")
    engine.say(text)
    engine.runAndWait()

def user_commands():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if assistant_name.lower() in command:
                command = command.replace(assistant_name.lower(), '')
                print(f"Hey there, you are saying my name: {command}")
                return command.strip()
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def handle_command(command):
    if 'play' in command:
        song = command.replace('play', '').strip()
        engine_talk(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk(f'The current time is {time}')
    elif 'who is' in command:
        name = command.replace('who is', '').strip()
        try:
            query = f"who is {name}"
            search_results = list(search(query, num_results=1))
            if search_results:
                info = search_results[0]
                print(info)
                engine_talk(f"Here's what I found: {info}")
            else:
                engine_talk(f'Sorry, I could not find any information on {name}.')
        except Exception as e:
            engine_talk(f'I encountered an error: {e}')
    elif 'joke' in command:
        engine_talk(pyjokes.get_joke())
    elif 'stop' in command:
        engine_talk('Goodbye!')
        sys.exit()
    else:
        response = get_chatgpt_response(command)
        engine_talk(response)

def handle_command_with_input():
    command = str(input("Enter the command: "))
    handle_command(command)

def run_alexa():
    print(f"Hi, I'm {assistant_name}. How can I help you today?")
    while True:
        if mic.lower() == "yes":
            command = user_commands()
            if command:
                handle_command(command)
        elif mic.lower() == "no":
            handle_command_with_input()
        else:
            print("Please enter yes or no only.")
            break

if __name__ == "__main__":
    run_alexa()'''
