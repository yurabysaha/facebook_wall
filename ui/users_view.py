import Tkinter as tk
import threading
import webbrowser
import facebook
import sqlite3 as db

from selenium import webdriver

from db_module import add_new_user

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

        tk.Label(self.listFrame, text='Login', bg='#e6e6e6', fg='#2c2d30').place(x=0, y=5)
        tk.Label(self.listFrame, text='Password', bg='#e6e6e6', fg='#2c2d30').place(x=0, y=25)
        self.login = tk.Entry(self.listFrame, width=26)
        self.login.place(x=60, y=5)
        self.passw = tk.Entry(self.listFrame, width=26)
        self.passw.place(x=60, y=25)

        self.update_mess_btn = tk.Button(self.listFrame,
                                         text='Add Facebook profile',
                                         fg='#ffffff',
                                         bg='#3b5998', activebackground='#3b5998',
                                         borderwidth=0,
                                         highlightthickness=0,
                                         width=18, height=2)

        self.update_mess_btn.bind("<Button-1>", self.add_new_fb_user)
        self.update_mess_btn.place(x=230, y=5)

        tk.Label(self.listFrame, text='Facebook id', bg='#e6e6e6', fg='#2c2d30').place(x=10, y=50)
        tk.Label(self.listFrame, text='User Name', bg='#e6e6e6', fg='#2c2d30').place(x=140, y=50)
        tk.Label(self.listFrame, text='Fetch', bg='#e6e6e6', fg='#2c2d30').place(x=250, y=50)
        tk.Label(self.listFrame, text='Options', bg='#e6e6e6', fg='#2c2d30').place(x=300, y=50)

        con = db.connect(database="../db")
        cur = con.cursor()
        for i in cur.execute("SELECT * FROM users;"):
            tk.Label(self.listFrame, text=str(i[1]), bg='#e6e6e6').place(x=10, y=self.id)
            tk.Label(self.listFrame, text=i[2], bg='#e6e6e6').place(x=140, y=self.id)
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
            # graph = facebook
            # perms = ['publish_actions', 'user_managed_groups', 'user_groups']
            # fb_login_url = graph.auth_url(APP_ID, REDIRECT_URL, perms)
            # get = webbrowser.open(fb_login_url)

            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument('--lang=en')
            chrome_options.add_argument("start-maximized")
            self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
            # self.chrome = webdriver.Chrome(executable_path='../chromedriver'.format(os.getcwd()),
            #                                chrome_options=chrome_options)
            self.chrome.get('https://www.facebook.com/login/?next=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2F145634995501895%2F')
            self.chrome.find_element_by_id('email').send_keys(self.login.get())
            self.chrome.find_element_by_id('pass').send_keys(self.passw.get())
            self.chrome.find_element_by_id('pass').submit()
            self.chrome.get('https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me%3F&version=v2.3')
            token = self.chrome.find_element_by_xpath('//div/div[2]/div/div[1]/label/input').get_attribute('value')
            self.chrome.close()
            graph = facebook.GraphAPI(access_token=token, version='2.3')
            w = graph.get_object('me')
            add_new_user(token, w, self.login.get(), self.passw.get())
            UsersView(self.root, self.frames, self.text)

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
