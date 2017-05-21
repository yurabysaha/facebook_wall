import threading

import facebook
import requests
import sqlite3 as db

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
        self.graph = facebook.GraphAPI(access_token=token, version='2.3')
        self.my_profile = self.graph.get_object('me')
        user_id = self.my_profile['id']
        user_name = self.my_profile['first_name'] + ' ' + self.my_profile['last_name']
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
            for z in users:
                if i[2] == z[2]:
                    token = z[3]
                    break
            t = threading.Thread(target=self.getAllPostsFromGroup, args=(token, i[1],))
            t.start()
