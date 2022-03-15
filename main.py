import math
import random
from pygame import mixer, init
from tkinter import *
import vlc

# ---------------------------- CONSTANTS ------------------------------- #
reg = 0
PINK = "#e2979c"
RED = "#e7305b"
BLACK = "#000000"
FONT_NAME = "Arial"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
check_mark = ""
display_time = None
paused = False
music_state = 0


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reg
    window.after_cancel(display_time)
    text.config(text="Timer")
    reg = 0
    canvas.itemconfig(canvas_text, text="00:00")
    check_marks.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer():
    window.attributes('-topmost', 1)
    alarm_sound = vlc.MediaPlayer("C:\\Users\\Harini\\Downloads\\PyCharm.webm")
    alarm_sound.play()
    global reg
    reg += 1
    if reg == 8:
        countdown(LONG_BREAK_MIN * 60)
        text.config(text="LONG BREAK", fg=RED)
        reg = 0

    elif reg % 2 == 0:
        countdown(SHORT_BREAK_MIN * 60)
        text.config(text="BREAK", fg=RED)
        check()

    elif reg % 2 != 0:
        countdown(WORK_MIN * 60)
        text.config(text="Work", fg=RED)
    window.attributes('-topmost', 0)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global check_mark
    remain_min = math.floor(count / 60)
    remain_sec = count % 60
    if remain_sec < 10:
        remain_sec = f"0{remain_sec}"
    canvas.itemconfig(canvas_text, text=f"{remain_min}:{remain_sec}")
    if count > 0:
        global display_time
        display_time = window.after(1000, countdown, count - 1)
    elif count == 0:
        timer()
        check_mark = "✔"


def check():
    global check_mark
    check_mark = "✔"
    check_marks.config(text=check_mark)
    check_mark += " ✔"


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.iconphoto(True, PhotoImage(file="C:\\Users\\Harini\\Desktop\\100 Days of Code\\Pomodoro\\2_clocks.png"))
window.title("Health Timer")
window.config(padx=20, pady=20, bg=BLACK)
window.resizable(width=False, height=False)

# Creating the canvas and the time
canvas = Canvas(width=300, height=300, bg=BLACK, highlightthickness=0)
total_img = PhotoImage(file="2_clocks.png")
canvas.create_image(150, 100, image=total_img)
canvas.grid(row=1, column=1)
canvas_text = canvas.create_text(150, 230, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

# Labels
text = Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=PINK, bg=BLACK, highlightthickness=0)
text.grid(row=0, column=1)
check_marks = Label(text=check_mark, font=(FONT_NAME, 12, "bold"), fg=RED, bg=BLACK, highlightthickness=0)
check_marks.grid(row=3, column=1)

stop_image = PhotoImage(file="images\\stop50.png")
play_song = PhotoImage(file="images\\play50.png")
pause_song = PhotoImage(file="images\\pause50.png")

mrl1 = "songs_collection\\See You Again.mp3"
mrl2 = "songs_collection\\COME ON COME ON TURN THE RADIO ON.mp3"
mrl3 = "songs_collection\\Let me love you.mp3"
mrl4 = "songs_collection\\Love Me Like You Do.mp3"
mrl5 = "songs_collection\\Pearl Princess.mp3"
mrl6 = "songs_collection\\I Think I Love You.mp3"
mrl7 = "songs_collection\\Perfect.mp3"

song_list = [mrl1, mrl2, mrl3, mrl4, mrl5, mrl6, mrl7]

# ---------------------------- PLAY MUSIC -------------------------------- #
# Stop playing the current song
def music_stop():
    global music_state
    mixer.music.stop()
    music_state = 1
    mixer.stop()


def music_on():
    global music_state
    music_state = 0
    if music_state == 0:
        random.shuffle(song_list)
        mixer.get_init()
        mixer.init()
        mixer.music.load(random.choice(song_list))
        mixer.music.set_volume(0.7)
        mixer.music.play(0)
        check_if_finished()


def check_if_finished():
    global music_state, paused
    if music_state != 1:
        if not mixer.music.get_busy() and paused == False:
            window.after(ms=1, func=music_on)
        window.after(ms=1, func=check_if_finished)


# Pause and unpause the current song
def music_pause():
    global paused
    # pause
    if not paused:
        mixer.music.pause()
        paused = True
    # unpause
    else:
        mixer.music.unpause()
        paused = False

# Buttons
start_button = Button(text="Start", font=(FONT_NAME, 16, "bold"), highlightthickness=0, command=timer)
start_button.grid(row=2, column=0)
restart_button = Button(text="Restart", font=(FONT_NAME, 16, "bold"), highlightthickness=0, command=reset)
restart_button.grid(row=2, column=2)
stop_button = Button(image=stop_image, bg=BLACK, borderwidth=0, command=music_stop)
stop_button.place(x=260, y=320)
play_button = Button(image=play_song, bg=BLACK, borderwidth=0, command=music_on)
play_button.place(x=195, y=320)
pause_button = Button(image=pause_song, bg=BLACK, borderwidth=0, command=music_pause)
pause_button.place(x=125, y=320)

window.mainloop()
