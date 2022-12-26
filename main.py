# -*- coding: utf-8 -*-

import os
import time

import requests
import io
import zipfile
import shutil

from pyfiglet import Figlet
from colorama import Fore, Back,init

init(convert=True)

start = Figlet(font='univers')

base_link = 'https://ziadoua.github.io/m3-Markdown-Badges/badges'
repo_branch_link = 'https://github.com/ziadOUA/m3-Markdown-Badges/archive/refs/heads/master.zip'
badge_list_dir = 'temp/m3-Markdown-Badges-master/badges'

svg_extension = '.svg'
space = ' '

done = False
valid = False

available_badge_list = []
badge_list = []
user_badge_list = []
folder_names = []


def badger():

    badge_user_input()
    badge_lister()
    print('')
    badge_comparator()
    html_tag_printer()


def badge_user_input():
    user_badges = []
    user_badges = str(input('Enter the badges you need, separated by a space >>> '))
    user_badges = user_badges.split(space)
    for i in user_badges:
        user_badge_list.append(i.lower())
    user_badge_list.sort()


def zip_fetcher():
    request = requests.get(repo_branch_link)
    zip_file = zipfile.ZipFile(io.BytesIO(request.content))
    zip_file.extractall('temp/')


def badge_lister():
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
    for wanted_badge in user_badge_list:
        if wanted_badge in available_badge_list:
            badge_list.append(wanted_badge)
        else:
            print(f'{Fore.YELLOW}Badge "{wanted_badge}" unavailable{Fore.RESET}')


def html_tag_printer():
    badge_list.sort()
    folder_names.sort()
    print('')
    for i in folder_names:
        for j in range(3):
            badge_tag = f'<img src="{base_link}/{i}/{i.lower()}{j + 1}{svg_extension}">'
            print(badge_tag)


def error(error_type=None):
    if error_type == 'zip_fetch':
        print(f'{Fore.RED}Failed to fetch the badge list{Fore.RESET}')
        print('The program will close in 3 seconds')
        time.sleep(3)
        exit()


if __name__ == '__main__':
    while not done:
        os.system('cls')
        available_badge_list = []
        badge_list = []
        user_badge_list = []
        folder_names = []
        valid = False
        done = False
        print(start.renderText('badger'))
        try:
            zip_fetcher()
        except zipfile.BadZipfile:
            error(error_type='zip_fetch')
        print(f'ziadOUA : There are {Back.WHITE + Fore.BLACK}{len(next(os.walk(badge_list_dir))[1])}{Back.RESET + Fore.RESET} badges available !')
        print('')
        badger()
        print('')
        while not valid:
            is_user_done = input('Leave ?\n Y: yes\n N: no\n>>> ')
            if is_user_done in ['y', 'Y']:
                valid = True
                done = True
            elif is_user_done in ['n', 'N']:
                valid = True
                done = False

print(start.renderText('badger'))
time.sleep(3)
exit()
