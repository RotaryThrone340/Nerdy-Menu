
# Type this into your python terminal to use
# pip install tkinter psutil pyautogui spotipy comtypes pycaw keyboard

# Quick reminder: DON'T put anything someone says into a terminal unless you have a valid reason.

# Here, it is the dependencies. (Copy and paste this into Chatgpt or something to validate)

import tkinter as tk
import psutil
import pyautogui
import socket
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard

# === SPOTIFY CONFIGURATION ===
SPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
SPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
Playlist_Name = ""  # Name of playlist where tracks will be saved if chosen.


class F3Overlay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("F3 Overlay")
        self.geometry("420x240+0+0")
        self.configure(bg="black")
        self.attributes("-topmost", True)
        self.overrideredirect(True)

        self.label = tk.Label(self, text="", fg="lime", bg="black", justify="left", font=("Consolas", 9))
        self.label.pack(padx=5, pady=5, anchor="nw")

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private"
        ))

        self.prev_bytes_sent = psutil.net_io_counters().bytes_sent
        self.prev_bytes_recv = psutil.net_io_counters().bytes_recv
        self.last_net_time = time.time()

        self.create_control_buttons()
        self.create_spotify_buttons()
        self.create_exit_spotify_button()

        self.key_sequence = []
        keyboard.on_press(self.on_key_press)
        self.update_overlay()

    def create_control_buttons(self):
        button_frame = tk.Frame(self, bg="black")
        button_frame.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

        tk.Button(button_frame, text="Minimize", command=self.withdraw, bg="gray", fg="white", width=8).pack(side="top", pady=(0, 2))
        tk.Button(button_frame, text="Exit", command=self.destroy, bg="red", fg="white", width=8).pack(side="top")

    def create_spotify_buttons(self):
        self.spotify_frame = tk.Frame(self, bg="black")
        self.spotify_frame.place(relx=0.5, rely=1.0, anchor="s", y=-5)

        tk.Button(self.spotify_frame, text="Save", command=self.spotify_save_to_music_playlist, bg="gray", fg="white", width=6).pack(side="left", padx=2)
        tk.Button(self.spotify_frame, text="Play/Pause", command=self.spotify_play_pause, bg="gray", fg="white", width=10).pack(side="left", padx=2)

    def create_exit_spotify_button(self):
        self.exit_spotify_frame = tk.Frame(self, bg="black")
        self.exit_spotify_frame.place(relx=0.0, rely=1.0, anchor="sw", x=5, y=-5)

        tk.Button(self.exit_spotify_frame, text="Exit Spotify", command=self.close_spotify, bg="red", fg="white", width=8).pack()

    def close_spotify(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and 'spotify' in proc.info['name'].lower():
                try:
                    proc.terminate()
                except Exception as e:
                    print(f"Error terminating Spotify process: {e}")

    def on_key_press(self, event):
        self.key_sequence.append(event.name)
        if len(self.key_sequence) > 4:
            self.key_sequence.pop(0)

        if self.key_sequence == ['0', '0', '0', '1']:
            if self.winfo_viewable():
                self.withdraw()
            else:
                self.deiconify()
            self.key_sequence = []

    def spotify_save_to_music_playlist(self):
        try:
            current = self.spotify.current_playback()
            if current and current.get("item"):
                track_id = current["item"]["id"]
                playlists = self.spotify.current_user_playlists()
                music_playlist_id = None
                for playlist in playlists['items']:
                    if playlist['name'] == Playlist_Name:
                        music_playlist_id = playlist['id']
                        break
                if music_playlist_id:
                    self.spotify.playlist_add_items(music_playlist_id, [track_id])
                    print(f"Track saved to '{Playlist_Name}' playlist.")
                else:
                    print(f"Playlist '{Playlist_Name}' not found.")
            else:
                print("No track currently playing.")
        except Exception as e:
            print("Error saving track:", e)

    def spotify_prev(self):
        keyboard.send('media previous track')

    def spotify_play_pause(self):
        keyboard.send('media play pause')

    def spotify_next(self):
        keyboard.send('media next track')

    def get_spotify_song(self):
        try:
            current = self.spotify.current_playback()
            if current and current.get("item"):
                name = current["item"]["name"]
                artist = current["item"]["artists"][0]["name"]
                return f"{name} - {artist}"
            else:
                return ""
        except Exception as e:
            print("Spotify error:", e)
            return ""

    def get_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return int(volume.GetMasterVolumeLevelScalar() * 100)

    def get_network_speed(self):
        now = time.time()
        elapsed = now - self.last_net_time
        counters = psutil.net_io_counters()

        upload_speed = (counters.bytes_sent - self.prev_bytes_sent) / elapsed / 1024
        download_speed = (counters.bytes_recv - self.prev_bytes_recv) / elapsed / 1024

        self.prev_bytes_sent = counters.bytes_sent
        self.prev_bytes_recv = counters.bytes_recv
        self.last_net_time = now

        return upload_speed, download_speed

    def get_disk_info(self):
        return round(psutil.disk_usage('/').free / (1024 ** 3), 2)

    def update_overlay(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        x, y = pyautogui.position()

        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = "Unavailable"

        upload, download = self.get_network_speed()
        disk_free = self.get_disk_info()
        volume = self.get_volume()
        song = self.get_spotify_song()

        output = (
            f"CPU: {cpu}% | RAM: {ram}%\n"
            f"Mouse: {x}, {y}\n"
            f"IP Address: {ip_address}\n"
            f"Upload: {upload:.2f} KB/s | Download: {download:.2f} KB/s\n"
            f"Disk Free: {disk_free} GB\n"
            f"Output Volume: {volume}%\n"
        )
        if song:
            output += f"Spotify: {song}\n"

        self.label.config(text=output)

        if song:
            self.spotify_frame.place(relx=0.5, rely=1.0, anchor="s", y=-5)
            self.exit_spotify_frame.place(relx=0.0, rely=1.0, anchor="sw", x=5, y=-5)
        else:
            self.spotify_frame.place_forget()
            self.exit_spotify_frame.place_forget()

        self.after(1000, self.update_overlay)


if __name__ == "__main__":
    app = F3Overlay()
    app.mainloop()
##############################################
#                                            #
# Go to the top to edit for personal use!    #
#                                            #
##############################################