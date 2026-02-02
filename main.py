# ================================ IMPORTS =====================================
import os
import re
import sys
import time
import random
import datetime
import pprint
import requests
import pyjokes
import pyautogui
import pywhatkit
import wolframalpha

from PIL import Image
from PyQt5.QtCore import QThread, QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow

from Jarvis import JarvisAssistant
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config

# ================================ INITIALIZATION ===============================
obj = JarvisAssistant()
app_id = config.wolframalpha_id

# ================================ CONSTANTS ====================================
GREETINGS = [
    "hello jarvis", "jarvis", "wake up jarvis", "you there jarvis",
    "time to work jarvis", "hey jarvis", "ok jarvis", "are you there"
]

GREETINGS_RES = [
    "Always there for you sir",
    "I am ready sir",
    "Your wish is my command",
    "How can I help you sir?",
    "I am online and ready sir"
]

EMAIL_DIC = {
    "myself": "atharvaaingle@gmail.com",
    "my official email": "atharvaaingle@gmail.com",
    "my second email": "atharvaaingle@gmail.com"
}

APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
}

MUSIC_DIR = r"F:\Songs\Imagine_Dragons"

# ================================ HELPERS ======================================
def speak(text: str):
    obj.tts(text)


def computational_intelligence(question: str):
    try:
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        return answer
    except Exception:
        speak("Sorry sir, I couldn't fetch the answer.")
        return None


def startup_sequence():
    steps = [
        "Initializing Jarvis",
        "Starting all system applications",
        "Checking all drivers",
        "Calibrating core processors",
        "Checking internet connection",
        "All systems are online"
    ]
    for step in steps:
        speak(step)
        time.sleep(0.5)

    wish_user()


def wish_user():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good Morning sir")
    elif hour < 18:
        speak("Good Afternoon sir")
    else:
        speak("Good Evening sir")

    speak(f"Currently it is {obj.tell_time()}")
    speak("I am Jarvis, online and ready. How may I help you?")


# ================================ MAIN THREAD ==================================
class MainThread(QThread):

    def run(self):
        startup_sequence()

        while True:
            try:
                command = obj.mic_input().lower()

                if not command:
                    continue

                # -------- BASIC INFO --------
                if "time" in command:
                    speak(obj.tell_time())

                elif "date" in command:
                    speak(obj.tell_me_date())

                elif command in GREETINGS:
                    speak(random.choice(GREETINGS_RES))

                # -------- APPLICATIONS --------
                elif command.startswith("launch"):
                    app = command.replace("launch", "").strip()
                    path = APP_PATHS.get(app)
                    if path:
                        speak(f"Launching {app}")
                        obj.launch_any_app(path)
                    else:
                        speak("Application not found")

                elif command.startswith("open"):
                    domain = command.replace("open", "").strip()
                    speak(f"Opening {domain}")
                    obj.website_opener(domain)

                # -------- MEDIA --------
                elif "play music" in command:
                    if os.path.exists(MUSIC_DIR):
                        for song in os.listdir(MUSIC_DIR):
                            os.startfile(os.path.join(MUSIC_DIR, song))
                    else:
                        speak("Music directory not found")

                elif "youtube" in command:
                    video = command.replace("youtube", "").strip()
                    speak(f"Playing {video} on YouTube")
                    pywhatkit.playonyt(video)

                # -------- INFORMATION --------
                elif "weather" in command:
                    city = command.split()[-1]
                    speak(obj.weather(city))

                elif command.startswith("tell me about"):
                    topic = command.replace("tell me about", "").strip()
                    speak(obj.tell_me(topic))

                elif "news" in command or "headlines" in command:
                    speak("Here are today's headlines")
                    for news in obj.news()[:5]:
                        speak(news["title"])

                # -------- EMAIL --------
                elif "send email" in command:
                    speak("Whom should I send the email to?")
                    recipient = obj.mic_input().lower()
                    receiver_email = EMAIL_DIC.get(recipient)

                    if receiver_email:
                        speak("What is the subject?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()

                        msg = f"Subject: {subject}\n\n{message}"
                        obj.send_mail(
                            config.email,
                            config.email_password,
                            receiver_email,
                            msg
                        )
                        speak("Email sent successfully")
                    else:
                        speak("Email address not found")

                # -------- UTILITIES --------
                elif "joke" in command:
                    speak(pyjokes.get_joke())

                elif "screenshot" in command:
                    speak("What should I name the file?")
                    name = obj.mic_input()
                    img = pyautogui.screenshot()
                    img.save(f"{name}.png")
                    speak("Screenshot saved")

                elif "calculate" in command or command.startswith(("what is", "who is")):
                    answer = computational_intelligence(command)
                    if answer:
                        speak(answer)

                elif "ip address" in command:
                    ip = requests.get("https://api.ipify.org").text
                    speak(f"Your IP address is {ip}")

                elif "switch window" in command:
                    pyautogui.hotkey("alt", "tab")

                elif "goodbye" in command or "bye" in command:
                    speak("Going offline sir. Have a great day")
                    sys.exit()

            except Exception as e:
                print("Error:", e)
                speak("Something went wrong, please try again")


# ================================ GUI ==========================================
startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie2 = QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie2)
        self.ui.movie2.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        startExecution.start()

    def showTime(self):
        self.ui.textBrowser.setText(QDate.currentDate().toString(Qt.ISODate))
        self.ui.textBrowser_2.setText(QTime.currentTime().toString("hh:mm:ss"))


# ================================ APP START ====================================
app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
