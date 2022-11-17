from tkinter import *
from random import choice
import pandas


BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
CURRENT_CARD = {}
TO_LEARN = {}


# ----------------------- CREATE NEW FLASH CARDS ----------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    TO_LEARN = original_data.to_dict(orient="records")
else:
    TO_LEARN = data.to_dict(orient="records")


def next_card():
    global CURRENT_CARD, flip_timer
    window.after_cancel(flip_timer)

    CURRENT_CARD = choice(TO_LEARN)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=CURRENT_CARD["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=CURRENT_CARD["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    TO_LEARN.remove(CURRENT_CARD)
    data = pandas.DataFrame(TO_LEARN)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# -------------------------------- UI SETUP -----------------------------------#
window = Tk()
window.title("FlashLearn")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(ms=3000, func=flip_card)

# Flash Card Canvas
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=TITLE_FONT)
card_word = canvas.create_text(400, 263, text="word", font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0)
wrong_button.configure(command=next_card)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0)
right_button.configure(command=is_known)
right_button.grid(column=1, row=1)

next_card()


window.mainloop()
