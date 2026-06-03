# 🤖 Rishu Core Supreme

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Groq](https://img.shields.io/badge/AI-Groq-orange)](https://groq.com/)

**An AI-powered voice assistant for Windows with memory, vision, and 50+ system-control features – build your own Jarvis!**

## 🚀 Overview

Rishu Core Supreme is a fully voice-controlled Windows assistant that can:

- 🧠 **Remember** previous conversations (context‑aware memory)
- 👁️ **Read your screen** using OCR (Tesseract)
- 🎤 **Understand** natural voice commands (Whisper via Groq)
- 🖥️ **Control** your PC: open apps, manage files, lock screen, control volume
- 📧 **Send emails**, 💬 WhatsApp messages, 🌦️ get weather
- 🎵 **Control music**, 🎬 YouTube, 📝 take meeting notes
- 💾 **Manage code snippets**, run tests, review code with AI
- 🔋 **Monitor battery** and set reminders automatically

Built with Python, Groq LLM, and a modular design – easy to extend with new skills.

## ✨ Features

### 🧠 Memory & Context
- Remembers recent conversations and references like *"that folder"*
- Stores temporary context (last file/folder created)

### 👁️ Vision (Screen Reading)
- Read aloud any text visible on your screen
- Find and click buttons by their text (OCR)
- Smart WhatsApp Web automation

### 🎤 Voice Control
- Wake word detection (*Hey Rishu*)
- Continuous conversation mode (no need to repeat wake word)
- Interruptible speech (say *Stop* while speaking)

### 🖥️ System Commands
- System info (CPU, RAM, Disk, Battery)
- Volume control, lock PC, empty recycle bin
- Screenshot, take webcam photo

### 📁 File Management
- Create/delete folders, open any file
- Search files by name, organize desktop

### 💬 Communication
- Send emails (Gmail SMTP)
- Send WhatsApp messages (Web automation)
- Get live weather for any city

### 🎵 Media & Browser
- Play/pause/skip music (Spotify, media keys)
- YouTube search & playback control
- Browser navigation (new tab, scroll, refresh)

### 💻 Developer Tools
- Git operations (status, commit, push, pull)
- Save & retrieve code snippets (SQLite)
- AI code review using Groq
- Run Python tests (pytest)

### 📝 Productivity
- Create text notes, set reminders
- Meeting assistant (join link, take voice notes)
- Read PDFs aloud

### 🎥 Screen Recording
- Start/stop screen recording (requires ffmpeg)

### 🔋 Background Services
- Automatic battery alerts (<20%)
- Reminder notifications every 60 seconds

  ## 🛠️ Installation

### Prerequisites
- Windows 10/11
- Python 3.8 or higher
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/releases) (install to default path: `C:\Program Files\Tesseract-OCR\`)
- Git (optional, for version control)

### 1. Clone the Repository
```bash
git clone https://github.com/Rishabh-022/rishu-core
cd rishu-core
```
### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Generate requirements.txt (if not already present
```bash
pip freeze > requirements.txt
```

### 3. Set Up Environment Variables
Create a .env file in the project root:
```
ini
GROQ_API_KEY=your_groq_api_key_here
EMAIL_ADDRESS=your_email@gmail.com      # optional
EMAIL_PASSWORD=your_app_password        # optional
Get a free Groq API key at console.groq.com.

For email, use a Gmail App Password.

```

### 4. Run the Assistant
```bash
python phase8.py

```

---

## **Phase 5: Usage**

### 🎮 How to Use 

1. Say **"Hey Rishu"** to wake the assistant.
2. It will reply **"Yes?"** and enter active mode.
3. Speak any command (see list below).
4. After execution, it asks **"What else?"** – you can keep talking.
5. To exit active mode say: *"sleep"*, *"stop"*, *"go to sleep"*.
6. To shut down completely: *"shutdown rishu"*.




**Example conversation:**

Hey Rishu
→ Yes?
Open notepad
→ Opening notepad
Type in notepad Hello World
→ Typing text
What time is it?
→ It's 3:15 PM
Thank you
→ (goes back to standby)



## 📜 Command Reference (50+ voice commands)

### 🖥️ System
| Command | Action |
|---------|--------|
| *System info* | CPU, RAM, Disk usage |
| *Check battery* | Battery percentage & charging status |
| *Set volume to 50* | Change system volume (0–100) |
| *Lock PC* | Lock Windows workstation |
| *Take a screenshot* | Save & open screenshot |
| *Take a photo* | Capture webcam image |
| *Read the screen* | Read visible text aloud |
| *Find and click Submit* | Locate text on screen and click |

### 📁 Files & Folders
| Command | Action |
|---------|--------|
| *Create folder projects* | Create a new folder |
| *Delete folder old* | Delete a folder |
| *Open file resume.pdf* | Open any file |
| *Search files report* | Search Downloads for matching files |

### 🌐 Apps & Web
| Command | Action |
|---------|--------|
| *Open notepad* | Launch any app |
| *Open YouTube* | Open website |
| *Open LeetCode* | Open competitive programming sites |
| *Open CodeChef* | (via built‑in shortcuts) |

### 📝 Typing & Clipboard
| Command | Action |
|---------|--------|
| *Type in notepad Hello* | Type text into an app |
| *Copy that* | Ctrl+C |
| *Paste this* | Paste from clipboard |
| *Read clipboard* | Speak clipboard content |

### 🎵 Media
| Command | Action |
|---------|--------|
| *Play music Shape of You* | Search & play on Spotify |
| *Pause music* | Pause/play |
| *Next track* / *Previous track* | Skip tracks |
| *YouTube search Python* | Search YouTube |
| *YouTube play pause* | Toggle play/pause |
| *YouTube fullscreen* | Enter/exit fullscreen |

### 💬 Communication
| Command | Action |
|---------|--------|
| *Send email to x@y.com subject Hi body Hello* | Send email via Gmail |
| *Send WhatsApp to John hello* | Send message via WhatsApp Web |
| *Get weather in London* | Current weather |

### 💻 Developer
| Command | Action |
|---------|--------|
| *Git status* | Show working tree status |
| *Git commit Updated code* | Commit changes |
| *Git push* / *Git pull* | Push/pull to remote |
| *Save code fibonacci def fib(n):* | Save snippet to DB & file |
| *Get code fibonacci* | Retrieve snippet (copied to clipboard) |
| *Review code phase8.py* | AI code review |
| *Run tests* | Execute pytest in current directory |

### 📅 Productivity
| Command | Action |
|---------|--------|
| *Create note shopping milk, eggs* | Save text note |
| *Set reminder 2026-05-20 14:30 Call John* | Schedule reminder |
| *Join meeting zoom.us/j/123* | Open meeting link |
| *Take notes* | Start voice note‑taking (say *stop notes* to finish) |
| *Read PDF report.pdf* | Read first 3 pages aloud |

### 🎥 Screen Recording
| Command | Action |
|---------|--------|
| *Start recording* | Begin ffmpeg desktop capture |
| *Stop recording* | Stop & save recording |

### ⚙️ Process & Browser
| Command | Action |
|---------|--------|
| *Kill process chrome* | Force‑close a program |
| *New tab* / *Close tab* / *Refresh page* | Browser control |
| *Scroll down* / *Scroll up* | Scroll page |
| *Click button Login* | Find & click element by text |
| *Fill form John Doe* | Type into active field |


## 📁 Project Structure
```text
rishu-core/
│
├── phase8.py             # Main assistant (all features)
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (ignored by git)
├── .gitignore            # Git ignore rules
├── README.md
│
├── venv/                 # Virtual environment (ignored)
│
└── Documents/Rishu_Notes/ # Auto-created storage
    ├── memory.json       # Conversation history
    ├── rishu_core.db     # SQLite database (reminders, code, notes)
    ├── Code_Snippets/    # Saved code files
    ├── Meeting_Notes/    # Meeting note files
    └── *.txt             # Text notes

```
## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Microphone not working** | Set default input device in Windows Sound settings |
| **Silent crash after "Yes?"** | Increase `time.sleep()` in speaker & mic functions |
| **Tesseract not found** | Install Tesseract OCR to `C:\Program Files\Tesseract-OCR\` |
| **Email fails** | Use Gmail App Password, not your real password |
| **WhatsApp Web doesn't load** | Ensure you're logged in and browser is Chrome/Edge |
| **ModuleNotFoundError** | Activate venv: `.\venv\Scripts\activate` then reinstall dependencies |

## 🙏 Credits

- **Groq** for the ultra‑fast LLM API (Llama‑3 70B, Whisper)
- **UB Mannheim** for Windows Tesseract builds
- **PyAutoGUI**, **OpenCV**, **pyttsx3** and all open‑source libraries

---

⭐ **If you like this project, give it a star on GitHub!**  
Happy voice‑controlling your PC! 🚀
