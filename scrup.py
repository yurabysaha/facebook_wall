import threading

import facebook
import requests
import sqlite3 as db

from selenium import webdriver

from db_module import add_new_posts


class Scrup:

    def __init__(self):
        pass

    def _is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def getAllPostsFromGroup(self, token, group_url):
        self.graph = facebook.GraphAPI(access_token=token, version="2.3")
        self.my_profile = self.graph.get_object('me')
        user_id = self.my_profile['id']
        user_name = self.my_profile['name']
        # Get ID from group Url
        get_group_name = group_url.rstrip('/ ').split('/')[-1]
        if self._is_number(get_group_name):
            group_id = get_group_name
            group_name = self.graph.get_object(group_id)['name']
        else:
            resposne = self.graph.search(type='group', q=get_group_name)
            group_id = resposne['data'][0]['id']
            group_name = resposne['data'][0]['name']
        # ---------------------
        # Get feeds from Group
        data = self.graph.get_connections(group_id, 'feed')
        count_posts = 1
        while (data['data']):
            try:
                for post in data['data']:
                    print ("-------------"+str(count_posts)+"------------------")
                    try:
                        print ('Post was created: ' + post['created_time'])
                    except:
                        pass
                    try:
                        print ('Who create post: ' + post['from']['name'] + '. ID: ' + post['from']['id'])
                    except:
                        pass
                    try:
                        print ('Description: ' + post['description'])
                    except:
                        post['description'] = ''
                        pass
                    try:
                        print ('Message: ' + post['message'])
                    except:
                        post['message'] = ''
                        pass
                    try:
                        print ('Picture link:  ' + post['picture'])
                    except:
                        post['picture'] = ''
                        pass
                    try:
                        print ('Link:  ' + post['link'])
                    except:
                        post['link'] = ''
                        pass
                    try:
                        print ('Source: :  ' + post['source'])
                    except:
                        post['source'] = ''
                        pass
                    try:
                        print ('Post id:  ' + post['id'])
                    except:
                        post['id'] = ''
                        pass
                    try:
                        print ('Story: ' + post['story'])
                    except:
                        post['story'] = ''
                        pass

                    count_posts += 1
                    add_new_posts(user_id,user_name,group_id,group_name,post)
                # Loading to other page
                data = requests.get(data['paging']['next']).json()
                # ---------------------
            except KeyError:
                print "Key Error"

    def start_scraping(self):
        con = db.connect(database="../db")
        cur = con.cursor()
        users = cur.execute("SELECT * FROM users;").fetchall()

        for i in cur.execute("SELECT * FROM groups WHERE scrup=1;"):
            token = ''
            for u in users:
                if i[2] == u[2]:
                    token = self.get_token(u[5], u[6])
                    break
            t = threading.Thread(target=self.getAllPostsFromGroup, args=(token, i[1],))
            t.start()

    def get_token(self, login, password):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument("start-maximized")
        self.chrome = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=chrome_options)
        # self.chrome = webdriver.Chrome(executable_path='../chromedriver'.format(os.getcwd()),
        #                                chrome_options=chrome_options)
        self.chrome.get(
            'https://www.facebook.com/login/?next=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2F145634995501895%2F')
        self.chrome.find_element_by_id('email').send_keys(login)
        self.chrome.find_element_by_id('pass').send_keys(password)
        self.chrome.find_element_by_id('pass').submit()
        self.chrome.get(
            'https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me%3F&version=v2.3')
        token = self.chrome.find_element_by_xpath('//div/div[2]/div/div[1]/label/input').get_attribute('value')
        self.chrome.close()
        return token
