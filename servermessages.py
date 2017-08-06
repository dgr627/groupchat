
# Module implenting HTTP message classes to send requests to and receive responses from the backend
# These classes must extend messages.Message. Note that they have only simple field classes so we have to work with that.

# Import protorpc messages

from protorpc import messages

# Generic Boolean Status Message

class StatusMessage(messages.Message):
	successful = messages.BooleanField(1, required=True)
	comments = messages.StringField(2)

# Login form

class LoginForm(messages.Message):
	username = messages.StringField(1, required=True)
	password = messages.StringField(2)
	token = messages.StringField(3)
	notes = messages.StringField(4) # Technical notes regarding the HTTP request

# Message form corresponding to profile creation and update

class ProfileForm(messages.Message):
	username = messages.StringField(1, required=True)
	email = messages.StringField(2)
	displayname = messages.StringField(3)
	blurb = messages.StringField(4)
	avatar = messages.BytesField(5)
	chatsmember = messages.StringField(8, repeated=True)
	chatsfollower = messages.StringField(9, repeated=True)
	password = messages.StringField(10)
	token = messages.StringField(11)
	notes = messages.StringField(12)
	soughtprofile = messages.StringField(13)


# Message form corresponding to an individual chat message

class ChatMessageForm(messages.Message):
	token = messages.StringField(1)
	username= messages.StringField(2, required=True)
	chatname = messages.StringField(3, required=True)
	messagetext = messages.StringField(4)
	messagemedia = messages.BytesField(5)
	notes = messages.StringField(6) 


# Get the message/comment IDs for a given chat

class MsgRetrieval(messages.Message):
	token = messages.StringField(1)
	username = messages.StringField(2, required=True)
	chatname=messages.StringField(3, required=True)
	msg_ids=messages.IntegerField(4, repeated=True)
	notes = messages.StringField(5)

# Get a single chat by ID

class ChatIdForm(messages.Message):
	token = messages.StringField(1)
	username = messages.StringField(2, required=True)
	msgid = messages.IntegerField(3, required=True)
	notes = messages.StringField(4)


# Message form corresponding to chat room creation/update/retrieval

class GroupChatForm(messages.Message):
	token = messages.StringField(1, required=True)
	username = messages.StringField(2, required=True)
	name = messages.StringField(3, required=True)
	members = messages.StringField(4, repeated=True)
	followers = messages.StringField(5, repeated=True)
	messagelist = messages.StringField(6, repeated=True)
	avatar = messages.BytesField(7)




