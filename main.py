import cv2
import ctypes
import smtplib
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, QCoreApplication, pyqtSignal
from PyQt5.QtGui import QMovie
import sys
import os
import webbrowser
import pyautogui
import pyjokes
import pyttsx3
import speech_recognition as sr
import datetime 
from googletrans import Translator
import urllib.parse 
import wikipedia
import winshell
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from deep_translator import GoogleTranslator




# Setting up text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning! How may I help you?")
        speak("Good Morning! How may I help you?")
    elif hour >= 12 and hour < 18:
        print("Good Afternoon! How may I help you?")
        speak("Good Afternoon! How may I help you?")
    else:
        print("Good Evening! How may I help you?")
        speak("Good Evening! How may I help you?")
        
        
def translate_text(self, text):
        translator = Translator()
        translated = translator.translate(text, dest='en')  # Translate to English
        return translated.text

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('parthmodi909@gmail.com', 'gaja bifj xgdb qscp')
    server.sendmail('parthmodi909@gmail.com', to, content)
    server.close()
class AssistantThread(QThread):
    update_text_signal = pyqtSignal(str)  # Define a signal to send text to the UI



    def __init__(self, selected_language, speech_display):
        super(AssistantThread, self).__init__()
        self.selected_language = selected_language
        self.translator = Translator()
        self.speech_display = speech_display 



    def run(self):
        self.JARVIS()

    def STT(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Listening....")
            print("Listening....")
            audio = recognizer.listen(source)
        try:
            print("Recognizing.....")
            text = recognizer.recognize_google(audio, language=self.selected_language)
            print("You said: ", text)
            self.update_text_signal.emit(f"You said: {text}")
            translated_text = self.translate_text(text)
            return translated_text.lower()
        except Exception:
            speak("Sorry, Say that again please.....")
            return "None"

    def translate_text(self, text):
        try:
            translated_text = GoogleTranslator(source='auto', target='en').translate(text)
            print(f"Translated Text: {translated_text}")
            speak(translated_text)
            self.update_text_signal.emit(f"Translated: {translated_text}")
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            speak("Sorry, I couldn't translate that.")
            return "None"



    def open_drive_or_folder(self, query):
        if 'open c drive' in query or 'c drive' in query:
            speak("Opening C drive")
            os.startfile("C:\\")
        elif 'open d drive' in query or 'd drive' in query:
            speak("Opening D drive")
            os.startfile("D:\\")
        elif 'open documents' in query or 'documents' in query:
            speak("Opening Documents folder")
            os.startfile(os.path.expanduser("~/Documents"))
        elif 'open desktop' in query or 'desktop' in query:
            os.startfile("Desktop:\\")
        elif 'open downloads' in query or 'downloads' in query:
            speak("Opening Downloads")
            os.startfile(os.path.expanduser("~/Downloads"))
        else:
            speak("I cannot recognize this drive or folder")

    def close_application(self, app_name):
        try:
            if app_name in ["chrome", "google chrome", "browser"]:
                os.system("taskkill /f /im chrome.exe")  
            elif app_name in ["firefox", "mozilla firefox"]:
                os.system("taskkill /f /im firefox.exe")  
            elif app_name in ["edge", "microsoft edge"]:
                os.system("taskkill /f /im msedge.exe")  
            else:
                os.system(f"taskkill /f /im {app_name}.exe")
            speak(f"{app_name.capitalize()} has been closed.")
        except Exception as e:
            speak(f"Unable to close {app_name}. Please check the name.")
            print(f"Error: {e}")



    def JARVIS(self):
        wish()
        while True:
            query = self.STT()

            if 'goodbye' in query or 'exit' in query:
                speak("Goodbye, have a nice day!")
                sys.exit()
                
            elif 'open chart gpt' in query:
                 webbrowser.open('https://chatgpt.com/')

            elif 'open google' in query or 'google' in query or 'go to google' in query or 'search google' in query:
                webbrowser.open('www.google.co.in')
                speak("Opening Google")
                
            elif "search on youtube" in query:
                    query = query.lower().replace("search on youtube", "").strip()

                    if query:
                        query = urllib.parse.quote_plus(query)
                        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                        
                       
                        speak(f"Searching on YouTube for {query.replace('+', ' ')}")  
                    else:
                        speak("Please provide a search query.") 
                
            elif 'open youtube' in query or 'youtube' in query or 'go to youtube' in query or 'turn on youtube' in query:
                webbrowser.open("www.youtube.com")
                speak("Opening YouTube")
                
                
            elif 'play music' in query:
                speak("Playing music ,wait a second")
                song=random.randint(1,5)
                if song==1:
                    webbrowser.open("https://www.youtube.com/watch?v=yZomIAahIZc")
                else:
                        webbrowser.open("https://www.youtube.com/watch?v=RpZzSH3nMdg")

                
                
            elif 'close' in query:
                app_name = query.replace("close", "").strip().lower()  # Normalize input
                if app_name:
                    try:
                        self.close_application(app_name)  # Close the application
                    except Exception as e:
                        speak(f"Sorry, I couldn't close {app_name}.")
                        print(f"Error: {e}")
                else:
                    speak("Please specify the application you want to close.")

                
            elif 'open c drive' in query or 'open d drive' in query or 'open downloads' in query or 'open documents' in query or "open desktop" in query:
                self.open_drive_or_folder(query)
                
                
            elif 'start transcription' in query:
                self.speech_Recognizing()
                
                
            elif 'who made you' in query:
                speak("I was developed by Anil,Parth & Darshan.")
                
                
            elif 'shutdown' in query:
                speak("Shutting down the system")
                os.system('shutdown /s /t 1')
                
                
            elif 'translate' in query:
                text_to_translate = query.replace("translate", "").strip()
                if text_to_translate:
                    self.translate_text(text_to_translate)
            
            elif 'open stackoverflow' in query:
                    speak("Here you go to Stack Over flow.Happy coding")
                    webbrowser.open("stackoverflow.com")
                    
            elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(f"Sir, the time is {strTime}")
                
            elif 'date' in query:
                strDate = datetime.datetime.now().strftime("% d % m % Y")
                speak(f"Sir, today's date is {strDate}")
            
            elif 'open' in query:
                query = query.replace("open", "").strip()
                if query:  
                    try:
                        speak(f"Opening {query}")
                        pyautogui.hotkey("win")  
                        pyautogui.typewrite(query, interval=0.1)  # Type the query
                        pyautogui.press("enter")  # Press Enter to open the app
                    except Exception as e:
                        speak(f"Sorry, I couldn't open {query}.")
                        print(f"Error: {e}")
                else:
                    speak("What do you want me to open?")

                    
            elif 'start recording' in query or 'start listening' in query or 'start recognizing' in query:
                self.speech_Recognizing()

            elif 'who am i' in query or 'who i am' in query:
                speak("If you're talking, you're definitely human!")
                
            elif 'i love you' in query:
                    speak("I love you too!")
            
            elif 'i hate you' in query:
                    speak("I hate you too!")
                    
            elif 'you fool' in query:
                    speak("you fool to!")
                    
            elif 'go to hell' in query:
                    speak("ok,then come with me!")
            
            elif 'lock window' in query:
                speak("Locking the device")
                ctypes.windll.user32.LockWorkStation()

            elif 'shutdown the pc' in query or 'shut down the pc' in query or 'shutdown' in query or 'shut down' in query:
                speak("Shutting down the system")
                os.system('shutdown /s /t 1')

            elif 'restart' in query:
                speak("Restarting the system")
                os.system("shutdown /r")

            elif 'hibernate' in query or 'sleep' in query:
                speak("Hibernating the system")
                os.system("shutdown /h")


            elif 'wikipedia' in query:
                query = query.replace("wikipedia ", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'how are you' in query:
                speak("I am fine, thank you. How are you?")

            elif 'joke' in query:
                speak(pyjokes.get_joke())
                    
            elif "camera" in query or "take a photo" in query:
                try:
                    camera = cv2.VideoCapture(0) 
                    ret, frame = camera.read()
                    if ret:
                        cv2.imshow("Captured Photo", frame)
                        cv2.waitKey(0)  
                        cv2.destroyAllWindows()  
                        cv2.imwrite("img.jpg", frame)
                
                        engine.say("Photo capture")
                        engine.runAndWait()
                    else:
                        raise Exception("Failed to capture image")
                except Exception as e:
                    engine.say("Something went wrong")
                    engine.runAndWait()
                camera.release()
                    
                    
            elif "write a note" in query:
                try:
                    speak("What should i write,sir")
                    note = query
                    file = open('jarvis.txt', 'w')    
                    speak("Sir, Should i include date and time")
                    snfm = query
                    if 'yes' in snfm or 'sure' in snfm:
                        strTime = datetime.datetime.now().strftime("% H:% M:% S")
                        file.write(strTime)
                        file.write(" :- ")
                        file.write(note)
                    else:
                        file.write(note)
                except:
                    speak("something went wrong")
                    
		
            elif "show note" in query and "desplay note" in query:
                    speak("Showing Notes")
                    file = open("jarvis.txt", "r") 
                    print(file.read())
                    speak(file.read(6))
                    
                    
            elif "search on google" in query or "search" in query:
                query = query.replace("search on google", "")
                query = query.replace("search", "")
                webbrowser.open("https://www.google.com/search?q=" + query.strip())
                speak("Searching on Google for " + query.strip())
                                   
    
            elif "send email" in query or "mail" in query or "email" in query or "send mail to" in query:
                try:
                    speak("What should I say?")
                    content ="""
                        Respected sir,

                                    I hope you're doing well.
                                    
                                    I wanted to offer you a quick demo of my project. It's a [briefly describe what it does] and I think it could be useful for you.

                                    Would you be free for a short demo? Let me know a time that works for you.

                                    Looking forward to hearing from you!

                                    Best,
                                    Parth Modi
                                    9714522594

                    """
                    speak("To whom should I send the mail?")
                    to = input("To:")   
                    sendEmail(to, content)
                    print("Email has been sent.")
                    speak("Email has been sent!")
                except Exception as e:  
                    print(e)
                    speak("Sorry sir. I am not able to send this email")
                    
            
            elif "space" in query:
                    speak("Pressing space button")
                    pyautogui.press("space")
                    
            elif "enter" in query:
                    speak("Pressing enter button")
                    pyautogui.press("enter")
                    
            elif "backspace" in query or "delete" in query:    
                    speak("Pressing backspace button")
                    pyautogui.press("backspace")
                    
            elif "tab" in query:
                    speak("Pressing tab button")
                    pyautogui.press("tab")
                    
            elif "alt + tab" in query or "next page" in query or "go to next page" in query or "go other page" in query:
                    try:
                         pyautogui.keyDown('alt')  
                         pyautogui.press('tab')    
                         pyautogui.keyUp('alt')    
                         speak("Alt and Tab keys have been pressed.")
                    except Exception as e:
                        speak(f"Sorry, I couldn't open {query}.")
                        print(f"Error: {e}")
                        
            elif "caps lock" in query:
                    speak("Caps Lock has been pressed.")
                    pyautogui.press('capslock')
                
            

class ListeningApp(QtWidgets.QWidget):
    def __init__(self):
        super(ListeningApp, self).__init__()

        screen = QtWidgets.QApplication.primaryScreen()
        self.showFullScreen()

        layout = QtWidgets.QVBoxLayout()
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setAlignment(QtCore.Qt.AlignLeft)

        contacts = [
            ('Parth Modi')
        ]

        for name, phone in contacts:
            vbox = QtWidgets.QVBoxLayout()

            name_button = QtWidgets.QPushButton(name)
            name_button.setFixedSize(250, 50)
            name_button.setStyleSheet(
                'font-size: 20px; background-color: #36354E; color: white; border-radius: 10px; padding: 10px;')
            vbox.addWidget(name_button)

            phone_button = QtWidgets.QPushButton(phone)
            phone_button.setFixedSize(250, 50)
            phone_button.setStyleSheet(
                'font-size: 20px; background-color: #36354E; color: white; border-radius: 10px; padding: 10px;')
            vbox.addWidget(phone_button)

            top_layout.addLayout(vbox)

        layout.addLayout(top_layout)
        self.setLayout(layout)
        self.language_combobox = QtWidgets.QComboBox()
        self.language_combobox.addItems(["English","Hindi"])
        self.language_combobox.setFixedSize(175, 65)
        self.language_combobox.setEditable(True)
        self.language_combobox.lineEdit().setPlaceholderText("Search Language")
        self.language_combobox.lineEdit().setStyleSheet('font-size: 18px; color: white;')


        # Add filtering functionality
        self.language_combobox.lineEdit().textChanged.connect(self.filter_languages)

        layout.addWidget(self.language_combobox, alignment=QtCore.Qt.AlignRight)
        self.language_combobox.setStyleSheet('font-size: 20px; background-color: #36354E; color: white; border-radius: 10px; padding: 10px;')


        self.gif_label = QtWidgets.QLabel()
        gif = QMovie("b.gif")
        self.gif_label.setMovie(gif)
        layout.addWidget(self.gif_label, alignment=QtCore.Qt.AlignCenter)
        gif.start()
        
        

        # Add QTextEdit for displaying recognized speech with medium size
        self.speech_display = QtWidgets.QTextEdit()
        self.speech_display.setFixedSize(600, 150)  # Set size to medium
        self.speech_display.setReadOnly(True)
        self.speech_display.setStyleSheet('font-size: 18px; background-color: #36354E; color: white; border-radius: 10px; padding: 10px;')
        layout.addWidget(self.speech_display)


        self.setLayout(layout)
        self.setStyleSheet('background-color:#000000; color: white;')

        selected_language = self.language_combobox.currentText()
        self.assistant_thread = AssistantThread(selected_language, self.speech_display)
        
        
        # Connect the signal to the update_text slot
        self.assistant_thread.update_text_signal.connect(self.update_text)
        self.assistant_thread.start()

        self.language_combobox.currentIndexChanged.connect(self.update_language)
        
        

    def filter_languages(self, text):
        for i in range(self.language_combobox.count()):
            item_text = self.language_combobox.itemText(i).lower()
            if text.lower() in item_text:
                self.language_combobox.view().setRowHidden(i, False)
            else:
                self.language_combobox.view().setRowHidden(i, True)
                
                

    def update_language(self):
        selected_language = self.language_combobox.currentText()
        self.assistant_thread.selected_language = selected_language

        
    @QtCore.pyqtSlot(str)
    def update_text(self, text):
        """Update QTextEdit with new text."""
        self.speech_display.append(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ListeningApp()
    window.show()
    sys.exit(app.exec_())