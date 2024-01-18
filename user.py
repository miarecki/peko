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

	def get_whiteboards(self):
		return db.get_whiteboards(self.user_id)

	def get_reminders(self):
		return db.get_reminders(self.user_id)

	def get_recordings(self):
		return db.get_recordings(self.user_id)

	def get_all_notes(self):
		return db.get_all_notes(self.user_id)

	def get_all_favorites(self):
		return db.get_all_favorites(self.user_id)

	def get_all_tag(self, tag_name):
		return db.get_all_tag(self.user_id, tag_name)


