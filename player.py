import os
import sys
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from PIL import Image, ImageTk
import numpy as np


def resource_path(relative_path):
    
    try:
     base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


root = Tk()
root.title("Janith's Media Player")
root.geometry("600x750")
root.configure(bg="#0f0f0f")
root.minsize(500, 400)


logo_path = resource_path("Assets/logojdr.png")
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path).resize((32, 32))
    logo_icon = ImageTk.PhotoImage(logo_img)
    root.iconphoto(False, logo_icon)


mixer.init()


current_song = None
is_playing = False
is_paused = False


def load_icon(name, size=(40, 40)):
    path = resource_path(os.path.join("Assets", name))
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)

play_icon = load_icon("play1.png")
pause_icon = load_icon("pause1.png")
stop_icon = load_icon("stop1.png")
next_icon = load_icon("next1.png")


def browse_music():
    folder = filedialog.askdirectory()
    if not folder:
        return
    os.chdir(folder)
    Playlist.delete(0, END)
    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            Playlist.insert(END, file)

def play_music():
    global current_song, is_playing, is_paused
    try:
        song = Playlist.get(ACTIVE)
    except:
        return
    if not song:
        return
    current_song = song
    now_playing.config(text=song)
    mixer.music.load(song)
    mixer.music.play()
    is_playing = True
    is_paused = False
    update_progress()

def pause_music():
    global is_paused
    if not is_playing:
        return
    if is_paused:
        mixer.music.unpause()
        is_paused = False
    else:
        mixer.music.pause()
        is_paused = True

def stop_music():
    global is_playing, is_paused
    mixer.music.stop()
    is_playing = False
    is_paused = False
    progress.set(0)
    now_playing.config(text="Stopped")

def next_song():
    if Playlist.size() == 0:
        return
    current = Playlist.curselection()
    index = 0 if not current else (current[0] + 1) % Playlist.size()
    Playlist.select_clear(0, END)
    Playlist.select_set(index)
    Playlist.activate(index)
    play_music()

def set_volume(val):
    mixer.music.set_volume(float(val)/100)

def update_progress():
    if is_playing:
        if mixer.music.get_busy():
            pos = mixer.music.get_pos()/1000
            progress.set(pos % 100)
            root.after(1000, update_progress)
        else:
            if is_playing:
                next_song()


viz_canvas = Canvas(root, width=580, height=80, bg="#0f0f0f", highlightthickness=0)
viz_canvas.pack(pady=5)

bars = [viz_canvas.create_rectangle(i*18, 80, i*18+12, 80, fill="#9b59b6") for i in range(30)]

def animate_visualizer():
    if mixer.music.get_busy():
        data = np.random.rand(30)
        for i, bar in enumerate(bars):
            h = int(data[i]*80)
            viz_canvas.coords(bar, i*18, 80-h, i*18+12, 80)
    root.after(80, animate_visualizer)

animate_visualizer()


top = Frame(root, bg="#0f0f0f")
top.pack(fill=X, pady=5)

Label(top, text="🎧🎵 Janith Rathnayake Creations", bg="#0f0f0f", fg="#9b59b6",
      font=("Segoe UI", 16, "bold")).pack(side=LEFT, padx=10)

Button(top, text="Browse Media", bg="#9b59b6", fg="white", font=("Segoe UI", 10, "bold"),
       bd=0, command=browse_music, cursor="hand2").pack(side=RIGHT, padx=10, ipadx=10, ipady=5)


if not os.path.exists(logo_path):
    img = Image.new("RGB", (200, 200), "black")
else:
    img = Image.open(logo_path)
img = img.resize((150, 150))
album_img = ImageTk.PhotoImage(img)
Label(root, image=album_img, bg="#0f0f0f").pack(pady=5)


now_playing = Label(root, text="No song playing", bg="#0f0f0f", fg="#9b59b6", font=("Segoe UI", 12))
now_playing.pack(pady=5)


frame = Frame(root, bg="#181818")
frame.pack(padx=10, pady=5, fill=BOTH, expand=True)

scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=Y)

Playlist = Listbox(frame, bg="#181818", fg="white", font=("Segoe UI", 10),
                   selectbackground="#9b59b6", bd=0, yscrollcommand=scroll.set)
Playlist.pack(fill=BOTH, expand=True)
scroll.config(command=Playlist.yview)


progress = DoubleVar()
progress_bar = Scale(root, variable=progress, from_=0, to=100, orient=HORIZONTAL,
                     bg="#0f0f0f", fg="white", troughcolor="#8e44ad",
                     highlightthickness=0, length=560)
progress_bar.pack(pady=5)


controls = Frame(root, bg="#0f0f0f")
controls.pack(pady=5)

def make_btn(icon, cmd, color="#9b59b6"):
    btn = Button(controls, image=icon, command=cmd, bg=color,
                 activebackground=color, bd=0, highlightthickness=0, cursor="hand2")
    btn.config(relief=FLAT)
    btn.bind("<Enter>", lambda e: btn.config(bg="#8e44ad"))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

btn_play = make_btn(play_icon, play_music)
btn_pause = make_btn(pause_icon, pause_music)
btn_stop = make_btn(stop_icon, stop_music)
btn_next = make_btn(next_icon, next_song)

btn_play.grid(row=0, column=0, padx=10)
btn_pause.grid(row=0, column=1, padx=10)
btn_stop.grid(row=0, column=2, padx=10)
btn_next.grid(row=0, column=3, padx=10)


volume_frame = Frame(root, bg="#0f0f0f")
volume_frame.pack(pady=5)

Label(volume_frame, text="🔊", bg="#0f0f0f", fg="#9b59b6").pack(side=LEFT)

volume_slider = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL,
                      command=set_volume, bg="#0f0f0f", fg="white",
                      troughcolor="#9b59b6", highlightthickness=0, length=300)
volume_slider.set(70)
volume_slider.pack(side=LEFT)


root.mainloop()


# Janith Rathnayake Creations , special thanks to my friend for the help in creating this media player. This is a simple music player built using Python's Tkinter for the GUI and Pygame's mixer for audio playback. It allows you to browse for music files, play, pause, stop, and skip tracks, as well as adjust the volume. The visualizer is a fun addition that simulates audio visualization using random data.