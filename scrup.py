import threading

import facebook
import requests
import sqlite3 as db

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
        # Get ID from group Url
        get_group_name = group_url.rstrip('/ ').split('/')[-1]
        if self._is_number(get_group_name):
            group_id = get_group_name
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
                        pass
                    try:
                        print ('Message: ' + post['message'])
                    except:
                        pass
                    try:
                        print ('Picture link:  ' + post['picture'])
                    except:
                        pass
                    try:
                        print ('Link:  ' + post['link'])
                    except:
                        pass
                    try:
                        print ('Source: :  ' + post['source'])
                    except:
                        pass
                    count_posts += 1
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
