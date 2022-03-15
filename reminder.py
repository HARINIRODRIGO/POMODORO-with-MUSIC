import datetime
from datetime import datetime
import time
from tkinter import *
import vlc
from tkinter import messagebox

BLACK = "#000000"
ash = "#B2BEB5"
lines = 0
window1 = Tk()
window1.title("alarm clock")

day = int(time.strftime("%d"))

# Getting whether day is "th" or "nd"
if 4 <= day <= 20 or 24 <= day <= 30:
    suffix = "th"
    day = str(day)
    day += suffix
else:
    suffix = ["st", "nd", "rd"][day % 10 - 1]
    day = str(day)
    day += suffix

# Getting today's date Eg: Thursday 27th July
day = time.strftime(f"%A {day} %B")

window1.iconphoto(True, PhotoImage(file="C:\\Users\\Harini\\Desktop\\100 Days of Code\\Pomodoro\\clock_icon.png"))
window1.config(padx=50, pady=50, bg="#E6BF83")
window1.resizable(width=False, height=False)
frame1 = Frame(window1, width=350, height=450)
frame2 = Frame(window1, width=350, height=450)
frame3 = Frame(window1, width=350, height=450)
frame1.grid(column=0, row=0)
canvas = Canvas(frame1, width=300, height=400, bg="#808080", highlightthickness=0)
total_img = PhotoImage(file="2_clocks.png")
canvas.create_image(150, 150, image=total_img)
canvas.grid(row=0, column=0)

hour_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
mini_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
reminder_label = Label(frame1, text=" ", fg="black", font=("Arial", 18, "bold"), bg="#808080")
sec_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
pm_or_am_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")

# Alarm sound
alarm = vlc.MediaPlayer("songs_collection\\See You Again.mp3")


# Alarm function
def alarm_sound():
    alarm.play()


def add_data(date, h_val, m_val, s_val, pm_am, info):
    confirm = messagebox.askyesno(title="my events",
                                  message=f"{date.get()} {h_val.get()}:{m_val.get()}:{s_val.get()} "
                                          f"{pm_am.get()}\n{info.get(1.0, END)}\n\nDo you need "
                                          f"to save this event?")
    if confirm:
        with open('alarms.txt', "a") as file:
            file.write(f"{date.get()} {h_val.get()}:{m_val.get()}:{s_val.get()} {pm_am.get()}\n{info.get(1.0, END)}")


def save_changes(data):
    confirm = messagebox.askyesno(title="my events", message="Do you need to save changes")
    if confirm:
        d = ""
    with open('alarms.txt', "w") as file:
        for i in data.get(1.0, END):
            if i != "\n":
                d += i
            else:
                if d != "":
                    file.write(d + "\n")
                d = ""


def delete_alarm():
    global frame3
    frame1.destroy()
    frame2.destroy()
    frame3 = Frame(window1, width=350, height=450)
    frame3.grid(column=0, row=0)
    canvas2 = Canvas(frame3, width=380, height=450, bg="#808080", highlightthickness=0)
    canvas2.place(x=0, y=0)
    event = Text(frame3, width=30, height=13, font=("Arial", 18, "bold"))
    event.place(x=0, y=0)
    event.focus()
    with open('alarms.txt', "r") as file:
        event.insert(INSERT, file.read())

    back_button = Button(frame3, text="Back", fg="black", font=("Arial", 15, "bold"), bg=ash,
                         command=back)
    back_button.place(x=50, y=400)

    changes = Button(frame3, text="Save Changes", font=("Arial", 15, "bold"), bg=ash,
                     command=lambda: save_changes(event))
    changes.place(x=150, y=400)


def back():
    global frame1, canvas, total_img
    frame2.destroy()
    frame3.destroy()
    frame1 = Frame(window1, width=350, height=450)
    frame1.grid(column=0, row=0)
    canvas = Canvas(frame1, width=300, height=400, bg="#808080", highlightthickness=0)
    canvas.create_image(150, 150, image=total_img)
    canvas.grid(row=0, column=0)
    frame_1()


def stop_alarm():
    alarm.stop()
    reminder_label.after(ms=2000)
    reminder_label.config(text=" ")


# display time
def time_update():
    global frame1, hour_label, mini_label
    global reminder_label, sec_label, pm_or_am_label, lines

    hour = datetime.today().strftime("%I")
    mini = datetime.today().strftime("%M")
    sec = datetime.today().strftime("%S")
    pm_am = datetime.today().strftime("%p")

    current_time = f"{hour}:{mini}:{sec} {pm_am}"
    data = time.strftime("%d/%m/%Y") + " " + current_time + "\n"
    # Reading the text file
    with open('alarms.txt', "r") as file:
        alarms = file.readlines()
        for i in range(len(alarms)):
            if i % 2 == 0:
                if alarms[i] == data:
                    reminder_label = Label(frame1, text=alarms[i + 1], fg="black", font=("Arial", 18, "bold"),
                                           bg="#808080")
                    reminder_label.place(x=0, y=280)
                    alarm_sound()

    hour_label.config(text=f"{hour}")
    mini_label.config(text=f"{mini}")
    sec_label.config(text=f"{sec}")
    pm_or_am_label.config(text=f"{pm_am}")
    sec_label.after(1000, time_update)


