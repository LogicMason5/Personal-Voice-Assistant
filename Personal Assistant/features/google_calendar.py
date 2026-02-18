from __future__ import print_function
import datetime
import os
import pickle
import pytz
import pyttsx3

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# =============================
# Constants
# =============================

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

MONTHS = {month: index + 1 for index, month in enumerate([
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
])}

DAYS = {day: index for index, day in enumerate([
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
])}


# =============================
# Text-to-Speech (Initialize Once)
# =============================

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text: str):
    engine.say(text)
    engine.runAndWait()


# =============================
# Google Authentication
# =============================

def authenticate_google():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


# =============================
# Get Events
# =============================

def get_events(day: datetime.date, service):
    tz = pytz.UTC

    start_of_day = datetime.datetime.combine(day, datetime.time.min).replace(tzinfo=tz)
    end_of_day = datetime.datetime.combine(day, datetime.time.max).replace(tzinfo=tz)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        speak("No events found for this day.")
        return

    speak(f"You have {len(events)} event(s) on this day.")

    for event in events:
        start = event['start'].get('dateTime')

        if start:
            start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
            start_time = start_dt.strftime("%I:%M %p")
        else:
            start_time = "all day"

        summary = event.get("summary", "No title")
        print(start_time, summary)
        speak(f"{summary} at {start_time}")


# =============================
# Natural Language Date Parser
# =============================

def get_date(text: str):
    text = text.lower()
    today = datetime.date.today()

    if "today" in text:
        return today

    day = None
    month = None
    year = today.year
    weekday_target = None

    words = text.split()

    for word in words:
        if word in MONTHS:
            month = MONTHS[word]
        elif word in DAYS:
            weekday_target = DAYS[word]
        elif word.rstrip("stndrdth").isdigit():
            day = int(word.rstrip("stndrdth"))

    # If weekday specified (e.g., "next monday")
    if weekday_target is not None:
        current_weekday = today.weekday()
        delta = weekday_target - current_weekday

        if delta <= 0:
            delta += 7
        if "next" in text:
            delta += 7

        return today + datetime.timedelta(days=delta)

    # If specific date mentioned
    if day and month:
        if month < today.month:
            year += 1
        return datetime.date(year, month, day)

    if day and not month:
        month = today.month
        if day < today.day:
            month += 1
        return datetime.date(year, month, day)

    return today
