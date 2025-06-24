
Nerdy Menu - Menu Overlay for Spotify and System Stats
A simple Python Tkinter overlay that shows your system info (CPU, RAM, network, disk, volume) and Spotify playback details.
Includes media controls (playpause, next, prev) using system media keys, and a save-to-playlist button using the Spotify API.

Features
Displays CPU %, RAM %, network upload/download speeds, free disk space, system volume

Shows current Spotify track info

Media control buttons playpause, next, previous (works system-wide via media keys)

Save current track to a Spotify playlist (requires Spotify API credentials)

Exit Spotify button to close the app

Always-on-top overlay with toggle shortcut (press 0001 to hideshow)

Requirements
Python 3.7+

Windows OS (uses Windows-specific audio and process APIs)

Installation
Clone the repository

bash
Copy
Edit
git clone httpsgithub.comRotaryThrone340Nerdy-Menu.git
cd Nerdy-Menu
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
(Or manually install with pip install tkinter psutil pyautogui spotipy comtypes pycaw keyboard)

Setup Spotify API Credentials
Go to the Spotify Developer Dashboard and create a new app.

Copy your Client ID and Client Secret.

Set the Redirect URI in your Spotify app settings to http127.0.0.18888callback.

Open F3Menu.py (or your main script) and replace the placeholders

python
Copy
Edit
SPOTIFY_CLIENT_ID = your_client_id_here
SPOTIFY_CLIENT_SECRET = your_client_secret_here
SPOTIFY_REDIRECT_URI = http127.0.0.18888callback
Playlist_Name = Music  # or whatever playlist you want to save tracks to
Run the App
Run the script with Python

bash
Copy
Edit
python F3Menu.py
Usage Notes
Media controls use system media keys and should work with Spotify, VLC, Windows Media Player, and others.

Toggle overlay visibility by pressing the key sequence 0 0 0 1.

The overlay always stays on top of other windows.

The Exit Spotify button kills the Spotify app if needed.

Disclaimer
Use this app responsibly. It accesses your Spotify account and controls media playback system-wide.

Keep your Spotify credentials private.
