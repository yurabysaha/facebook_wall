import Tkinter as tk
import threading
import webbrowser
import facebook
import sqlite3 as db

PORT_NUMBER = 8000
APP_ID = 222805424880776
APP_SECRET = '36f97d6ee25af24899a40b3124b5ff9f'
REDIRECT_URL = 'http://localhost:8000/'


class UsersView:
    def __init__(self, root, frames, textfield):
        self.id = 80
        self.root = root
        self.frames = frames
        self.text = textfield
        self.body = tk.Frame(root, bg='#e6e6e6')
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

        self.update_mess_btn = tk.Button(self.listFrame,
                                         text='Add Facebook profile',
                                         fg='#ffffff',
                                         bg='#3b5998', activebackground='#3b5998',
                                         borderwidth=0,
                                         highlightthickness=0,
                                         width=18, height=2)

        self.update_mess_btn.bind("<Button-1>", self.add_new_fb_user)
        self.update_mess_btn.place(x=110, y=5)

        tk.Label(self.listFrame, text='ID', bg='#e6e6e6').place(x=10, y=50)
        tk.Label(self.listFrame, text='User Name', bg='#e6e6e6').place(x=150, y=50)
        tk.Label(self.listFrame, text='Fetch', bg='#e6e6e6').place(x=250, y=50)
        tk.Label(self.listFrame, text='Options', bg='#e6e6e6').place(x=300, y=50)

        con = db.connect(database="../db")
        cur = con.cursor()
        for i in cur.execute("SELECT * FROM users;"):
            tk.Label(self.listFrame, text=str(i[1]), bg='#e6e6e6').place(x=10, y=self.id)
            tk.Label(self.listFrame, text=i[2], bg='#e6e6e6').place(x=150, y=self.id)
            if i[4] == 1:
                text = 'Yes'
            else:
                text = 'No'
            btn = tk.Button(self.listFrame, text=text, fg='#2a416f', bg='#ffffff', width=4, borderwidth=1)
            btn.place(x=250, y=self.id)
            btn.bind("<Button-1>", lambda event, user=i: self.change_fetch(event, user))

            delete_btn = tk.Button(self.listFrame, text='Delete', fg='#2a416f', bg='#ffffff', width=5, borderwidth=1)
            delete_btn.place(x=310, y=self.id)
            delete_btn.bind("<Button-1>", lambda event, user=i: self.delete_user(event, user))

            self.id += 30

    def add_new_fb_user(self, event):
            graph = facebook
            perms = ['user_friends', 'user_status', 'user_about_me']
            fb_login_url = graph.auth_url(APP_ID, REDIRECT_URL, perms)
            get = webbrowser.open(fb_login_url)

    def change_fetch(self, event, user):
        con = db.connect(database="../db")
        cur = con.cursor()
        user = cur.execute("SELECT * FROM users WHERE id=?", (user[0],)).fetchone()
        if not user[4]:
            cur.execute("UPDATE groups SET scrup=1 WHERE owner=?", (user[2],))
            cur.execute("UPDATE users SET scrup_all=1 WHERE id=?", (user[0],))
            con.commit()
            con.close()
            event.widget.config(text='Yes')
            return
        else:
            cur.execute("UPDATE groups SET scrup=0 WHERE owner=?", (user[2],))
            cur.execute("UPDATE users SET scrup_all=0 WHERE id=?", (user[0],))
            con.commit()
            con.close()
            event.widget.config(text='No')
            return

    def delete_user(self, event, user):
        con = db.connect(database="../db")
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (user[0],))
        con.commit()
        con.close()
        for child in self.listFrame.winfo_children():
            child.destroy()
        UsersView(self.root, self.frames, self.text)
