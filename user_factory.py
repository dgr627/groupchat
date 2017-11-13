import uuid
import endpoints
from protorpc import *

from models import *

def create_new_user(username, password):
    try:
        userid = str(uuid.uuid4())
        new_prof = UserProfile(id=userid, username=username, userid=userid)
        cred = Credential()
        cred.hash_password(password)
        cred.put()
        new_prof.credential = cred.key
        new_prof.put()
        return new_prof
    except:
        raise endpoints.BadRequestException("Google Datastore save error.")