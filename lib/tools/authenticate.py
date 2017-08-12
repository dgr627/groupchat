
import endpoints
from google.appengine.ext import ndb
from models import *

def authenticate_login(username, token):
	user_key=ndb.Key(UserProfile, username)
	cred = user_key.get().credential.get()
	if not token == cred.token:
		raise endpoints.UnauthorizedException("Not logged in.")

def username_taken(username):
	user_key=ndb.Key(UserProfile, username)
	if user_key.get():
		raise endpoints.BadRequestException("Username already taken.")

def valid_password(password):
	if not password:
		raise endpoints.BadRequestException("Please enter a password.")
	if not len(password)>5:
		raise endpoints.BadRequestException("Password length needs to be at least 6 characters.")

def user_exists(username):
	user_key=ndb.Key(UserProfile, username)
	if not user_key.get():
		raise endpoints.BadRequestException("User does not exist.")

def chat_taken(chatname):
	chat_key=ndb.Key(GroupChat, chatname)
	if chat_key.get():
		raise endpoints.BadRequestException("Chat name already in use.")

def chat_exists(chatname):
	chat_key=ndb.Key(GroupChat, chatname)
	if not chat_key.get():
		raise endpoints.BadRequestException("Chat does not exist.")