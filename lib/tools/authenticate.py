import endpoints
from google.appengine.ext import ndb
from models import *


def authenticate_login(userid, token):
    user_key = ndb.Key(UserProfile, userid)
    user = user_key.get()
    cred = user.credential.get()
    if not token == cred.token:
        raise endpoints.UnauthorizedException("Not logged in.")
    return user

def authenticate(username, password):
    q = UserProfile.query(UserProfile.username == username)
    for user in q.iter():
        cred = user.credential.get()
        if cred.verify_password(password):
            return user
        else:
            raise endpoints.UnauthorizedException("Incorrect password.")
    raise endpoints.UnauthorizedException("User not found.")

def authenticate_chat(chatname, userid):
    chat_key = ndb.Key(GroupChat, chatname)
    chat = chat_key.get()

    if not chat:
        raise endpoints.BadRequestException("Chat does not exist.")
    return chat

def validate_username(username):
    count = UserProfile.query(UserProfile.username == username).count()
    if count > 0:
        raise endpoints.BadRequestException("Username already taken.")


def validate_password(password):
    if not password:
        raise endpoints.BadRequestException("Please enter a password.")
    if not len(password) > 5:
        raise endpoints.BadRequestException("Password length needs to be at least 6 characters.")


def user_exists(username):
    count = UserProfile.query(UserProfile.username == username).count()
    if count == 0:
        raise endpoints.BadRequestException("User does not exist.")
    return True


def chat_taken(chatname):
    chat_key = ndb.Key(GroupChat, chatname)
    if chat_key.get():
        raise endpoints.BadRequestException("Chat name already in use.")


def chat_exists(chatname):
    chat_key = ndb.Key(GroupChat, chatname)
    if not chat_key.get():
        raise endpoints.BadRequestException("Chat does not exist.")

