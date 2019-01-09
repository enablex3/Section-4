from user import User

# Authenticate user
def authenticate(username, password):
	user = User.find_by_username(username)
	if user and user.password == password:
		return(user)

def identity(payload):
	user_id = User.find_by_id(payload['identity'])
	return(user_id)
