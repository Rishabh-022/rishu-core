import os
import shutil
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
import pyttsx3
import subprocess
import webbrowser
from datetime import datetime, timedelta
import time
import pyautogui
import cv2
import psutil
import requests
import pyperclip
import json
from pathlib import Path
import threading
from collections import deque
import pytesseract
from PIL import Image
import numpy as np
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from plyer import notification

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 180)

def setup_database():
    """Initialize SQLite database for reminders, code snippets, and notes"""
    db_path = Path.home() / "Documents" / "Rishu_Notes" / "rishu_core.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_time TEXT NOT NULL,
            message TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            code TEXT NOT NULL,
            language TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meeting_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn, cursor

db_conn, db_cursor = setup_database()

class ConversationMemory:
    def __init__(self, max_history=10):
        self.history = deque(maxlen=max_history)
        self.short_term = {}
        self.memory_file = Path.home() / "Documents" / "Rishu_Notes" / "memory.json"
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.load_memory()
    
    def add_interaction(self, user_input, response, action_taken=None):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": response,
            "action": action_taken
        }
        self.history.append(interaction)
        self.save_memory()
    
    def get_context(self, last_n=3):
        return list(self.history)[-last_n:]
    
    def remember_temp(self, key, value):
        self.short_term[key] = value
    
    def recall_temp(self, key):
        return self.short_term.get(key, None)
    
    def save_memory(self):
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(list(self.history), f, indent=2)
        except Exception as e:
            print(f"Memory save error: {e}")
    
    def load_memory(self):
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.history.extend(data[-10:])
        except Exception as e:
            print(f"Memory load error: {e}")

memory = ConversationMemory()

