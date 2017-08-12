
# Import model and message form classes; import cloud platform modules

import endpoints
from protorpc import messages
from protorpc import *

from google.appengine.ext import ndb

from models import *
from servermessages import *
from tools import authenticate

import datetime

    
# Define API

@endpoints.api(name='groupchat', version='v1')
class GroupChatApi(remote.Service):

    @endpoints.method(StatusMessage, StatusMessage, path='hello', http_method='POST', name='groupchat.test')
    def hello(self, request):
        return StatusMessage(successful=True, comments="works")

    # Login. A successful login returns a token from the server. 

    @endpoints.method(LoginForm, LoginForm, path='login', http_method='POST', name='groupchat.login')
    def login(self, request):
        authenticate.user_exists(request.username)
        userkey=ndb.Key(UserProfile, request.username)
        user=userkey.get()
        usercred=user.credential.get()
        if usercred.verify_password(request.password):
            output=LoginForm(username=request.username, token=usercred.token)
            return output
        else:
            raise endpoints.UnauthorizedException("Incorrect password.")

    # Create a profile

    @endpoints.method(ProfileForm, LoginForm, path='createprofile', http_method='POST', name='profile.create')
    def create_profile(self, request):
        authenticate.username_taken(request.username)
        authenticate.valid_password(request.password)
    	new_prof=UserProfile(id=request.username, username=request.username)
        cred = Credential()
        cred.hash_password(request.password)
        cred.set_token()
        cred.put()
        new_prof.credential=cred.key
    	if new_prof.put():
    		return LoginForm(username=request.username, token=cred.token)
    	else: 
    		raise endpoints.BadRequestException("Google Datastore save error.")


    # Update a profile

    @endpoints.method(ProfileForm, StatusMessage, path='update', http_method='POST', name='profile.update')
    def update_profile(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        currentprof = ndb.Key(UserProfile, request.username).get()
    	for field in ('email','displayname','blurb','avatar'):
    		if hasattr(request, field):
    			val=getattr(request,field)
    			setattr(currentprof, field, val)
    	if currentprof.put():
    		return StatusMessage(successful=True)
    	else: 
    		raise endpoints.BadRequestException("Google Datastore save error.")

    # Return profile

    @endpoints.method(ProfileForm, ProfileForm, path='return', http_method='GET', name='profile.return')
    def return_profile(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        prof_key=ndb.Key(UserProfile, request.soughtprofile)
        prof = prof_key.get()
    	profile = ProfileForm(username=request.soughtprofile)
    	for field in ('email','displayname','blurb','avatar','friends','chatsmember','chatsfollowing'):
    		if hasattr(prof, field):
    			val=getattr(prof, field)
    			setattr(profile, field, val)
    	return profile


    # Create a group chat

    @endpoints.method(GroupChatForm, StatusMessage, path='createchat', http_method='POST', name='groupchat.create')
    def create_chat(self, request):  
        authenticate.authenticate_login(username=request.username, token=request.token)
        authenticate.chat_taken(request.name)
        member_keys=[]
        member_test=[]
        for x in range(0, len(request.members)):
            k = ndb.Key(UserProfile, request.members[x])
            member_keys.append(k)
            future=k.get()
            if not future:
                raise endpoints.BadRequestException("User does not exist.")
        new_chat = GroupChat(name=request.name, members=member_keys, avatar=request.avatar)
        new_chat.key=ndb.Key(GroupChat, request.name)
        if new_chat.put():
            return StatusMessage(successful = True, comments='Chat created.')
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")


    # Get the messages ids for a given chat

    @endpoints.method(MsgRetrieval, MsgRetrieval, path='return_msg_ids', http_method='GET', name='groupchat.return_msg_ids')
    def get_msg_ids(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        chat = ndb.Key(GroupChat, request.chatname).get()
        ids = []
        for count in range(0, len(chat.messagelist)):
            ids.append(chat.messagelist[count].id())
        response = MsgRetrieval(chatname=request.chatname, msg_ids=ids, username=request.username)
        return response


    # Post a message

    @endpoints.method(ChatMessageForm, StatusMessage, path='postchat',http_method='POST', name='chatmessage.post')
    def post_message(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        authenticate.chat_exists(request.chatname)
        chat_key = ndb.Key(GroupChat, request.chatname)
        chat = chat_key.get()
        msg = ChatMessage(username=ndb.Key(UserProfile, request.username), chatname=chat_key, messagetext=request.messagetext, messagemedia=request.messagemedia, messagetime=datetime.datetime.now())
        if msg.put():
            msg_key = msg.key
            chat.messagelist.append(msg_key)
            if chat.put():
                return StatusMessage(successful = True, comments = "Message posted")
            else:
                raise endpoints.BadRequestException("Google Datastore save error.") 
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")


    # Get a message

    @endpoints.method(ChatIdForm, ChatMessageForm, path='returnmsg', http_method='GET', name='message.return')
    def get_msg(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        msg_key=ndb.Key(ChatMessage, request.msgid)
        msg = msg_key.get()
        msg_form=ChatMessageForm(username=msg.username.id(), chatname=msg.chatname.id(), messagetext=msg.messagetext, messagemedia=msg.messagemedia)
        return msg_form


    # Delete a message

    @endpoints.method(ChatIdForm, StatusMessage, path='deletechat', http_method='POST', name='chatmessage.delete')
    def delete_msg(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        msg_key = ndb.Key(ChatMessage, request.msgid)
        msg = msg_key.get()
        parent_chat=msg.chatname.get()
        parent_chat.messagelist.remove(msg_key)
        msg_key.delete()
        if parent_chat.put():
            return StatusMessage(successful=True)
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")



# Create API Server

api = endpoints.api_server([GroupChatApi])


