# Python scripts to test out the API
# You need to pip install requests for this to work

import ast
import requests
#payload={'username':'bananas244', 'token':'$2a$01$rXhizzYGa377KftoGWC7q.','blurb':'testblurb'}
#r = requests.post('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/update', params=payload)
#x=r.json()
#print x["successful"]

#for i in range(1,20):
#	payload2={'username':'bananas244', 'token':'$2a$01$rXhizzYGa377KftoGWC7q.','chatname':'testchat', 'messagetext':'%s' %i}
#	r=requests.post('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/postchat', params=payload2)
#	x=r.json()
#	print x["successful"]


payload3={'username':'bananas244', 'token':'$2a$01$rXhizzYGa377KftoGWC7q.','chatname':'testchat'}
r = requests.get('https://groupchatdev1.appspot.com/_ah/api/groupchat/v1/return_msgs', params=payload3)
x=r.json()
print x
	
