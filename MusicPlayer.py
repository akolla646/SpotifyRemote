import spotipy
from spotipy.oauth2 import SpotifyOAuth
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()

# --- Spotify App Credentials ---
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
REDIRECT_URI = "http://127.0.0.1:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,playlist-read-private,playlist-modify-public,playlist-modify-private,user-library-modify"
))

# --- CustomTkinter settings ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Kolla's Music Player")
root.geometry("420x900")
root.minsize(350, 600)  # Minimum size to prevent squishing

# --- Layout frames ---
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

track_label = ctk.CTkLabel(main_frame, text="Track: ", wraplength=400, font=("Helvetica", 16, "bold"))
track_label.pack(pady=5, anchor="center")

artist_label = ctk.CTkLabel(main_frame, text="Artist: ", font=("Helvetica", 14))
artist_label.pack(pady=5, anchor="center")

album_frame = ctk.CTkFrame(main_frame, corner_radius=15)
album_frame.pack(pady=5, fill="both", expand=True)

canvas = ctk.CTkCanvas(album_frame, bg="#121212", highlightthickness=0)
canvas.pack(fill="both", expand=True)

progress_var = ctk.DoubleVar()
progress_bar = ctk.CTkSlider(main_frame, from_=0, to=100, variable=progress_var, progress_color="#1db954", button_color="#1db954")
progress_bar.pack(pady=10, fill="x", padx=10)

btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=10)

play_pause_btn = ctk.CTkButton(btn_frame, text="Play/Pause", width=90, height=40)
play_pause_btn.grid(row=0, column=0, padx=5, pady=5)

prev_btn = ctk.CTkButton(btn_frame, text="Prev", width=90, height=40)
prev_btn.grid(row=0, column=1, padx=5, pady=5)

next_btn = ctk.CTkButton(btn_frame, text="Next", width=90, height=40)
next_btn.grid(row=0, column=2, padx=5, pady=5)

vol_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
vol_frame.pack(pady=5)

vol_down_btn = ctk.CTkButton(vol_frame, text="Vol -", width=100, height=40)
vol_down_btn.grid(row=0, column=0, padx=5, pady=5)

vol_up_btn = ctk.CTkButton(vol_frame, text="Vol +", width=100, height=40)
vol_up_btn.grid(row=0, column=1, padx=5, pady=5)

playlist_label = ctk.CTkLabel(main_frame, text="Select Playlist:", font=("Helvetica", 14))
playlist_label.pack(pady=5)

playlist_dict = {}
playlist_var = ctk.StringVar()

def get_user_playlists():
    global playlist_dict
    playlists = sp.current_user_playlists(limit=50)
    playlist_dict = {"Liked Songs": "liked_songs"}  # Special entry
    for playlist in playlists['items']:
        playlist_dict[playlist['name']] = playlist['id']
    if playlist_dict:
        playlist_var.set(next(iter(playlist_dict)))
    else:
        playlist_var.set("No playlists found")

get_user_playlists()
playlist_menu = ctk.CTkOptionMenu(main_frame, variable=playlist_var, values=list(playlist_dict.keys()))
playlist_menu.pack(pady=5, fill="x", padx=10)

def play_selected_playlist():
    selected_name = playlist_var.get()
    playlist_id = playlist_dict.get(selected_name)
    if playlist_id == "liked_songs":
        liked_tracks = sp.current_user_saved_tracks(limit=50)
        uris = [item["track"]["uri"] for item in liked_tracks["items"]]
    else:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        uris = [item["track"]["uri"] for item in playlist_tracks["items"]]
    if uris:
        sp.start_playback(uris=uris)

play_playlist_btn = ctk.CTkButton(main_frame, text="Play Playlist", command=play_selected_playlist, fg_color="#1db954")
play_playlist_btn.pack(pady=5, fill="x", padx=10)

def add_to_playlist():
    selected_name = playlist_var.get()
    playlist_id = playlist_dict.get(selected_name)
    if playlist_id and playlist_id != "liked_songs":
        playback = sp.current_playback()
        if playback and playback.get("item"):
            track_uri = playback["item"]["uri"]
            sp.playlist_add_items(playlist_id, [track_uri])

