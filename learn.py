import time

from num2words import num2words as words
import os
import random
from pygame import mixer
from webapi import download_sound


def expect_string(expected):
    inp = input("Write solution: ")
    if expected.strip() == inp:
        print("OK")
    else:
        print("WRONG, expected:", expected)


def play_sound(number, language_api, path):
    mixer.music.load(download_sound(number, language_api, path))
    mixer.music.play()
    time.sleep(2)
    mixer.music.play()
    time.sleep(2)


def learn(language_api, num_language, max_number=100):
    mixer.init()
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sounds", language_api)
    if not os.path.exists(path):
        os.makedirs(path)
    while True:
        number = random.randint(0, max_number)
        translated = words(number, lang=num_language)
        if random.randint(0, 3) == 0:
            print(translated)
            play_sound(number, language_api, path)
            expect_string(str(number))
        else:
            print(number)
            expect_string(translated)
            play_sound(number, language_api, path)
