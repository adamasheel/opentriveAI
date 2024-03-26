import tkinter as t
import requests
import random
import html # For un-escaping HTML entities (&lt; ===> '<').

# API url: 'https://opentdb.com/api.php'  (<-- base url)  '?'   'amount=10'  (<-- one parameter) '&'  'type=boolean'  (<-- another parameter).
# api_link = "https://opentdb.com/api.php?amount=10&type=boolean"
# (Open Trivia Database API).
api_link = "https://opentdb.com/api.php"  # Using Base URL, we will have to pass parameters ourselves.
api_parameters = {
    'amount': 10,
    'type': 'boolean'
}

#######################  GET QUESTIONS FROM API  ###############
# Getting 10 true/false questions.
def get_questions():
    response = requests.get(url=api_link, params=api_parameters)
    response.raise_for_status()
    data = response.json()
    return(data['results'])

########################  GAME VARIABLES  ####################
sc = 0  # To keep track of score.
q_list = get_questions()
font1 = ("Times New Roman", 15, 'normal')
font2 = ("Arial", 20, 'italic')
q_color = "#171717"
bg_color = "#2a0944"
cd_color = "#fec260"
ques = random.choice(q_list)
k = None  # for window.after() events.

######################### BUTTON FUNCTIONS  ###################
def res_true():
    global ques, sc, q_list, k
    if(len(q_list) == 0):  # No remaining questions.
        pass
    else:
        if(ques['correct_answer'] == "True"):
            # Player is correct.
            sc += 1
            card.config(bg='green')
            score.config(text=f"Score: {sc}")
        else:
            # Player is incorrect.
            card.config(bg='red')
        # We should remove question from q_list only after it
        # has been attempted.
        q_list.remove(ques)
        if(k != None):
            window.after_cancel(k)
        k = window.after(2000, update_card)

def res_false():
    global ques, sc, q_list, k
    if(len(q_list) == 0):  # No remaining questions.
        pass
    else:
        if(ques['correct_answer'] == "False"):
            # Player is correct.
            sc += 1
            card.config(bg='green')
            score.config(text=f"Score: {sc}")
        else:
            # Player is incorrect.
            card.config(bg='red')
        q_list.remove(ques)
        if(k != None):
            window.after_cancel(k)
        k = window.after(2000, update_card)

#########################  UPDATE QUESTION CARD  ##################
def update_card():
    global ques, q_list
    card.config(bg=cd_color)
    if(len(q_list) == 0):  # No remaining questions.
        card.itemconfig(card_txt, text=f"Game Over!!!\nYour Final Score: {sc}")
    else:
        ques = random.choice(q_list)
        card.itemconfig(card_txt, text=html.unescape(ques['question']))

#########################  UI SETUP  #########################
# Set Up Window.
window = t.Tk()
window.title("Quizzy!")
window.config(bg=bg_color, padx=50, pady=20)

# Set Up Score Label:
score = t.Label(text=f"Score: {sc}", font=font1, fg='white', bg=bg_color)
score.config(pady=10)
score.grid(column=3, row=0)

# Blank Row to create space between buttons and card :)
b_row = t.Label(text='', bg=bg_color, fg=bg_color)
b_row.grid(column=2, row=2)

# Set Up Canvas to display question.
card = t.Canvas(bg=cd_color, width=600, height=400, highlightthickness=0)
card.grid(column=1, row=1, columnspan=3)
# Unescaping HTML entities before displaying question. (Using html module).
card_txt = card.create_text(300, 200, text=html.unescape(ques['question']), font=font2, fill=q_color, width=400)

# Set Up Buttons.
# True btn.
true_img = t.PhotoImage(file='true.png')
true_btn = t.Button(image=true_img, highlightthickness=0, border=0, command=res_true)
true_btn.grid(column=1, row=3)

# False btn.
false_img = t.PhotoImage(file='false.png')
false_btn = t.Button(image=false_img, highlightthickness=0, border=0, command=res_false)
false_btn.grid(column=3, row=3)

# To keep window displayed.
window.mainloop()