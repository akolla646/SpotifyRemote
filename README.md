# 🎵 Spotify Desktop Remote Player

A modern, resizable **Spotify desktop remote-control application** built using **Python**, **Spotipy**, and **CustomTkinter**.  
This app allows you to control Spotify playback, play playlists (including *Liked Songs*), manage volume, toggle shuffle/repeat, and view currently playing track details with **rounded album art**.

---

## ✨ Features

- 🎶 Play / Pause / Next / Previous track controls
- 📂 Select and play **any Spotify playlist**
- ❤️ Play **Liked Songs**
- ➕ Add current track to selected playlist
- 💾 Save track to Spotify library
- 🔀 Shuffle toggle
- 🔁 Repeat toggle (off → context → track)
- 🔊 Volume control
- 🖼️ Rounded album art with dynamic resizing
- 📐 Fully **resizable window**
- 🌙 Modern dark UI using CustomTkinter

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Spotipy** – Spotify Web API wrapper
- **CustomTkinter** – modern UI framework
- **Pillow (PIL)** – image handling
- **Requests**

---

## 📋 Prerequisites

1. A **Spotify account** (Premium recommended for full playback control)
2. A registered application on the  
   **Spotify Developer Dashboard**  
   https://developer.spotify.com/dashboard

---

## 🔑 Spotify App Setup

1. Go to the **Spotify Developer Dashboard**
2. Create a new app
3. Copy the following credentials:
   - `CLIENT_ID`
   - `CLIENT_SECRET`
4. Add the following Redirect URI in the app settings:

http://127.0.0.1:8888/callback


---

## 🚀 Installation & Setup

### Clone the repository

git clone https://github.com/your-username/spotify-desktop-remote.git
cd spotify-desktop-remote

### Install dependencies

pip install spotipy customtkinter pillow requests


### Configure Spotify credentials

Open the Python file and replace:

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"


with your Spotify app credentials.

---

## ▶️ Running the Application

python main.py


On the first run, a browser window will open asking you to authorize the application with Spotify.

---

## 🎧 Important Usage Notes

- Spotify **must be open on at least one device** (desktop, mobile, or web player)
- Start playing any song once manually
- After that, this app can control playback

If no device is active, Spotify will return:

NO_ACTIVE_DEVICE

---

## 📂 Project Structure



├── main.py

├── README.md


---

## ⚠️ Limitations

- Spotify Web API does **not allow downloading songs**
- Playback control requires an active Spotify device
- Free Spotify accounts have limited playback control

---


## 🙌 Acknowledgements

- Spotify Web API
- Spotipy
- CustomTkinter
