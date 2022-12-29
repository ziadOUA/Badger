# -*- coding: utf-8 -*-

import os
import time
import random

import requests
import io
import zipfile
import shutil

from datetime import date

from pyfiglet import Figlet
from colorama import Fore, Back, init

init(convert=True)

start = Figlet(font='univers')

today = date.today()
today = today.strftime("%d/%m/%Y")

base_link = 'https://ziadoua.github.io/m3-Markdown-Badges/badges'
repo_branch_link = 'https://github.com/ziadOUA/m3-Markdown-Badges/archive/refs/heads/master.zip'
badge_list_dir = 'temp/m3-Markdown-Badges-master/badges'

svg_extension = '.svg'
space = ' '

done = False
valid = False
variant = None

available_badge_list = []
badges_available = []
badge_list = []
user_badges = []
user_badge_list = []
folder_names = []


def badger():

    badge_user_input()
    badge_lister()
    badge_comparator()
    if len(badge_list) > 0:
        variant_selector()
        html_tag_printer()
        markdown()


def badge_user_input():
    global user_badges
    user_badges = str(input('Enter the badges you need, separated by a space >>> '))
    user_badges = user_badges.split(space)
    while '' in user_badges:
        user_badges.remove('')
    for i in user_badges:
        user_badge_list.append(i.lower())
    user_badge_list.sort()


def zip_fetcher():
    request = requests.get(repo_branch_link)
    zip_file = zipfile.ZipFile(io.BytesIO(request.content))
    zip_file.extractall('temp/')


def badge_lister():
    global badges_available
    badges_available = os.listdir(badge_list_dir)
    shutil.rmtree('temp/m3-Markdown-Badges-master')
    for i in badges_available:
        available_badge_list.append(i.lower())
    for i in badges_available:
        if i.lower() in user_badge_list:
            folder_names.append(i)
        else:
            continue


def badge_comparator():
    if user_badge_list == ['*']:
        for i in badges_available:
            badge_list.append(i)
            folder_names.append(i)
        pass
    else:
        for wanted_badge in user_badge_list:
            if wanted_badge in available_badge_list:
                badge_list.append(wanted_badge)
            else:
                print(f'{Fore.YELLOW}Badge "{wanted_badge}" unavailable{Fore.RESET}')


def variant_selector():
    global valid
    global variant
    new_line()
    while not valid:
        variants_wanted = str(input('Chose what variant you want\n 1: Variant 1\n 2: Variant 2\n 3: Variant 3\n R: '
                                    'Randomize\n *: All variants\n>>> '))
        if variants_wanted in ['1', '2', '3']:
            variant = int(variants_wanted)
            valid = True
        elif variants_wanted == '*':
            variant = 4
            valid = True
        elif variants_wanted in ['r', 'R']:
            variant = 5
            valid = True
    valid = False


def html_tag_printer():
    badge_list.sort()
    folder_names.sort()
    new_line()
    for i in folder_names:
        if variant in [1, 2, 3]:
            badge_tag = f'<img src="{base_link}/{i}/{i.lower()}{variant}{svg_extension}">'
            print(badge_tag)
        if variant == 4:
            for j in range(3):
                badge_tag = f'<img src="{base_link}/{i}/{i.lower()}{j + 1}{svg_extension}">'
                print(badge_tag)
        if variant == 5:
            badge_tag = f'<img src="{base_link}/{i}/{i.lower()}{random.randint(1, 3)}{svg_extension}">'
            print(badge_tag)


def markdown():
    global valid
    new_line()
    while not valid:
        is_markdown_mode = input('Print the markdown table for theses badges ?\n Y: yes\n N: no\n>>> ')
        if is_markdown_mode in ['y', 'Y']:
            valid = True
            new_line()
            for i in folder_names:
                for j in range(3):
                    badge_tag = f'| <img src="{base_link}/{i}/{i.lower()}{j + 1}{svg_extension}"> | `{base_link}' \
                                f'/{i}/{i.lower()}{j + 1}{svg_extension}` | '
                    print(badge_tag)
        elif is_markdown_mode in ['n', 'N']:
            valid = True
    valid = False


def error(error_type=None):
    if error_type == 'zip_fetch':
        print(f'{Fore.RED}Failed to fetch the badge list{Fore.RESET}', end='\n\n')
        print('The program will close in 3 seconds')
        time.sleep(3)
        exit()


def new_line():
    print('')


if __name__ == '__main__':
    while not done:
        os.system('cls')
        available_badge_list = []
        badge_list = []
        user_badge_list = []
        folder_names = []
        valid = False
        done = False
        print(start.renderText('Badger'))
        try:
            zip_fetcher()
        except zipfile.BadZipfile:
            error(error_type='zip_fetch')
        badge_number = len(next(os.walk(badge_list_dir))[1])
        print(f'{today}: There are {Back.WHITE + Fore.BLACK}{badge_number}{Back.RESET + Fore.RESET} badges available !')
        new_line()
        badger()
        new_line()
        while not valid:
            is_user_done = input('Leave ?\n Y: yes\n N: no\n>>> ')
            if is_user_done in ['y', 'Y']:
                valid = True
                done = True
            elif is_user_done in ['n', 'N']:
                valid = True
                done = False

print(start.renderText('Badger'))
time.sleep(3)
exit()
