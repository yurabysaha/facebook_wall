#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import sys
import threading
import db_module

import server
from ui.groups_view import GroupsView
from ui.users_view import UsersView
from ui.results_view import ResultsView


MAIN_BG = '#303030'

# Потрібно щоб не вискакувало вікно на віндовсі при закритті програми
# sys.stderr = open('error.log', 'w')
# sys.stdout = open('output.log', 'w')

root = tk.Tk()
root.title('Facebook')
root.configure(background=MAIN_BG)
root.resizable(width=False, height=False)
root.minsize(width=500, height=500)


menu = tk.Frame(root, bg=MAIN_BG)
body = tk.Frame(root, bg=MAIN_BG)
frames = {'logging': body}
textfield = tk.Text(body, width=47, height=30, bg='#e6e6e6')
textfield.place(x=0, y=4)
menu_btns = []


def open_logging(event):
    active_menu_btn(event)
    for i in frames:
        frames[i].place_forget()
    body.place(x=120, y=0, width=380, height=500)


def open_users(event):
    active_menu_btn(event)
    for i in frames:
        frames[i].place_forget()
    UsersView(root, frames, textfield)


def open_groups(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    GroupsView(root, frames, textfield)


def open_results(event):
    active_menu_btn(event)
    for i in frames:
            frames[i].place_forget()
    ResultsView(root, frames)


def active_menu_btn(event):
    for i in menu_btns:
        i.config(bg='#eeeeee', fg='#000000')
    event.widget.config(bg='#616161', fg='#ffffff')


class Menu:
    def __init__(self):
        self.logging_btn = tk.Button(menu,
                                     text='Process log',
                                     highlightbackground=MAIN_BG,
                                     bg='#eeeeee', activebackground=MAIN_BG,
                                     highlightcolor='#ff5722',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.logging_btn.bind("<Button-1>", open_logging)
        self.logging_btn.place(x=0, y=2)
        menu_btns.append(self.logging_btn)

        self.users_btn = tk.Button(menu,
                                     text='Users',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.users_btn.bind("<Button-1>", open_users)
        self.users_btn.place(x=0, y=40)
        menu_btns.append(self.users_btn)

        self.groups_btn = tk.Button(menu,
                                     text='Groups',
                                     highlightbackground=MAIN_BG,
                                     highlightcolor=MAIN_BG,
                                     bg='#eeeeee', activebackground='#e6e6e6',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.groups_btn.bind("<Button-1>", open_groups)
        self.groups_btn.place(x=0, y=78)
        menu_btns.append(self.groups_btn)

        self.results_btn = tk.Button(menu,
                                    text='Results',
                                    highlightbackground=MAIN_BG,
                                    highlightcolor=MAIN_BG,
                                    bg='#eeeeee', activebackground='#e6e6e6',
                                    borderwidth=0,
                                    highlightthickness=0,
                                    width=18, height=2)

        self.results_btn.bind("<Button-1>", open_results)
        self.results_btn.place(x=0, y=116)
        menu_btns.append(self.results_btn)


if __name__ == "__main__":
    menu.place(x=0, y=0, width=120, height=500)
    body.place(x=120, y=0, width=380, height=500)
    Menu()
    t = threading.Thread(target=server.Server)
    t.start()
    root.mainloop()
