import speech_recognition as sr
import pywhatkit
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def speak(text):
    # Create an instance of gTTS with the text to be spoken
    tts = gTTS(text=text, lang="en", tld="us")

    # Save the speech as an audio file
    tts.save("speech.mp3")

    # Load the audio file using pydub
    audio = AudioSegment.from_mp3("speech.mp3")

    # Play the audio
    play(audio)

def recognize_speech():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the source for speech recognition
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Set the pause threshold to indicate the end of a phrase
        audio = r.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        query = r.recognize_google(audio)
        print("You said:", query)
        return query

    except sr.UnknownValueError:
        print("I'm sorry, I couldn't understand what you said.")
        return ""

    except sr.RequestError as e:
        print("I'm sorry, there was an error during speech recognition:", str(e))
        return ""

def process_speech(query):
    if query:
        if "open YouTube" in query:
            speak("What do you want to watch?")
            query = recognize_speech()
            if query:
                speak("Sure! Opening YouTube and playing " + query)
                pywhatkit.playonyt(query)
            else:
                speak("No specific video mentioned. Exiting.")
        else:
            speak("I'm sorry, I couldn't recognize that command.")
    else:
        speak("Please say a command.")

while True:
    speak("Please say a command.")
    query = recognize_speech()
    process_speech(query)
