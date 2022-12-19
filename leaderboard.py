import json
import os

scores = []
highscores = open("scores.dat")


def show_scores():
    scores.append(json.loads(highscores.read()))


def add_score(name, number):
    playerscore = (name, number)
    scores.append(playerscore)

    highscores.write(json.dumps(scores))
    highscores.close()


def filter_score():
    scores.sort()
