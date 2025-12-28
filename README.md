# 🎵 Spotify Desktop Remote Player

A modern, resizable **Spotify desktop remote-control application** built using **Python**, **Spotipy**, and **CustomTkinter**.  
This app allows you to control Spotify playback, play playlists (including *Liked Songs*), manage volume, toggle shuffle/repeat, and view currently playing track details with **rounded album art**.

---

## ✨ Features

- 🎶 Play / Pause / Next / Previous track controls
- 📂 Select and play **any playlist**
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
- **Spotipy** (Spotify Web API wrapper)
- **CustomTkinter** (modern UI framework)
- **Pillow (PIL)** – image handling
- **Requests**

---

## 📋 Prerequisites

1. A **Spotify account** (Premium recommended for playback control)
2. A registered app on the  
   👉 [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

---

## 🔑 Spotify App Setup

1. Go to **Spotify Developer Dashboard**
2. Create a new app
3. Copy:
   - `CLIENT_ID`
   - `CLIENT_SECRET`
4. Add this Redirect URI in app settings:
