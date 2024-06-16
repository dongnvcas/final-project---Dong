import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import time
import threading
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import wikipedia
import win32api
import win32con
import os
import sys


# Text-to-speech engine
bbot = pyttsx3.init()
voice = bbot.getProperty('voices')
bbot.setProperty('voice', voice[1].id)  # [1].id female voice [0].id male voice

# Function to speak text
def speak(audio):
    chat_log("B.BOT: " + audio)
    bbot.say(audio)
    bbot.runAndWait()

# Function to get current time
def timenow():
    Time = datetime.datetime.now().strftime('%I:%M:%p')
    speak(Time)

# Function to welcome user
def welcome():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak('Good morning Sir')
    elif 12 <= hour < 18:
        speak('Good afternoon Sir')
    else:
        speak('Good evening Sir')
    speak('How can I assist you')
    speak('Press listen to talk or type your command')

# Function to recognize voice command
def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        c.pause_threshold = 2  # delay 2 seconds
        try:
            audio = c.listen(source, timeout=5.0)  # listen for 5 seconds
        except sr.WaitTimeoutError:
            speak("Listening timed out, please try again.")
            return ""
    try:
        query = c.recognize_google(audio, language='en')
        chat_log('Boss: ' + query)
    except sr.UnknownValueError:
        speak('Please repeat or type the command')
        query = str(input('Your request is: '))
    return query

# Function to process user query
def process_query(query):
    query = query.lower()
    response = "This is a response to your query: " + query
    
    # Display the response in the text area
    chatWindow.insert(tk.END, "B.BOT: " + response + "\n")
    chatWindow.yview(tk.END)
    root.update_idletasks()  # Ensure the GUI updates immediately

    if 'google' in query:
        speak('What should I search sir?')
        search = command().lower()
        url = f'https://www.google.com/search?q={search}'
        wb.get().open(url)
        speak(f'Here is your {search} on Google')
    elif 'youtube' in query:
        speak('What should I search sir?')
        search = command().lower()
        url = f'https://www.youtube.com/search?q={search}'
        wb.get().open(url)
        speak(f'Here is your {search} on YouTube')
    elif 'music' in query:
        url = f'spotify:search:{query}'
        wb.get().open(url)
        speak(f'Playing music on Spotify')
        # Wait for the application to load
        time.sleep(3)
        # Press the space key
        win32api.keybd_event(0x20, 0, 0, 0)  # 0x20 is the virtual key code for the space bar
        time.sleep(0.05)  # Small delay to simulate a key press
        win32api.keybd_event(0x20, 0, win32con.KEYEVENTF_KEYUP, 0)  # Release the space key
    elif 'time' in query:
        speak(f'It is:')
        timenow()
    elif 'quit' in query or 'goodbye' in query:
        speak('Goodbye Sir')
        root.destroy()
    elif query:
        try:
            wikipedia.set_lang('en')
            robot = wikipedia.summary(query, sentences = 1)
            speak(robot)
        except wikipedia.exceptions.PageError as e:
            speak('Sorry, I can not find the result')
        except wikipedia.exceptions.DisambiguationError as e:
            speak('Sorry, I can not find the result')
    else:
        speak('I did not understand your command')

# Function to start listening for voice commands
def listen_command():
    threading.Thread(target=lambda: process_query(command())).start()

# Function to handle user input in GUI
def entered():
    user_input = messageWindow.get()
    chat_log("You: " + user_input)
    messageWindow.delete(0, END)
    process_query(user_input)

# Function to log chat history
def chat_log(message):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")
    chatWindow.insert(END, message + "\n")
    chatWindow.yview(tk.END)
    root.update_idletasks()

# Function to save chat history
def save_chat():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w",encoding="utf-8") as f:
            f.write(chatWindow.get(1.0, END))

# Adding code to make sure output exe can find logo
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize GUI
root = Tk()
root.title("B.BOT Chat")
root.geometry("400x450")
# Use resource_path to find logo
logo_path = resource_path('logo.png')
photo = PhotoImage(file = logo_path)
root.iconphoto(False, photo)

# Create Menu
main_menu = Menu(root)
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Save Chat", command=save_chat)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
main_menu.add_cascade(label="File", menu=file_menu)
root.config(menu=main_menu)

chatWindow = Text(root, bd=1, bg="white", width=50, height=8)
chatWindow.place(x=6, y=6, height=270, width=370)

messageWindow = Entry(root, bg="white", width=30)
messageWindow.place(x=6, y=280, height=88, width=160)

sendButton = Button(root, text="Send", bg="blue", fg="white", activebackground="light blue", width=12, height=5, font=("Arial", 18, "bold"), command=entered)
sendButton.place(x=150, y=280, height=88, width=100)

listenButton = Button(root, text="Listen", bg="green", fg="white", activebackground="light green", width=12, height=5, font=("Arial", 18, "bold"), command=listen_command)
listenButton.place(x=275, y=280, height=88, width=100)

# Start welcome message in a separate thread to avoid blocking the GUI
threading.Thread(target=welcome).start()

root.mainloop()