class ScreenReader:
    def read_text_on_screen(self, region=None):
        try:
            screenshot = pyautogui.screenshot(region=region)
            text = pytesseract.image_to_string(screenshot)
            return text.strip()
        except:
            return ""
    
    def find_and_click(self, search_text):
        try:
            screenshot = pyautogui.screenshot()
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            for i, text in enumerate(data['text']):
                if search_text.lower() in text.lower():
                    x = data['left'][i] + data['width'][i] // 2
                    y = data['top'][i] + data['height'][i] // 2
                    pyautogui.click(x, y)
                    return True
        except:
            pass
        return False
    
    def wait_for_text(self, text, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if text.lower() in self.read_text_on_screen().lower():
                return True
            time.sleep(0.5)
        return False

screen_reader = ScreenReader()

class StableSpeaker:
    def speak(self, text):
        print(f"Rishu Core: {text}")
        text = text.replace("ACTION:", "").replace("_", " ")
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
        time.sleep(0.5)

speaker = StableSpeaker()

DESKTOP = str(Path.home() / "Desktop")
DOWNLOADS = str(Path.home() / "Downloads")
DOCUMENTS = str(Path.home() / "Documents")

def listen_for_wake_word():
    time.sleep(0.2)
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\n[Waiting for 'Hey Rishu'...] ")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
        text = recognizer.recognize_google(audio).lower()
        print(f"Heard: {text}")
        wake_words = ["rishu", "issue", "reku", "ishu", "tissue", "ratio", "reshu", "shoe", "dishu"]
        return any(word in text for word in wake_words)
    except:
        return False

def listen_for_command():
    time.sleep(0.3)
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("--- Listening for command ---")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        audio_data = audio.get_wav_data()
        try:
            transcription = client.audio.transcriptions.create(
                file=("command.wav", audio_data),
                model="whisper-large-v3-turbo",
                response_format="text",
            )
            return transcription.strip()
        except:
            return recognizer.recognize_google(audio).strip()
    except:
        return ""

def send_email(recipient, subject, body):
    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            speaker.speak("Email not configured. Add EMAIL_ADDRESS and EMAIL_PASSWORD to .env file.")
            return False
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def control_music(action, song_name=""):
    try:
        if action == "play":
            if song_name:
                webbrowser.open(f"https://open.spotify.com/search/{song_name}")
                time.sleep(3)
                pyautogui.press('enter')
            else:
                pyautogui.press('playpause')
        elif action == "pause":
            pyautogui.press('playpause')
        elif action == "next":
            pyautogui.press('nexttrack')
        elif action == "previous":
            pyautogui.press('prevtrack')
        return True
    except:
        return False

def set_reminder(reminder_time_str, message):
    try:
        db_cursor.execute(
            "INSERT INTO reminders (reminder_time, message) VALUES (?, ?)",
            (reminder_time_str, message)
        )
        db_conn.commit()
        return True
    except:
        return False

def check_reminders():
    try:                                                                                                                           
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        db_cursor.execute(
            "SELECT id, message FROM reminders WHERE reminder_time <= ? AND is_active = 1",
            (current_time,)
        )
        for reminder_id, message in db_cursor.fetchall():
            notification.notify(title="Rishu Core Reminder", message=message, timeout=10)
            speaker.speak(f"Reminder: {message}")
            db_cursor.execute("UPDATE reminders SET is_active = 0 WHERE id = ?", (reminder_id,))
        db_conn.commit()
    except:
        pass

def save_code_snippet(title, code, language="python"):
    try:
        db_cursor.execute(
            "INSERT INTO code_snippets (title, code, language) VALUES (?, ?, ?)",
            (title, code, language)
        )
        db_conn.commit()
        snippets_dir = Path.home() / "Documents" / "Rishu_Notes" / "Code_Snippets"
        snippets_dir.mkdir(parents=True, exist_ok=True)
        ext_map = {"python": ".py", "javascript": ".js", "java": ".java", "cpp": ".cpp"}
        ext = ext_map.get(language, ".txt")
        with open(snippets_dir / f"{title}{ext}", 'w') as f:
            f.write(code)
        return True
    except:
        return False

def get_code_snippet(title):
    try:
        db_cursor.execute(
            "SELECT code FROM code_snippets WHERE title LIKE ? ORDER BY created_at DESC LIMIT 1",
            (f"%{title}%",)
        )
        result = db_cursor.fetchone()
        if result:
            pyperclip.copy(result[0])
            return f"Code copied to clipboard: {result[0][:100]}..."
        return "No code snippet found"
    except:
        return "Error retrieving code"

def check_battery():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            if not plugged and percent < 20:
                speaker.speak(f"Warning: Battery at {percent}%. Please charge!")
            return f"Battery: {percent}% {'(Charging)' if plugged else '(On battery)'}"
    except:
        return "Battery info unavailable"

def browser_navigate(action, text=""):
    try:
        if action == "click_button":
            return f"Clicked {text}" if screen_reader.find_and_click(text) else f"Could not find {text}"
        elif action == "fill_form":
            pyautogui.write(text, interval=0.05)
            return "Form filled"
        elif action == "scroll_down":
            pyautogui.scroll(-500)
            return "Scrolled down"
        elif action == "scroll_up":
            pyautogui.scroll(500)
            return "Scrolled up"
        elif action == "new_tab":
            pyautogui.hotkey('ctrl', 't')
            return "New tab opened"
        elif action == "close_tab":
            pyautogui.hotkey('ctrl', 'w')
            return "Tab closed"
        elif action == "refresh":
            pyautogui.hotkey('ctrl', 'r')
            return "Page refreshed"
    except:
        return "Browser error"

def git_operations(action, message=""):
    try:
        if action == "status":
            result = subprocess.run(["git", "status"], capture_output=True, text=True, shell=True)
            return result.stdout[:500]
        elif action == "commit":
            subprocess.run(["git", "commit", "-m", message], shell=True)
            return f"Committed: {message}"
        elif action == "push":
            subprocess.run(["git", "push"], shell=True)
            return "Code pushed"
        elif action == "pull":
            subprocess.run(["git", "pull"], shell=True)
            return "Code pulled"
    except:
        return "Git error"

def youtube_control(action, query=""):
    try:
        if action == "search":
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Searching YouTube for {query}"
        elif action == "play_pause":
            pyautogui.press('space')
            return "Play/Pause toggled"
        elif action == "fullscreen":
            pyautogui.press('f')
            return "Fullscreen toggled"
        elif action == "skip_forward":
            pyautogui.press('l')
            return "Skipped forward"
    except:
        return "YouTube error"

def review_code(filename):
    try:
        with open(filename, 'r') as f:
            code = f.read()
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a senior code reviewer."},
                {"role": "user", "content": f"Review this code:\n{code[:2000]}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )
        review = chat_completion.choices[0].message.content
        speaker.speak(review[:500])
        return review
    except:
        return "Error reviewing code"

def smart_whatsapp_message(contact, message):
    try:
        speaker.speak(f"Sending WhatsApp to {contact}")
        webbrowser.open("https://web.whatsapp.com/")
        if screen_reader.wait_for_text("Search", timeout=30):
            pyautogui.hotkey('ctrl', 'alt', '/')
            time.sleep(1)
            pyautogui.write(contact, interval=0.1)
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(1)
            if message:
                pyautogui.write(message, interval=0.05)
                pyautogui.press('enter')
            speaker.speak("Message sent!")
    except:
        speaker.speak("WhatsApp error")

def process_with_brain(user_input):
    context = memory.get_context(3)
    context_str = "\n".join([f"User: {c['user']}" for c in context])
    
    system_prompt = f"""
    You are Rishu Core, a SUPREME Windows assistant.
    
    RECENT CONTEXT: {context_str}
    
    AVAILABLE ACTIONS (respond with EXACT format):
    ACTION:CREATE_FOLDER|name
    ACTION:DELETE_FOLDER|name
    ACTION:OPEN_APP|app_name
    ACTION:OPEN_WEBSITE|url
    ACTION:GET_TIME
    ACTION:TYPE_TEXT|app_name|text
    ACTION:TAKE_PHOTO
    ACTION:OPEN_FILE|filename
    ACTION:SYSTEM_INFO
    ACTION:SET_VOLUME|number
    ACTION:SCREENSHOT
    ACTION:LOCK_PC
    ACTION:CLIPBOARD_COPY
    ACTION:CLIPBOARD_PASTE|text
    ACTION:CLIPBOARD_READ
    ACTION:KILL_PROCESS|process_name
    ACTION:SEARCH_FILES|pattern
    ACTION:CREATE_NOTE|title|content
    ACTION:GET_WEATHER|city
    ACTION:WHATSAPP|contact|message
    ACTION:SEND_EMAIL|recipient|subject|body
    ACTION:PLAY_MUSIC|song_name
    ACTION:PAUSE_MUSIC
    ACTION:NEXT_TRACK
    ACTION:PREVIOUS_TRACK
    ACTION:SET_REMINDER|time|message
    ACTION:SAVE_CODE|title|code
    ACTION:GET_CODE|title
    ACTION:REVIEW_CODE|filename
    ACTION:BATTERY_CHECK
    ACTION:CLICK_BUTTON|button_text
    ACTION:FILL_FORM|text
    ACTION:SCROLL_DOWN
    ACTION:SCROLL_UP
    ACTION:NEW_TAB
    ACTION:CLOSE_TAB
    ACTION:REFRESH_PAGE
    ACTION:GIT_COMMIT|message
    ACTION:GIT_PUSH
    ACTION:GIT_PULL
    ACTION:GIT_STATUS
    ACTION:YOUTUBE_SEARCH|query
    ACTION:YOUTUBE_PLAY_PAUSE
    ACTION:YOUTUBE_FULLSCREEN
    ACTION:YOUTUBE_SKIP
    ACTION:START_RECORDING
    ACTION:STOP_RECORDING
    ACTION:JOIN_MEETING|link
    ACTION:TAKE_NOTES
    ACTION:RUN_TESTS|project_name
    ACTION:READ_PDF|filename
    ACTION:READ_SCREEN
    ACTION:FIND_AND_CLICK|text

    CP WEBSITES: "lead code"/"bleed code/leet code" → ACTION:OPEN_WEBSITE|leetcode.com | "code chef" → ACTION:OPEN_WEBSITE|codechef.com
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return chat_completion.choices[0].message.content
    except:
        return "Brain error"

def background_tasks():
    while True:
        try:
            check_reminders()
            check_battery()
        except:
            pass
        time.sleep(60)

bg_thread = threading.Thread(target=background_tasks, daemon=True)
bg_thread.start()

if __name__ == "__main__":
    print("=" * 50)
    print("RISHU CORE SUPREME STARTING...")
    print("=" * 50)
    
    speaker.speak("Rishu Core Supreme is online with all features!")
    
    while True:
        try:
            time.sleep(0.1)
            
            if listen_for_wake_word():
                speaker.speak("Yes?")
                
                while True:
                    command = listen_for_command()
                    
                    bad_words = ["you", "i", ".", "you.", "i.", "yeah", "ok", "", "thank you.", "thank you", "thanks."]
                    if not command or len(command.strip()) <= 1 or command.lower().strip() in bad_words:
                        break
                    
                    print(f"You said: {command}")
                    
                    if any(word in command.lower() for word in ["sleep", "stop", "go to sleep", "standby"]):
                        speaker.speak("Standing by.")
                        break
                    
                    if "shutdown rishu" in command.lower():
                        speaker.speak("Goodbye!")
                        db_conn.close()
                        exit()
                    
                    response = process_with_brain(command)
                    print(f"Brain: {response}")
                    
                    try:
                        if "ACTION:CREATE_FOLDER" in response:
                            name = response.split("|")[-1].strip()
                            os.makedirs(name, exist_ok=True)
                            speaker.speak(f"Created {name}")
                        
                        elif "ACTION:DELETE_FOLDER" in response:
                            name = response.split("|")[-1].strip()
                            if os.path.exists(name):
                                shutil.rmtree(name)
                                speaker.speak(f"Deleted {name}")
                        
                        elif "ACTION:OPEN_APP" in response:
                            app = response.split("|")[-1].strip()
                            speaker.speak(f"Opening {app}")
                            subprocess.run(f"start {app}", shell=True)

                        elif "ACTION:OPEN_WEBSITE" in response:
                            site = response.split("|")[-1].strip()
                            if not site.startswith("http"):
                                site = f"https://www.{site}.com"
                            speaker.speak(f"Opening {site}")
                            webbrowser.open(site)

                        elif "ACTION:GET_TIME" in response:
                            speaker.speak(datetime.now().strftime("%I:%M %p"))

                        elif "ACTION:TYPE_TEXT" in response:
                            parts = response.split("|")
                            app_name = parts[1].strip()
                            text = parts[2].strip()
                            subprocess.run(f"start {app_name}", shell=True)
                            time.sleep(3)
                            pyautogui.write(text, interval=0.05)

                        elif "ACTION:TAKE_PHOTO" in response:
                            cap = cv2.VideoCapture(0)
                            time.sleep(2)
                            ret, frame = cap.read()
                            if ret:
                                filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                                cv2.imwrite(filename, frame)
                                os.startfile(filename)
                            cap.release()

                        elif "ACTION:OPEN_FILE" in response:
                            filename = response.split("|")[-1].strip()
                            os.startfile(filename)

                        elif "ACTION:SYSTEM_INFO" in response:
                            cpu = psutil.cpu_percent(interval=1)
                            mem = psutil.virtual_memory()
                            speaker.speak(f"CPU: {cpu}% RAM: {mem.percent}%")

                        elif "ACTION:SCREENSHOT" in response:
                            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            pyautogui.screenshot().save(filename)
                            os.startfile(filename)

                        elif "ACTION:LOCK_PC" in response:
                            os.system("rundll32.exe user32.dll,LockWorkStation")

                        elif "ACTION:CLIPBOARD_COPY" in response:
                            pyautogui.hotkey('ctrl', 'c')

                        elif "ACTION:CLIPBOARD_READ" in response:
                            speaker.speak(pyperclip.paste())

                        elif "ACTION:CLIPBOARD_PASTE" in response:
                            text = response.split("|")[-1].strip()
                            pyperclip.copy(text)
                            pyautogui.hotkey('ctrl', 'v')

                        elif "ACTION:KILL_PROCESS" in response:
                            proc = response.split("|")[-1].strip()
                            for p in psutil.process_iter(['name']):
                                if proc.lower() in p.info['name'].lower():
                                    p.kill()
                            speaker.speak(f"Killed {proc}")

                        elif "ACTION:SEARCH_FILES" in response:
                            pattern = response.split("|")[-1].strip()
                            results = []
                            for root, dirs, files in os.walk(DOWNLOADS):
                                for file in files:
                                    if pattern.lower() in file.lower():
                                        results.append(file)
                            speaker.speak(f"Found: {', '.join(results[:5])}" if results else "No files")

                        elif "ACTION:CREATE_NOTE" in response:
                            parts = response.split("|")
                            title = parts[1].strip()
                            content = parts[2].strip()
                            path = os.path.join(DOCUMENTS, "Rishu_Notes")
                            os.makedirs(path, exist_ok=True)
                            with open(os.path.join(path, f"{title}.txt"), 'w') as f:
                                f.write(content)

                        elif "ACTION:GET_WEATHER" in response:
                            city = response.split("|")[-1].strip()
                            result = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
                            speaker.speak(result.text.strip())

                        elif "ACTION:WHATSAPP" in response:
                            parts = response.split("|")
                            contact = parts[1].strip()
                            message = parts[2].strip() if len(parts) > 2 else ""
                            smart_whatsapp_message(contact, message)

                        elif "ACTION:READ_SCREEN" in response:
                            text = screen_reader.read_text_on_screen()
                            speaker.speak(text[:300])

                        elif "ACTION:FIND_AND_CLICK" in response:
                            text = response.split("|")[-1].strip()
                            screen_reader.find_and_click(text)

                        elif "ACTION:SEND_EMAIL" in response:
                            parts = response.split("|")
                            send_email(parts[1].strip(), parts[2].strip(), parts[3].strip() if len(parts) > 3 else "")

                        elif "ACTION:PLAY_MUSIC" in response:
                            control_music("play", response.split("|")[-1].strip())

                        elif "ACTION:PAUSE_MUSIC" in response:
                            control_music("pause")

                        elif "ACTION:NEXT_TRACK" in response:
                            control_music("next")

                        elif "ACTION:PREVIOUS_TRACK" in response:
                            control_music("previous")

                        elif "ACTION:SET_REMINDER" in response:
                            parts = response.split("|")
                            set_reminder(parts[1].strip(), parts[2].strip())

                        elif "ACTION:SAVE_CODE" in response:
                            parts = response.split("|")
                            save_code_snippet(parts[1].strip(), parts[2].strip())

                        elif "ACTION:GET_CODE" in response:
                            speaker.speak(get_code_snippet(response.split("|")[-1].strip()))

                        elif "ACTION:REVIEW_CODE" in response:
                            review_code(response.split("|")[-1].strip())

                        elif "ACTION:BATTERY_CHECK" in response:
                            speaker.speak(check_battery())

                        elif "ACTION:CLICK_BUTTON" in response:
                            browser_navigate("click_button", response.split("|")[-1].strip())

                        elif "ACTION:FILL_FORM" in response:
                            browser_navigate("fill_form", response.split("|")[-1].strip())

                        elif "ACTION:SCROLL_DOWN" in response:
                            browser_navigate("scroll_down")

                        elif "ACTION:SCROLL_UP" in response:
                            browser_navigate("scroll_up")

                        elif "ACTION:NEW_TAB" in response:
                            browser_navigate("new_tab")

                        elif "ACTION:CLOSE_TAB" in response:
                            browser_navigate("close_tab")

                        elif "ACTION:REFRESH_PAGE" in response:
                            browser_navigate("refresh")

                        elif "ACTION:GIT_COMMIT" in response:
                            git_operations("commit", response.split("|")[-1].strip())

                        elif "ACTION:GIT_PUSH" in response:
                            git_operations("push")

                        elif "ACTION:GIT_PULL" in response:
                            git_operations("pull")

                        elif "ACTION:GIT_STATUS" in response:
                            speaker.speak(git_operations("status"))

                        elif "ACTION:YOUTUBE_SEARCH" in response:
                            youtube_control("search", response.split("|")[-1].strip())

                        elif "ACTION:YOUTUBE_PLAY_PAUSE" in response:
                            youtube_control("play_pause")

                        elif "ACTION:YOUTUBE_FULLSCREEN" in response:
                            youtube_control("fullscreen")

                        elif "ACTION:YOUTUBE_SKIP" in response:
                            youtube_control("skip_forward")

                        elif "ACTION:SET_VOLUME" in response:
                            level = int(response.split("|")[-1].strip())
                            for _ in range(50):
                                pyautogui.press('volumedown')
                            for _ in range(level//2):
                                pyautogui.press('volumeup')
                        
                        else:
                            if "ACTION:" not in response:
                                speaker.speak(response)
                    
                    except Exception as e:
                        print(f"Error: {e}")
                    
                    memory.add_interaction(command, response)
                    speaker.speak("What else?")
        
        except KeyboardInterrupt:
            print("\nShutting down...")
            db_conn.close()
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(1)