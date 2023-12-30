from tkinter import *
from pygame import mixer
import math

# ---------------------------- CONSTANTS ------------------------------- #
MY_PINK = "#e2979c"  # Pink color code
MY_RED = "#e7305b"   # Red color code
MY_GREEN = "#9bdeac"  # Green color code
MY_YELLOW = "#f7f5dd"  # Yellow color code
FONT_NAME = "Courier"  # Font name
WORK_MIN = 25  # Work session duration in minutes
SHORT_BREAK_MIN = 5  # Short break duration in minutes
LONG_BREAK_MIN = 20  # Long break duration in minutes
reps = 0  # Number of work sessions completed
timer = None  # Timer variable


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """
    Reset the timer and update UI components.
    """
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_mark_label.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """
    Start the Pomodoro timer based on the current work session.
    """
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=MY_RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=MY_PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=MY_GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """
    Perform countdown and update UI components.
    """
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        play_sound()
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_mark_label.config(text=marks)


# ---------------------------- SOUND SETUP ------------------------------- #
def play_sound():
    """
    Play a sound when a work session is completed.
    """
    mixer.init()
    mixer.music.load("bell.mp3")
    mixer.music.play()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=MY_YELLOW)

window.after(1000, )
canvas = Canvas(width=200, height=224, bg=MY_YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Timer Label
title_label = Label(text="Timer", fg=MY_GREEN, bg=MY_YELLOW, font=(FONT_NAME, 50))
title_label.grid(row=0, column=1)

# Start button
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

# Reset button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

# Check mark
check_mark_label = Label(fg=MY_GREEN, bg=MY_YELLOW)
check_mark_label.grid(row=3, column=1)

window.mainloop()
