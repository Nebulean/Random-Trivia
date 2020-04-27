#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import consolemenu as cm # to make menues
import json
import urllib.request as url # to download
import html
import random
from time import sleep
from playsound import playsound

# We first get all the categories
link = "https://opentdb.com/api_category.php"
with url.urlopen(link) as f:
    categories = json.loads(f.read().decode())

categories_name = []
categories_index = []
for cat in categories['trivia_categories']:
    # print(cat['name'])
    categories_name.append(cat['name'])
    categories_index.append(cat['id'])
categories_name.append('Any Categories')
categories_index.append(-1)

# print(categories_name)
# print(categories_index)

# We choose a category
menu = cm.SelectionMenu(categories_name, "Please choose a category.")
menu.show()
menu.join()
selection = menu.selected_option

if selection == len(categories_name):
    print("OK, bye.")
    quit()
elif categories_index[selection] == -1:
    str_category = ""
else:
    str_category = "&category=" + str(categories_index[selection])

# We select the amount of questions to load
# By default: 10 questions.
str_question = "amount=10"

# We select difficulty
difficulties = ['easy', 'medium', 'hard']
menu = cm.SelectionMenu(difficulties, "Please choose a difficulty.")
menu.show()
menu.join()
selection = menu.selected_option

if selection == len(difficulties):
    print("OK, bye.")
    quit()
else:
    str_difficulty = "&difficulty=" + difficulties[selection]
print("passed")

# We finally get our URL.
link = "https://opentdb.com/api.php?" + str_question + str_category + str_difficulty
print("Data URL: " + link)
with url.urlopen(link) as f:
    data = json.loads(f.read().decode())

for q in data['results']:
    # print("Now is the time for a question!")
    answers = ['Direct answer [3pts if correct]', 'Multiple Choice [1pts if correct]']
    menu = cm.SelectionMenu(answers, html.unescape(q['question']))
    menu.show()
    menu.join()
    selection = menu.selected_option

    if selection == len(answers):
        print("OK, bye.")
        quit()
    elif selection == 0:
        answer = 'It was: '
    else:
        # We add all the wrong answers
        possibilities = []
        for a in q['incorrect_answers']:
            possibilities.append(html.unescape(a))

        # Choose where to put the right question, and we insert it.
        number = random.randint(0, len(possibilities))
        possibilities.insert(number, html.unescape(q['correct_answer']))

        # print(possibilities)
        menu = cm.SelectionMenu(possibilities, html.unescape(q['question']))
        menu.show()
        menu.join()
        selection = menu.selected_option

        if selection == len(possibilities):
            print("OK, bye.")
            quit()
        elif selection == number:
            answer = 'Correct! The answer was: '
        else:
            answer = 'Wrong! The answer was: '

    select = ["Continue"]
    menu = cm.SelectionMenu(select, answer + html.unescape(q['correct_answer']))
    menu.show()
    menu.join()
    selection = menu.selected_option

    if selection == len(select):
        print("OK, bye.")
        quit()
    else:
        pass
