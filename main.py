import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize
translator = Translator()
pygame.mixer.init()
isTranslateOn = False

# Language mapping
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(text, from_language, to_language):
    return translator.translate(text, src=from_language, dest=to_language).text

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")  
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn
    rec = sr.Recognizer()

    while isTranslateOn:
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)
            
            output_placeholder.text(f"Detected: {spoken_text}")
            translated_text = translator_function(spoken_text, from_language, to_language)

            output_placeholder.text(f"Translated: {translated_text}")
            text_to_voice(translated_text, to_language)

        except Exception as e:
            output_placeholder.text("Error: " + str(e))

# Streamlit UI
st.title("Real-Time Language Translator")

from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

st.subheader("🎤 Voice Translation")
start_button = st.button("Start Listening")
stop_button = st.button("Stop Listening")

st.subheader("📝 Text Translation")
text_input = st.text_area("Type text to translate:")
translate_button = st.button("Translate Text")

output_placeholder = st.empty()

if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        main_process(output_placeholder, from_language, to_language)

if stop_button:
    isTranslateOn = False

if translate_button and text_input:
    translated_text = translator_function(text_input, from_language, to_language)
    output_placeholder.text(f"Translated: {translated_text}")
    text_to_voice(translated_text, to_language)
