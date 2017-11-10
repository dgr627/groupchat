# Import model and message form classes; import cloud platform modules

import endpoints
from protorpc import *
import user_factory

from google.appengine.ext import ndb
from google.appengine.api import images

from models import *
from servermessages import *
from tools import authenticate

import datetime


# Define API
@endpoints.api(name='groupchat', version='v1')
class GroupChatApi(remote.Service):
    @endpoints.method(
        StatusMessage,
        StatusMessage,
        path='hello',
        http_method='POST',
        name='groupchat.test'
    )
    def hello(self):
        return StatusMessage(successful=True, comments="works")

    # Login. A successful login returns a token from the server.
    @endpoints.method(
        LoginForm,
        LoginForm,
        path='login',
        http_method='POST',
        name='groupchat.login'
    )
    def login(self, request):
        user = authenticate.authenticate(request.username, request.password)
        return user.to_private_output()

    # Create a profile
    @endpoints.method(
        LoginForm,
        LoginForm,
        path='createprofile',
        http_method='POST',
        name='profile.create'
    )
    def create_profile(self, request):
        username = request.username
        password = request.password

        authenticate.validate_username(username)
        authenticate.validate_password(password)

        user = user_factory.create_new_user(username, password)
        return user.to_private_output()

    # Update a profile
    @endpoints.method(
        ProfileForm,
        ProfileForm,
        path='update',
        http_method='POST',
        name='profile.update'
    )
    def update_profile(self, request):
        user = authenticate.authenticate_login(request.userid, request.token)
        for field in ('email', 'displayname', 'blurb'):
            val = getattr(request, field)
            if val:
                setattr(user, field, val)

        if request.avatar:
            avatar = images.resize(request.avatar, 32, 32)
            user.avatar = avatar

        if user.put():
            return user.to_public_output()
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")

    # Return profile
    @endpoints.method(
        ProfileForm,
        ProfileForm,
        path='return',
        http_method='GET',
        name='profile.return'
    )
    def return_profile(self, request):
        user = authenticate.authenticate_login(request.userid, request.token)
        return user.to_public_output()

    # Create a group chat
    @endpoints.method(
        GroupChatForm,
        GroupChatInfoForm,
        path='createchat',
        http_method='POST',
        name='groupchat.create'
    )
    def create_chat(self, request):
        user = authenticate.authenticate_login(request.userid, request.token)
        authenticate.chat_taken(request.name)
        member_keys = [user.userid]

        for x in range(0, len(request.members)):
            future = ndb.Key(UserProfile, x).get()
            if not future:
                raise endpoints.BadRequestException("User does not exist.")
            else:
                member_keys.append(x)

        new_chat = GroupChat(name=request.name, members=member_keys, avatar=request.avatar)
        new_chat.key = ndb.Key(GroupChat, request.name)
        if new_chat.put():
            return new_chat.to_private_output()
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")

    # Get the messages ids for a given chat
    @endpoints.method(
        MsgRetrieval,
        MsgRetrieval,
        path='return_msg_ids',
        http_method='GET',
        name='groupchat.return_msg_ids'
    )
    def get_msg_ids(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        chat = ndb.Key(GroupChat, request.chatname).get()
        ids = []
        for count in range(0, len(chat.messagelist)):
            ids.append(chat.messagelist[count].id())
        response = MsgRetrieval(chatname=request.chatname, msg_ids=ids, username=request.username)
        return response

    # Get the messages for a given chat
    @endpoints.method(
        MsgRetrieval,
        MsgRetrieval,
        path='return_msgs',
        http_method='POST',
        name='groupchat.return_msgs'
    )
    def return_msgs(self, request):
        user = authenticate.authenticate_login(request.userid, request.token)
        chat = authenticate.authenticate_chat(request.chatname, user.userid)
        msgs = []
        for count in range(0, len(chat.messagelist)):
            msg_key = chat.messagelist[count]
            print('CHAT', msg_key)
            msg = msg_key.get()
            if not msg.votes:
                likes = 0
            else:
                likes = msg.votes.get().user_count
            msgform = ChatMessageForm(
                userid=msg.userid,
                chatname=msg.chatname,
                messagetext=msg.messagetext,
                messagemedia=msg.messagemedia,
                messagetime=msg.messagetime,
                messageid=msg_key.id(), votes=likes
            )
            msgs.append(msgform)
        response = MsgRetrieval(chatname=request.chatname, username=request.username, messages=msgs)
        return response

    # def return_chat_info(self, request):
    #   authenticate.authenticate_login(username=request.username, token=request.token)
    #   chat = ndb.Key(GroupChat, request.chatname).get()

    # Post a message
    @endpoints.method(
        ChatMessageForm,
        ChatMessageForm,
        path='postchat',
        http_method='POST',
        name='chatmessage.post'
    )
    def post_message(self, request):
        user = authenticate.authenticate_login(request.userid, request.token)
        chat = authenticate.authenticate_chat(request.chatname, user.userid)

        msg = ChatMessage(
            userid=user.userid,
            chatname=chat.name,
            messagetext=request.messagetext,
            messagemedia=request.messagemedia,
            messagetime=datetime.datetime.now())

        if msg.put():
            msg_key = msg.key
            chat.messagelist.append(msg_key)
            if chat.put():
                return msg.to_public_output()
            else:
                raise endpoints.BadRequestException("Google Datastore save error.")
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")

    # Get a message
    @endpoints.method(
        ChatIdForm,
        ChatMessageForm,
        path='returnmsg',
        http_method='GET',
        name='message.return'
    )
    def get_msg(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        msg_key = ndb.Key(ChatMessage, request.msgid)
        msg = msg_key.get()
        msg_form = ChatMessageForm(
            username=msg.username.id(),
            chatname=msg.chatname.id(),
            messagetext=msg.messagetext,
            messagemedia=msg.messagemedia)
        return msg_form

    # Delete a message
    @endpoints.method(
        ChatIdForm,
        StatusMessage,
        path='deletechat',
        http_method='POST',
        name='chatmessage.delete'
    )
    def delete_msg(self, request):
        authenticate.authenticate_login(username=request.username, token=request.token)
        msg_key = ndb.Key(ChatMessage, request.msgid)
        msg = msg_key.get()
        parent_chat = msg.chatname.get()
        parent_chat.messagelist.remove(msg_key)
        msg_key.delete()
        if parent_chat.put():
            return StatusMessage(successful=True)
        else:
            raise endpoints.BadRequestException("Google Datastore save error.")


# Create API Server

api = endpoints.api_server([GroupChatApi])