def frame_2():
    global alarm_button, frame2
    frame1.destroy()
    frame3.destroy()
    frame2 = Frame(window1, width=350, height=450)
    frame2.grid(column=0, row=0)

    # Create Text field
    def add_alarm():
        canvas2 = Canvas(frame2, width=380, height=450, bg="#808080", highlightthickness=0)
        canvas2.place(x=0, y=0)

        # Event date label and entry
        date_label = Label(frame2, text="Date: ", font=("Arial", 18, "bold"), bg="#808080")
        date_label.place(x=2, y=20)
        event_date = Entry(frame2, width=10, font=("Arial", 18, "bold"))
        x = time.strftime("%d/%m/%Y")
        event_date.insert(0, f"{x}")
        event_date.place(x=80, y=20)

        # Event time label and entry
        time_label = Label(frame2, text="Time: ", font=("Arial", 18, "bold"), bg="#808080")
        time_label.place(x=0, y=95)

        # hour spinbox
        hour_time = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        hour_value = StringVar()
        hour_box = Spinbox(frame2,
                           values=hour_time, font=("Arial", 20, "bold"), width=2,
                           textvariable=hour_value, wrap=True)
        hour_value.set(time.strftime("%I"))
        hour_box.place(x=80, y=95)

        hour = Label(frame2, text="H", font=("Arial", 18, "bold"), bg="#808080")
        hour.place(x=86, y=60)

        # min spinbox
        min_time = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"
                                                                                                  "14", "15", "16",
                    "17",
                    "18", "19", "20", "21", "22", "23", "24", "25", "26", "27"
                                                                          "28", "29", "30", "31", "32", "33", "34",
                    "35",
                    "36", "37", "38", "39", "40", "41"
                                                  "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52",
                    "53",
                    "54", "55"
                          "56", "57", "58", "59", "60"]
        min_value = StringVar()
        min_box = Spinbox(frame2,
                          values=min_time, font=("Arial", 20, "bold"), width=2,
                          textvariable=min_value, wrap=True)
        min_value.set(time.strftime("%M"))
        min_box.place(x=150, y=95)

        min = Label(frame2, text="M", font=("Arial", 18, "bold"), bg="#808080")
        min.place(x=156, y=60)

        # sec spinbox
        sec_time = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"
                                                                                                  "14", "15", "16",
                    "17",
                    "18", "19", "20", "21", "22", "23", "24", "25", "26", "27"
                                                                          "28", "29", "30", "31", "32", "33", "34",
                    "35",
                    "36", "37", "38", "39", "40", "41"
                                                  "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52",
                    "53",
                    "54", "55",
                    "56", "57", "58", "59", "60"]
        sec_value = StringVar()
        sec_box = Spinbox(frame2,
                          values=sec_time, font=("Arial", 20, "bold"), width=2,
                          textvariable=sec_value, wrap=True)
        sec_value.set(time.strftime("%S"))
        sec_box.place(x=220, y=95)

        sec = Label(frame2, text="S", font=("Arial", 18, "bold"), bg="#808080")
        sec.place(x=226, y=60)

        # pm and am
        am_pm = ["AM", "PM"]
        am_pm_value = StringVar()
        am_pm_box = Spinbox(frame2,
                            values=am_pm, font=("Arial", 20, "bold"), width=3,
                            textvariable=am_pm_value, wrap=True
                            )
        am_pm_value.set(time.strftime("%p"))
        am_pm_box.place(x=280, y=95)

        # Event data
        event = Text(frame2, width=19, height=8, font=("Arial", 18, "bold"))
        event.place(x=50, y=150)
        event.focus()
        add_notifications = Button(frame2, text="+ Add", fg="black", font=("Arial", 15, "bold"), bg=ash,
                                   command=lambda: add_data(event_date, hour_value, min_value, sec_value, am_pm_value,
                                                            event))
        add_notifications.place(x=250, y=400)

        back_button = Button(frame2, text="Back", fg="black", font=("Arial", 15, "bold"), bg=ash,
                             command=back)

        back_button.place(x=150, y=400)

    add_alarm()


def frame_1():
    global frame1
    global hour_label
    global mini_label
    global reminder_label
    global sec_label
    global pm_or_am_label
    global alarm_button

    # Labels
    day_label = Label(frame1, text=f"{day}", fg="white", font=("Arial", 18, "bold"), bg="#808080")
    day_label.place(x=0, y=0)
    hour_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
    hour_label.place(x=50, y=140)
    mini_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
    mini_label.place(x=100, y=140)
    sec_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
    sec_label.place(x=150, y=140)
    pm_or_am_label = Label(frame1, text=" ", fg="white", font=("Arial", 25, "bold"), bg="black")
    pm_or_am_label.place(x=200, y=140)
    reminder_label = Label(frame1, text=" ", fg="black", font=("Arial", 18, "bold"), bg="#808080")
    reminder_label.place(x=0, y=280)
    time_update()

    # Button
    alarm_button = Button(frame1, text="Add", fg="black", font=("Arial", 15, "bold"), bg=ash, borderwidth=0,
                          command=frame_2)
    alarm_button.place(x=100, y=350)
    delete_button = Button(frame1, text="Delete", fg="black", font=("Arial", 15, "bold"), bg=ash, borderwidth=0,
                           command=delete_alarm)
    delete_button.place(x=190, y=350)
    stop_button = Button(frame1, text="Stop", fg="black", font=("Arial", 15, "bold"), bg=ash, borderwidth=0,
                         command=stop_alarm)
    stop_button.place(x=10, y=350)


# Stop alarm function
alarm_button = Button(frame1, text="Add", fg="black", font=("Arial", 15, "bold"), bg=ash, borderwidth=0,
                      command=frame_2)

frame_1()

window1.mainloop()
