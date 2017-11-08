# Python scripts to test out the API
# You need to pip install requests for this to work

import ast
import requests

username = 'deepak18'
password = 'deepak'
chatname = 'testtest2'
messagetext = 'dogs'


def create_profile(username, password):
    payload = {'username': '%s' % username, 'password': '%s' % password}
    r = requests.post('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/createprofile', params=payload)
    x = r.json()
    print x["token"]
    token = x["token"]
    return token


z = create_profile(username, password)


def create_groupchat(username, token, chatname):
    payload = {'username': '%s' % username, 'token': '%s' % token, 'name': '%s' % chatname}
    r = requests.post('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/createchat', params=payload)
    x = r.json()
    print x["successful"]


create_groupchat(username, z, chatname)


def post_message(username, token, chatname, messagetext):
    payload = {'username': '%s' % username, 'token': '%s' % token, 'chatname': '%s' % chatname,
               'messagetext': '%s' % messagetext}
    r = requests.post('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/postchat', params=payload)
    x = r.json()
    print x["successful"]


post_message(username, z, chatname, messagetext)


def display_messages(username, token, chatname):
    payload3 = {'username': '%s' % username, 'token': '%s' % token, 'chatname': '%s' % chatname}
    r = requests.get('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/return_msgs', params=payload3)
    x = r.json()
    print x


display_messages(username, z, chatname)
