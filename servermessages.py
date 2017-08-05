
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
	password = messages.StringField(2, required=True)

# Message form corresponding to profile creation and update

class ProfileForm(messages.Message):
	username = messages.StringField(1, required=True)
	email = messages.StringField(2)
	displayname = messages.StringField(3)
	blurb = messages.StringField(4)
	avatar = messages.BytesField(5)
	chatsmember = messages.StringField(8, repeated=True)
	chatsfollower = messages.StringField(9, repeated=True)


# Message form corresponding to an individual chat message

class ChatMessageForm(messages.Message):
	sender = messages.StringField(1, required=True)
	chatname = messages.StringField(2, required=True)
	messagetext = messages.StringField(3)
	messagemedia = messages.BytesField(4)


# Get the message/comment IDs for a given chat

class MsgRetrieval(messages.Message):
	chatname=messages.StringField(1, required=True)
	msg_ids=messages.IntegerField(2, repeated=True)

# Get a single chat by ID

class ChatIdForm(messages.Message):
	msgid = messages.IntegerField(1, required=True)


# Message form corresponding to chat room creation/update/retrieval

class GroupChatForm(messages.Message):
	name = messages.StringField(1, required=True)
	members = messages.StringField(2, repeated=True)
	followers = messages.StringField(3, repeated=True)
	messagelist = messages.StringField(4, repeated=True)
	avatar = messages.BytesField(5)




