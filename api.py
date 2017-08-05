
# Import model and message form classes; import cloud platform modules

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb

from models import *
from servermessages import *

import datetime

    
# Define API

@endpoints.api(name='groupchat', version='v1')
class GroupChatApi(remote.Service):



    # Create a group chat

    @endpoints.method(GroupChatForm, StatusMessage, path='createchat', http_method='POST', name='groupchat.create')
    def create_chat(self, request):  
        nametaken_key = ndb.Key(GroupChat, request.name)    # Test whether chat already exists
        if nametaken_key.get(): 
            return StatusMessage(successful = False, comments = 'Chat already exists')
        member_keys=[]
        member_test=[]
        for x in range(0, len(request.members)):
            k = ndb.Key(UserProfile, request.members[x])
            member_keys.append(k)
            future=k.get()
            if not future:
                return StatusMessage(successful = False, comments = 'Member does not exist')
 
        new_chat = GroupChat(name=request.name, members=member_keys, avatar=request.avatar)
        new_chat.key=ndb.Key(GroupChat, request.name)
        if new_chat.put():
            return StatusMessage(successful = True)
        else:
            return StatusMessage(successful = False)


    # Get the messages ids for a given chat

    @endpoints.method(MsgRetrieval, MsgRetrieval, path='return_msg_ids', http_method='GET', name='groupchat.return_msg_ids')
    def get_msg_ids(self, request):
        chat = ndb.Key(GroupChat, request.chatname).get()
        ids = []
        for count in range(0, len(chat.messagelist)):
            ids.append(chat.messagelist[count].id())
        response = MsgRetrieval(chatname=request.chatname, msg_ids=ids)
        return response


	# Post a message

    @endpoints.method(ChatMessageForm, StatusMessage, path='postchat',http_method='POST', name='chatmessage.post')
    def post_message(self, request):
        chat_key = ndb.Key(GroupChat, request.chatname)
        chat = chat_key.get()
        if not chat:
            return StatusMessage(successful = False, comments = 'Chat does not exist')
    	msg = ChatMessage(sender=ndb.Key(UserProfile, request.sender), chatname=chat_key, messagetext=request.messagetext, messagemedia=request.messagemedia, messagetime=datetime.datetime.now())
    	if msg.put():
            msg_key = msg.key
            chat.messagelist.append(msg_key)
            if chat.put():
    		    return StatusMessage(successful = True)
            else:
                return StatusMessage(successful = False)  
    	else:
    		return StatusMessage(successful = False)


    # Get a message

    @endpoints.method(ChatIdForm, ChatMessageForm, path='returnmsg', http_method='GET', name='message.return')
    def get_msg(self, request):
        msg_key=ndb.Key(ChatMessage, request.msgid)
        msg = msg_key.get()
        msg_form=ChatMessageForm(sender=msg.sender.id(), chatname=msg.chatname.id(), messagetext=msg.messagetext, messagemedia=msg.messagemedia)
        return msg_form


    # Delete a message

    @endpoints.method(ChatIdForm, StatusMessage, path='deletechat', http_method='POST', name='chatmessage.delete')
    def delete_msg(self, request):
        msg_key = ndb.Key(ChatMessage, request.msgid)
        msg = msg_key.get()
        parent_chat=msg.chatname.get()
        parent_chat.messagelist.remove(msg_key)
        msg_key.delete()
        if parent_chat.put():
            return StatusMessage(successful=True)
        else:
            return StatusMessage(successful=False)



    # Create a profile

    @endpoints.method(ProfileForm, StatusMessage, path='createprofile', http_method='POST', name='profile.create')
    def create_profile(self, request):
    	test = ndb.Key(UserProfile, request.username)
    	if test.get():
            return StatusMessage(successful=False, comments='Profile already exists')
    	new_prof=UserProfile(id=request.username, username=request.username)
    	for field in ('email','displayname','blurb','avatar'):
    		if hasattr(request, field):
    			val=getattr(request,field)
    			setattr(new_prof, field, val)

    	if new_prof.put():
    		return StatusMessage(successful=True)
    	else: 
    		return StatusMessage(successful=False, comments='Google Datastore save error')


    # Update a profile

    @endpoints.method(ProfileForm, StatusMessage, path='update', http_method='POST', name='profile.update')
    def update_profile(self, request):
    	test = ndb.Key(UserProfile, request.username)
    	currentprof = test.get()
    	if not currentprof:
    		return StatusMessage(successful=False, comments='Profile nonexistent')
    	else:
    		for field in ('email','displayname','blurb','avatar'):
    			if hasattr(request, field):
    				val=getattr(request,field)
    				setattr(currentprof, field, val)
    		if currentprof.put():
    			return StatusMessage(successful=True)
    		else: 
    			return StatusMessage(successful=False, comments='Google Datastore save error')

    # Return profile

    @endpoints.method(ProfileForm, ProfileForm, path='return', http_method='GET', name='profile.return')
    def return_profile(self, request):
    	p_key = ndb.Key(UserProfile, request.username)
    	prof = p_key.get()
    	profile = ProfileForm(username=request.username)
    	for field in ('email','displayname','blurb','avatar','friends','chatsmember','chatsfollowing'):
    		if hasattr(prof, field):
    			val=getattr(prof, field)
    			setattr(profile, field, val)
    	return profile


# Create API Server

api = endpoints.api_server([GroupChatApi])