add_btn = ctk.CTkButton(main_frame, text="Add to Playlist", command=add_to_playlist, fg_color="#1db954")
add_btn.pack(pady=5, fill="x", padx=10)

def save_to_library():
    playback = sp.current_playback()
    if playback and playback.get("item"):
        track_id = playback["item"]["id"]
        sp.current_user_saved_tracks_add([track_id])

save_btn = ctk.CTkButton(main_frame, text="Save to Library", command=save_to_library, fg_color="#1db954")
save_btn.pack(pady=5, fill="x", padx=10)

shuffle_btn = ctk.CTkButton(main_frame, text="Shuffle: OFF")
shuffle_btn.pack(pady=5, fill="x", padx=10)

repeat_btn = ctk.CTkButton(main_frame, text="Repeat: off")
repeat_btn.pack(pady=5, fill="x", padx=10)

current_album_img = None

def update_ui():
    global current_album_img
    try:
        playback = sp.current_playback()
        if not playback or not playback.get("item"):
            track_label.configure(text="Track: No track playing")
            artist_label.configure(text="Artist: -")
            canvas.delete("all")
            progress_var.set(0)
            shuffle_btn.configure(text="Shuffle: OFF")
            repeat_btn.configure(text="Repeat: off")
            return

        item = playback["item"]
        track_name = item["name"]
        artists = ", ".join([a["name"] for a in item["artists"]])
        album_img_url = item["album"]["images"][0]["url"]
        progress_ms = playback["progress_ms"]
        duration_ms = item["duration_ms"]

        track_label.configure(text=f"Track: {track_name}")
        artist_label.configure(text=f"Artist: {artists}")

        response = requests.get(album_img_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data)).convert("RGBA")

        frame_w = album_frame.winfo_width()
        frame_h = album_frame.winfo_height()
        size = min(frame_w, frame_h)

        img = img.resize((size, size), Image.LANCZOS)

        # Rounded mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)

        img_tk = ImageTk.PhotoImage(img)

        canvas.delete("all")
        canvas.create_image(frame_w // 2, frame_h // 2, anchor="center", image=img_tk)
        canvas.image = img_tk
        current_album_img = img

        progress_percent = (progress_ms / duration_ms) * 100
        progress_var.set(progress_percent)

        shuffle_state = playback.get("shuffle_state", False)
        shuffle_btn.configure(text=f"Shuffle: {'ON' if shuffle_state else 'OFF'}")

        repeat_state = playback.get("repeat_state", "off")
        repeat_btn.configure(text=f"Repeat: {repeat_state}")

    except Exception as e:
        track_label.configure(text=f"Error: {str(e)}")

def play_pause():
    playback = sp.current_playback()
    if playback and playback["is_playing"]:
        sp.pause_playback()
    else:
        sp.start_playback()

def next_track():
    sp.next_track()

def prev_track():
    sp.previous_track()

def volume_up():
    current = sp.current_playback()["device"]["volume_percent"]
    new_vol = min(current + 10, 100)
    sp.volume(new_vol)

def volume_down():
    current = sp.current_playback()["device"]["volume_percent"]
    new_vol = max(current - 10, 0)
    sp.volume(new_vol)

def toggle_shuffle():
    playback = sp.current_playback()
    if playback:
        shuffle_state = playback.get("shuffle_state", False)
        sp.shuffle(not shuffle_state)

def toggle_repeat():
    playback = sp.current_playback()
    if playback:
        current_state = playback.get("repeat_state", "off")
        new_state = "context" if current_state == "off" else "track" if current_state == "context" else "off"
        sp.repeat(new_state)

def refresh_loop():
    while True:
        update_ui()
        time.sleep(2)

play_pause_btn.configure(command=play_pause)
next_btn.configure(command=next_track)
prev_btn.configure(command=prev_track)
vol_up_btn.configure(command=volume_up)
vol_down_btn.configure(command=volume_down)
shuffle_btn.configure(command=toggle_shuffle)
repeat_btn.configure(command=toggle_repeat)

def on_resize(event):
    update_ui()

root.bind("<Configure>", on_resize)

thread = threading.Thread(target=refresh_loop, daemon=True)
thread.start()

root.mainloop()
