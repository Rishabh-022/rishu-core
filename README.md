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
git clone https://github.com/YOUR_USERNAME/rishu-core.git
cd rishu-core
