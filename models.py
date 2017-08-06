
# Module implementing classes for saving user data on Datastore

# If you want to persist any data, you must save it in classes that extend ndb.Model (ndb=New Database)
# NDB is a NOSQL database based on kind, entity, property, which are equivalent to class, instance, field in OOP
# and Table, Row, Column in SQL

# Imports

from google.appengine.ext import ndb
from pybcrypt import bcrypt
from datetime import datetime
import endpoints

# User Collection class
# This is used when storing user keys directly in an instance might result in a very 
# large list for a given entity (e.g. a chat's followers might be in the millions). 
# This way we can delay querying until absolutely necessary. 

class UserCollection(ndb.Model):
	user_keys=ndb.KeyProperty(kind='UserProfile', repeated=True)
	user_count=ndb.ComputedProperty(lambda self: self.user_keys.count())

# User Profile class 

class UserProfile(ndb.Model):
	username = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	displayname = ndb.StringProperty()
	blurb = ndb.StringProperty()
	avatar = ndb.BlobProperty()
	chatsmember = ndb.KeyProperty(kind='GroupChat', repeated=True)
	chatsfollower = ndb.KeyProperty(kind='GroupChat', repeated=True)
	credential =  ndb.KeyProperty(kind='Credential')


# Credential object contains hashed user password, user API token, salt

class Credential(ndb.Model):
	hashed_password = ndb.StringProperty(indexed=False)
	salt = ndb.StringProperty(indexed=False)
	token = ndb.StringProperty(indexed=False)

	def hash_password(self, inputstr):
		s = bcrypt.gensalt()
		h = bcrypt.hashpw(inputstr, s)
		self.hashed_password = h
		self.salt = s

	def set_token(self):
		self.token = bcrypt.gensalt()

	def verify_password(self, inputstr):
		if not inputstr:
			return False
		if not bcrypt.hashpw(inputstr, self.salt) == self.hashed_password:
			return False
		else: 
			return True

	def verify_token(self, inputstr):
		if not inputstr:
			return False
		if not inputstr == self.token:
			return False
		else:
			return True


# Single Message class

class ChatMessage(ndb.Model):
	username = ndb.KeyProperty(kind='UserProfile', required=True)
	chatname = ndb.KeyProperty(kind='GroupChat', required=True)
	messagetext = ndb.StringProperty()
	messagemedia = ndb.BlobProperty()
	messagetime = ndb.DateTimeProperty()
	votes = ndb.KeyProperty(kind='UserCollection')

# Chat class 

''' Note that a GroupChat object is simply a container for its members, followers, and individual messages
    all of which are datastore types'''

class GroupChat(ndb.Model):
	name = ndb.StringProperty(required=True)
	members = ndb.KeyProperty(kind='UserProfile', repeated=True)
	followers = ndb.KeyProperty(kind='UserCollection')
	messagelist = ndb.KeyProperty(kind = 'ChatMessage', repeated=True)
	avatar = ndb.BlobProperty()

