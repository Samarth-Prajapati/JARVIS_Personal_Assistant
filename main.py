import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = 'd6cfcc8f5bf04993b11f147b38618784'

def speak_alternate_version(text):
    engine.say(text)
    engine.runAndWait()

def speak( text ) :
    tts = gTTS( text )
    tts.save( 'temp.mp3' )
    pygame.mixer.init()
    pygame.mixer.music.load( 'temp.mp3' )
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() :
        pygame.time.Clock().tick( 10 )
    pygame.mixer.music.unload()
    os.remove( 'temp.mp3' )


def processCommand( command ) :
    command = command.lower().strip()
    if 'open' in command:
        parts = command.split(' ')
        if len(parts) > 1:
            application = parts[ 1 ]
            webbrowser.open(f'https://{application}.com')
        else:
            print("No application specified to open.")
    elif 'play' in command:
        parts = command.split(' ')
        if len(parts) > 1:
            song = parts[ 1 ]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                print(f"No link found for song: {song}")
        else:
            print("No song specified to play.")
    elif 'news' in command :
        r = requests.get( f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}' )
        if r.status_code == 200 :
            data = r.json()
            articles = data.get( 'articles' , [] )
            for article in articles :
                speak( article.get( 'title' ) )
    else :
        pass 
        
if __name__ == '__main__' :
    speak( 'Activating JARVIS...' )
    while True :
        r = sr.Recognizer()
        print( 'Recognizing...' )
        try :
            with sr.Microphone() as source:
                print( 'Listening...' )
                audio = r.listen( source , timeout = 3 , phrase_time_limit = 2 )
            word = r.recognize_google( audio )
            if word.lower() == 'jarvis' :
                speak( 'Yaa' )
                with sr.Microphone() as source:
                    print( 'JARVIS Activated...' )
                    audio = r.listen( source )
                    command = r.recognize_google( audio )
                    processCommand( command )
        except Exception as e :
            print( e )