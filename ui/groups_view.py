import Tkinter as tk
import threading
import tkMessageBox
import webbrowser
from ttk import Combobox

import facebook
import sqlite3 as db

from db_module import add_new_group, update_group_fetch


class GroupsView:
    def __init__(self, root, frames, textfield):
        self.id = 5
        self.root = root
        self.frames = frames
        self.text = textfield
        self.body = tk.Frame(self.root, bg='#e6e6e6')
        frames['connect'] = self.body

        self.body.place(x=120, y=0, width=380, height=500)
        canvas = tk.Canvas(self.body, bg='#e6e6e6')
        self.listFrame = tk.Frame(canvas, width=380, height=500, bg='#e6e6e6')
        scrollb = tk.Scrollbar(self.body, orient="vertical", command=canvas.yview)
        scrollb.pack(side='right', fill='y')  # grid scrollbar in master, but
        canvas['yscrollcommand'] = scrollb.set  # attach scrollbar to frameTwo

        def AuxscrollFunction(event):
            # You need to set a max size for frameTwo. Otherwise, it will grow as needed, and scrollbar do not act
            canvas.configure(scrollregion=canvas.bbox("all"), width=380, height=500)
            # canvas.configure(scrollregion=canvas.bbox("all"))

        self.listFrame.bind("<Configure>", AuxscrollFunction)
        canvas.create_window((10, 10), window=self.listFrame, anchor='w')
        canvas.pack()

        self.input_link = tk.Entry(self.listFrame, width=30)
        self.input_link.place(x=35, y=10)

        tk.Label(self.listFrame, text=' Link ', bg='#e6e6e6').place(x=0, y=10)
        tk.Label(self.listFrame, text=' Owner ', bg='#e6e6e6').place(x=0, y=30)
        con = db.connect(database="../db")
        cur = con.cursor()
        users = []
        for i in cur.execute("SELECT name FROM users;"):
            users.append(i[0])
        self.combobox = Combobox(self.listFrame, values=users)
        self.combobox.current()
        self.combobox.configure(state='readonly')
        # self.combobox.bind("<<ComboboxSelected>>", self.select_owner)
        self.combobox.place(x=50, y=30)

        self.add_group_btn = tk.Button(self.listFrame,
                                         text='Add Group',
                                         fg='#ffffff',
                                         bg='#3b5998', activebackground='#3b5998',
                                         borderwidth=0,
                                         highlightthickness=0,
                                         width=16, height=2)

        self.add_group_btn.bind("<Button-1>", self.add_new_fb_group)
        self.add_group_btn.place(x=240, y=5)

        tk.Label(self.listFrame, text='Link', bg='#e6e6e6', fg='#2c2d30').place(x=20, y=80)
        tk.Label(self.listFrame, text='Owner', bg='#e6e6e6', fg='#2c2d30').place(x=150, y=80)
        tk.Label(self.listFrame, text='Fetch', bg='#e6e6e6', fg='#2c2d30').place(x=250, y=80)
        tk.Label(self.listFrame, text='Options', bg='#e6e6e6', fg='#2c2d30').place(x=310, y=80)

        self.y_place = 110
        for i in cur.execute("SELECT * FROM groups;"):
            self.group_list(i)

    def add_new_fb_group(self, event):
        add_new_group(self.input_link.get(), self.combobox.get())
        tkMessageBox.showinfo(
            "Added",
            "New group added successful"
        )
        # Get last user for adding to UI
        con = db.connect(database="../db")
        cur = con.cursor()
        cur.execute("SELECT * FROM groups ORDER BY id DESC LIMIT 1")
        new_user = cur.fetchone()

        self.group_list(new_user)

    def group_list(self, i):
        link_url = '..' + str(i[1])[-20:]
        tk.Label(self.listFrame, text=link_url, bg='#e6e6e6').place(x=20, y=self.y_place)
        tk.Label(self.listFrame, text=i[2], bg='#e6e6e6').place(x=150, y=self.y_place)
        if i[3] == 1:
            text = 'Yes'
        else:
            text = 'No'
        btn = tk.Button(self.listFrame, text=text, fg='#2a416f', bg='#ffffff',  width=4, borderwidth=1)
        btn.place(x=250, y=self.y_place)
        btn.bind("<Button-1>", lambda event, group=i: self.change_fetch(event, group))

        delete_btn = tk.Button(self.listFrame, text='Delete', fg='#2a416f', bg='#ffffff', width=5, borderwidth=1)
        delete_btn.place(x=310, y=self.y_place)
        delete_btn.bind("<Button-1>", lambda event, group=i: self.delete_group(event, group))
        self.y_place += 30

    def change_fetch(self, event, group):
        con = db.connect(database="../db")
        cur = con.cursor()
        user = cur.execute("SELECT * FROM groups WHERE id=?", (group[0],)).fetchone()
        if user[3] == 0:
            update_group_fetch(user[0], True)
            event.widget.config(text='Yes')
            return
        else:
            update_group_fetch(user[0], False)
            event.widget.config(text='No')
            return

    def delete_group(self, event, group):
        con = db.connect(database="../db")
        cur = con.cursor()
        cur.execute("DELETE FROM groups WHERE id=?", (group[0],))
        con.commit()
        con.close()
        for child in self.listFrame.winfo_children():
            child.destroy()
        GroupsView(self.root, self.frames, self.text)
