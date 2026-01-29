import speech_recognition as sr
import pyttsx3

from Jarvis.features import (
    date_time,
    launch_app,
    website_open,
    weather,
    wikipedia,
    news,
    send_email,
    google_search,
    google_calendar,
    note,
    system_stats,
    loc,
)

# -------------------- TTS ENGINE SETUP --------------------
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)


class JarvisAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000

    # -------------------- SPEECH INPUT --------------------
    def mic_input(self):
        """
        Capture voice input from microphone
        :return: recognized text (str) or False
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source)

            print("Recognizing...")
            command = self.recognizer.recognize_google(
                audio, language="en-in"
            ).lower()

            print(f"You said: {command}")
            return command

        except sr.UnknownValueError:
            print("Could not understand audio")
            return False

        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return False

        except Exception as e:
            print(f"Mic input error: {e}")
            return False

    # -------------------- TEXT TO SPEECH --------------------
    def tts(self, text: str) -> bool:
        """
        Convert text to speech
        """
        try:
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"TTS error: {e}")
            return False

    # -------------------- DATE & TIME --------------------
    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    # -------------------- SYSTEM / APPS --------------------
    def launch_any_app(self, path_of_app: str):
        return launch_app.launch_app(path_of_app)

    def system_info(self):
        return system_stats.system_stats()

    # -------------------- WEB --------------------
    def website_opener(self, domain: str):
        return website_open.website_opener(domain)

    def search_anything_google(self, command: str):
        google_search.google_search(command)

    # -------------------- WEATHER --------------------
    def get_weather(self, city: str):
        try:
            return weather.fetch_weather(city)
        except Exception as e:
            print(f"Weather error: {e}")
            return False

    # -------------------- WIKIPEDIA --------------------
    def tell_me(self, topic: str):
        return wikipedia.tell_me_about(topic)

    # -------------------- NEWS --------------------
    def get_news(self):
        return news.get_news()

    # -------------------- EMAIL --------------------
    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        return send_email.mail(
            sender_email, sender_password, receiver_email, msg
        )

    # -------------------- GOOGLE CALENDAR --------------------
    def google_calendar_events(self, text: str):
        try:
            service = google_calendar.authenticate_google()
            date = google_calendar.get_date(text)

            if not date:
                return False

            return google_calendar.get_events(date, service)

        except Exception as e:
            print(f"Calendar error: {e}")
            return False

    # -------------------- NOTES --------------------
    def take_note(self, text: str):
        note.note(text)

    # -------------------- LOCATION --------------------
    def location(self, target_location: str):
        return loc.loc(target_location)

    def my_location(self):
        return loc.my_location()
