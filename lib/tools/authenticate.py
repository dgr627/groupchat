
import endpoints
from google.appengine.ext import ndb
from models import UserProfile

def authenticate_login(username, token):
	user_key=ndb.Key(UserProfile, username)
	cred = user_key.get().credential.get()
	if not token == cred.token:
		raise endpoints.UnauthorizedException("Not logged in.")