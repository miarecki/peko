import peko_database as db

class User:
	def __init__(self, user_id):
		self.user_id = user_id

	def get_user_id(self):
		return self.user_id

	def get_username(self):
		return db.get_username(self.user_id)

	def get_text_notes(self):
		return db.get_text_notes(self.user_id)

	def get_contacts(self):
		return db.get_contacts(self.user_id)


