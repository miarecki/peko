from argon2 import PasswordHasher
import peko_database
import re

def acc_name_check(acc_name):
	return len(acc_name) <= 16 and bool(re.compile(r'^[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ_]+$').match(acc_name))


def create_new_account(acc_name, password1, password2):

	message = ''

	if len(acc_name) > 16:
		message = 'Username is too long (max. 16 characters).'
		return message

	if not bool(re.compile(r'^[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ_]+$').match(acc_name)):
		message = 'Username contains an invalid character.'
		return message

	if peko_database.db_check_if_account_exist(acc_name):
		message = 'Username is taken.'
		return message

	if len(password1) < 8:
		message = 'Password must be at least 8 characters long.'
		return message

	if password1 != password2:
		message = 'Passwords do not match.'
		return message

	ph = PasswordHasher()
	hashed_password = ph.hash(password1)

	peko_database.db_add_user(acc_name, hashed_password, enc_key = 'test')
	message = 'Success!'
	return message

def log_in(acc_name, password):

	message = ''
	ph = PasswordHasher()

	if not peko_database.db_check_if_account_exist(acc_name):
		message = 'Account does not exist.'
		return message

	try:
		hashed_pass = peko_database.db_grab_hash(acc_name)
		if ph.verify(hashed_pass, password):
			message = 'Success!'
			return message
	except Exception:
			message = 'Password is not correct.'
			return message







