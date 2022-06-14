from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(background_img, image=card_front)
    canvas.itemconfig(card_title, text="German", fill='black')
    canvas.itemconfig(card_word, text=current_card["German"], fill="black")
    flip_timer = window.after(3000, func=update_card)


def update_card():
    canvas.itemconfig(background_img, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def new_words():
    words_to_learn.remove(current_card)
    df = pd.DataFrame(words_to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flash Card")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
window.resizable(False, False)
flip_timer = window.after(3000, update_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
background_img = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

correct_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

# Reading CSV as pandas

data = pd.read_csv("data/german_words.csv")
to_learn = data.to_dict(orient="records")
try:
    data_words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_to_learn = to_learn
else:
    data_new_words = data_words.to_dict(orient="records")
    words_to_learn = data_new_words

# Canvas Text

card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"), text="Title")
card_word = canvas.create_text(400, 263, font=("Arial", 60, "bold"), text="word")


# Buttons

wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

correct_button = Button(image=correct_img, highlightthickness=0, command=next_card and new_words)
correct_button.grid(row=1, column=1)


next_card()
window.mainloop()
