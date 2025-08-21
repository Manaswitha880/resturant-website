
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import wikipedia
import pywhatkit
import smtplib
import threading
import time
import traceback

# ---------- Configuration ----------
OPENWEATHER_API_KEY = ""   # <-- put your OpenWeatherMap API key here (optional for weather)
EMAIL_SMTP = "smtp.gmail.com"
EMAIL_PORT = 587
# If using Gmail: create an App Password and use it below (recommended), or enable less-secure apps (not recommended)
EMAIL_ADDRESS = ""         # <-- your email address to send from
EMAIL_PASSWORD = ""        # <-- your email password or app password
# -----------------------------------

class VoiceAssistant:
    def __init__(self, name="Assistant"):
        self.name = name
        # Initialize recognizer and TTS
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        # Try to choose a nice voice (optional)
        try:
            voices = self.tts.getProperty('voices')
            if voices:
                self.tts.setProperty('voice', voices[0].id)
        except Exception:
            pass

        # Reminders: list of tuples (timestamp_unix, message)
        self.reminders = []
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()

        self.speak(f"Hello, I am {self.name}. How can I help you today?")

    def speak(self, text):
        print("Assistant:", text)
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception:
            # If TTS fails, still print
            pass

    def listen(self, timeout=5, phrase_time_limit=8):
        """Return recognized text or None. Falls back to text input if microphone unavailable."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Processing...")
                text = self.recognizer.recognize_google(audio)
                print("You:", text)
                return text.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except Exception as e:
            # If microphone/PyAudio is not present, fallback to text input
            print("Microphone error or speech recognition error:", str(e))
            print("Falling back to text input. Type your command and press Enter.")
            return input("You (type): ").lower()

    # ---------- Commands / Skills ----------
    def tell_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {now}")

    def tell_date(self):
        today = datetime.date.today().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {today}")

    def open_website(self, site):
        if not site.startswith("http"):
            site = "https://" + site
        webbrowser.open(site)
        self.speak(f"Opened {site}")

    def wiki_search(self, query):
        try:
            summary = wikipedia.summary(query, sentences=2)
            self.speak(summary)
        except Exception as e:
            self.speak("Sorry, I could not find information on that.")
            print("Wikipedia error:", e)

    def play_youtube(self, query):
        try:
            self.speak(f"Playing {query} on YouTube.")
            pywhatkit.playonyt(query)
        except Exception as e:
            self.speak("Error playing on YouTube.")
            print("pywhatkit error:", e)

    def get_weather(self, city):
        if not OPENWEATHER_API_KEY:
            self.speak("Weather API key is not configured. Skipping weather lookup.")
            return
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
            r = requests.get(url, params=params, timeout=8)
            data = r.json()
            if data.get("cod") != 200:
                self.speak("I couldn't find weather for that location.")
                return
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            self.speak(f"Current weather in {city}: {desc}. Temperature {temp}°C. Humidity {humidity} percent. Wind {wind} meters per second.")
        except Exception as e:
            print("Weather fetch error:", e)
            self.speak("Sorry, I couldn't fetch the weather right now.")

    def send_email(self, to_address, subject, body):
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            self.speak("Email credentials are not set. Please configure them in the script first.")
            return
        try:
            msg = f"Subject: {subject}\n\n{body}"
            server = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_address, msg)
            server.quit()
            self.speak("Email sent successfully.")
        except Exception as e:
            print("Email error:", e)
            self.speak("Sorry, I could not send the email. Check your credentials and SMTP settings.")

    def add_reminder(self, minutes_from_now, message):
        trigger_ts = time.time() + minutes_from_now * 60
        self.reminders.append((trigger_ts, message))
        self.speak(f"Reminder set for {minutes_from_now} minutes from now.")

    def _reminder_loop(self):
        while True:
            now = time.time()
            # Use a copy to avoid modifying list during iteration
            for item in list(self.reminders):
                trigger_ts, message = item
                if now >= trigger_ts:
                    # Speak reminder
                    self.speak("Reminder: " + message)
                    try:
                        self.reminders.remove(item)
                    except ValueError:
                        pass
            time.sleep(5)

    # ---------- Main command processor ----------
    def process_command(self, cmd: str):
        if not cmd: 
            return

        # Simple keyword-based processing, easy for beginners to extend
        if "time" in cmd:
            self.tell_time()
        elif "date" in cmd:
            self.tell_date()
        elif cmd.startswith("open "):
            site = cmd.replace("open ", "").strip()
            self.open_website(site)
        elif cmd.startswith("search wikipedia for ") or cmd.startswith("wikipedia "):
            q = cmd.replace("search wikipedia for ", "").replace("wikipedia ", "").strip()
            self.wiki_search(q)
        elif cmd.startswith("play "):
            q = cmd.replace("play ", "").strip()
            self.play_youtube(q)
        elif "weather in" in cmd:
            city = cmd.split("weather in")[-1].strip()
            self.get_weather(city)
        elif cmd.startswith("send email"):
            # Beginner flow: ask for details
            self.speak("Who should I send the email to? Please type the recipient email address.")
            to_addr = input("Recipient email: ").strip()
            self.speak("What is the subject?")
            subj = input("Subject: ").strip()
            self.speak("What should I say in the email?")
            body = input("Email body: ").strip()
            self.send_email(to_addr, subj, body)
        elif "set reminder" in cmd:
            # Command example: "set reminder in 5 minutes to check the oven"
            # We'll parse a simple pattern
            try:
                parts = cmd.split("in")
                if len(parts) >= 2:
                    after_in = parts[1].strip()
                    # expected like "5 minutes to check the oven"
                    tokens = after_in.split()
                    minutes = int(tokens[0])
                    # find "to" and rest is message
                    if "to" in after_in:
                        message = after_in.split("to", 1)[1].strip()
                    else:
                        message = "Reminder"
                    self.add_reminder(minutes, message)
                else:
                    self.speak("Sorry, please say: set reminder in X minutes to YOUR MESSAGE")
            except Exception:
                self.speak("Could not parse the reminder command. Use: set reminder in 5 minutes to take a break")
        elif "quit" in cmd or "exit" in cmd or "stop" in cmd:
            self.speak("Goodbye!")
            raise SystemExit()
        else:
            # fallback: simple web search
            self.speak("I did not understand that fully. Do you want me to search the web for it? (say yes or no)")
            answer = self.listen()
            if answer and "yes" in answer:
                webbrowser.open(f"https://www.google.com/search?q={cmd}")
                self.speak("I opened a web search for you.")

    # ---------- Run assistant loop ----------
    def run(self):
        while True:
            try:
                self.speak("Listening for command...")
                cmd = self.listen()
                if cmd is None:
                    # ask for typed command
                    self.speak("I did not hear anything. You can type the command, or say 'exit' to quit.")
                    cmd = input("Type command (or 'exit'): ").lower()
                self.process_command(cmd)
            except SystemExit:
                break
            except Exception as e:
                print("Error processing command:", e)
                traceback.print_exc()
                self.speak("Sorry, I encountered an error.")

if __name__ == "__main__":
    assistant = VoiceAssistant(name="Juno")
    assistant.run()
