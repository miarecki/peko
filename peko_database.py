import psycopg2
from argon2 import PasswordHasher
import os
from dotenv import load_dotenv

load_dotenv()

def db_connect():
    db_connect.conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

# =========================================================================================================

def update_history(uid, action_type, item_name, item_type):

	#db_connect()
	c = db_connect.conn.cursor()

	try:
		c.execute('''
			INSERT INTO History (user_id, action_type, item_name, item_type)
			VALUES (%s, %s, %s, %s);
		''', (uid, action_type, item_name, item_type))

	except Exception as e:
		pass

# =========================================================

def db_add_user(acc_name, hashed_password):
	db_connect()

	c = db_connect.conn.cursor() 

	c.execute('''
		INSERT INTO Users (username, password_hash)
		VALUES (%s, %s)
		RETURNING user_id;
		''', (acc_name, hashed_password))

	# Get the ID of the inserted user
	user_id = c.fetchone()[0]
	'''
	try:
		settings_table_setup()
	except psycopg2.Error as e:
		print(f"Error: {e}")
	'''
	c.execute("INSERT INTO Settings (user_id) VALUES (%s);", (user_id,))

	# Close the cursor and connection
	db_connect.conn.commit()
	db_connect.conn.close()

# =========================================================

def db_check_if_account_exist(acc_name):
	db_connect()

	c = db_connect.conn.cursor() 

	try:
		c.execute('''
			SELECT 1 FROM Users WHERE username = %s;''', (acc_name,))

		result = c.fetchone()

		return result is not None

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()


# =========================================================

def db_grab_hash(acc_name):
	db_connect()

	c = db_connect.conn.cursor() 

	try:
		c.execute('''
			SELECT password_hash FROM Users WHERE username = %s;''', (acc_name,))

		result = c.fetchone()

		return result[0]

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()


# ========================================================

def get_text_notes(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Notes
			WHERE user_id = %s AND is_deleted = false
			ORDER BY
	last_edit DESC;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def insert_text_note(uid, title, content, fav, tags):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		# Insert the text note into the Notes table
		c.execute('''
			INSERT INTO Notes (user_id, title, content, favorite)
			VALUES (%s, %s, %s, %s)
			RETURNING note_id;
		''', (uid, title, content, fav))

		# Get the ID of the inserted note
		note_id = c.fetchone()[0]

		# Insert tags into the NotesTags junction table
		for tag in tags:
			c.execute('''
				INSERT INTO NotesTags (id, tag_name)
				VALUES (%s, %s);
			''', (note_id, tag))

		update_history(uid, 'Create', title, 'Text Note')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()


# ========================================================

def get_username(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT username FROM Users
			WHERE user_id = %s;
''', (uid,))

		result = c.fetchone()
		return result[0]

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_uid(name):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT user_id FROM Users
			WHERE username = %s;
''', (name,))

		result = c.fetchone()
		return result[0]

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ======= new contact add

def insert_contact(uid, display_name, first_name, last_name, email, phone, avatar):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		query = '''
			INSERT INTO Contacts (
				user_id,
				contact_display_name,
				contact_first_name,
				contact_last_name,
				contact_email,
				contact_phone,
				contact_avatar
			) VALUES (
				%s, %s, %s, %s, %s, %s, %s
			);
		'''
		c.execute(query, (
			uid,
			display_name if display_name != '' else None,
			first_name if first_name != '' else None,
			last_name if last_name != '' else None,
			email if email != '' else None,
			phone if phone != '' else None,
			avatar if avatar != '' else '/gui/avatar_default.png'
		))

		update_history(uid, 'Create', display_name, 'Contact')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

#===============

def get_contacts(uid):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		c.execute('''SELECT * FROM Contacts
			WHERE user_id = %s
			ORDER BY contact_display_name;

''', (uid,))

		results = c.fetchall()
		return results

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# =======

def get_text_note(uid, nid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Notes
			WHERE note_id = %s AND user_id = %s;
''', (nid, uid))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =================

def get_contact(uid, cid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Contacts
			WHERE contact_id = %s AND user_id = %s;
''', (cid, uid))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =================

def delete_contact(uid, cid):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		query = '''
			DELETE FROM Contacts
			WHERE contact_id = %s AND user_id = %s;
		'''
		c.execute(query, (cid, uid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# =================

def delete_reminder(uid, rid):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		query = '''
			DELETE FROM Reminders
			WHERE reminder_id = %s AND user_id = %s;
		'''
		c.execute(query, (rid, uid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# =================

def insert_whiteboard(uid, title, content, fav, tags):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		c.execute('''
			INSERT INTO WhiteboardNotes(user_id, title, content, favorite)
			VALUES (%s, %s, %s, %s)
			RETURNING whiteboard_note_id;
		''', (uid, title, content, fav))

		# Get the ID of the inserted note
		whiteboard_id = c.fetchone()[0]

		for tag in tags:
			c.execute('''
				INSERT INTO WhiteboardsTags (id, tag_name)
				VALUES (%s, %s);
			''', (whiteboard_id, tag))

		update_history(uid, 'Create', title, 'Whiteboard')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# =========================

def get_whiteboards(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM WhiteboardNotes
			WHERE user_id = %s AND is_deleted = false
			ORDER BY
	last_edit DESC;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =========================

def get_whiteboard(uid, wid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM WhiteboardNotes
			WHERE whiteboard_note_id = %s AND user_id = %s;
''', (wid, uid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ================================

def insert_reminder(uid, title, desc, rem_date):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		c.execute('''
			INSERT INTO Reminders(user_id, title, description, remind_date)
			VALUES (%s, %s, %s, %s);
		''', (uid, title, desc, rem_date))

		update_history(uid, 'Create', title, 'Reminder')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ================================

def get_reminders(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Reminders
			WHERE user_id = %s
			ORDER BY remind_date DESC;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ================================

def get_reminder(uid, rid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Reminders
			WHERE reminder_id = %s AND user_id = %s;
''', (rid, uid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =================

def insert_recording(uid, title, content, dur, fav, tags):
	db_connect()
	c = db_connect.conn.cursor()

	try:
		c.execute('''
			INSERT INTO Recordings(user_id, title, content, duration, favorite)
			VALUES (%s, %s, %s, %s, %s)
			RETURNING recording_id;
		''', (uid, title, content, dur, fav))

		# Get the ID of the inserted note
		recording_id = c.fetchone()[0]

		for tag in tags:
			c.execute('''
				INSERT INTO RecordingsTags (id, tag_name)
				VALUES (%s, %s);
			''', (recording_id, tag))

		update_history(uid, 'Create', title, 'Recording')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ================================

def get_recordings(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Recordings
			WHERE user_id = %s AND is_deleted = false
			ORDER BY
	last_edit DESC;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ================================

def get_recording(uid, rid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Recordings
			WHERE recording_id = %s AND user_id = %s;
''', (rid, uid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ================================

def get_all_notes(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute("""
			SELECT
	'Notes' AS note_type,
	note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	Notes
WHERE
	user_id = %s AND is_deleted = false

UNION ALL

SELECT
	'WhiteboardNotes' AS note_type,
	whiteboard_note_id AS note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	WhiteboardNotes
WHERE
	user_id = %s AND is_deleted = false

UNION ALL

SELECT
	'Recordings' AS note_type,
	recording_id AS note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	Recordings
WHERE
	user_id = %s AND is_deleted = false

ORDER BY
	creation_date DESC;
		""", (uid, uid, uid))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =======================================		

def get_all_favorites(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute("""
			SELECT
	'Notes' AS note_type,
	note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	Notes
WHERE
	user_id = %s AND is_deleted = false AND favorite = true

UNION ALL

SELECT
	'WhiteboardNotes' AS note_type,
	whiteboard_note_id AS note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	WhiteboardNotes
WHERE
	user_id = %s AND is_deleted = false AND favorite = true

UNION ALL

SELECT
	'Recordings' AS note_type,
	recording_id AS note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	Recordings
WHERE
	user_id = %s AND is_deleted = false AND favorite = true

ORDER BY
	creation_date DESC;
		""", (uid, uid, uid))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ====================================

def get_all_tag(uid, tag_name):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute("""
			SELECT
	'Notes' AS note_type,
	n.note_id,
	n.user_id,
	n.title,
	n.content,
	n.creation_date,
	n.last_edit,
	n.favorite,
	n.is_deleted
FROM
	Notes n
JOIN
	NotesTags nt ON n.note_id = nt.id
JOIN
	Tags t ON nt.tag_name = t.tag_name
WHERE
	t.tag_name = %s AND n.is_deleted = false AND n.user_id = %s

UNION ALL

SELECT
	'WhiteboardNotes' AS note_type,
	wn.whiteboard_note_id AS note_id,
	wn.user_id,
	wn.title,
	wn.content,
	wn.creation_date,
	wn.last_edit,
	wn.favorite,
	wn.is_deleted
FROM
	WhiteboardNotes wn
JOIN
	WhiteboardsTags wt ON wn.whiteboard_note_id = wt.id
JOIN
	Tags t ON wt.tag_name = t.tag_name
WHERE
	t.tag_name = %s AND wn.is_deleted = false AND wn.user_id = %s

UNION ALL

SELECT
	'Recordings' AS note_type,
	r.recording_id AS note_id,
	r.user_id,
	r.title,
	r.content,
	r.creation_date,
	r.last_edit,
	r.favorite,
	r.is_deleted
FROM
	Recordings r
JOIN
	RecordingsTags rt ON r.recording_id = rt.id
JOIN
	Tags t ON rt.tag_name = t.tag_name
WHERE
	t.tag_name = %s AND r.is_deleted = false AND r.user_id = %s

ORDER BY
	last_edit DESC;

		""", (tag_name, uid, tag_name, uid, tag_name, uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_settings(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Settings
			WHERE user_id = %s;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_settings(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Settings
			WHERE user_id = %s;
''', (uid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def update_avatar(uid, avatar):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Settings
SET avatar = %s
WHERE user_id = %s;
''', (avatar, uid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def update_color_scheme(uid, color):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Settings
SET color_scheme = %s
WHERE user_id = %s;
''', (color, uid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def update_display_name(uid, name):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Settings
SET display_name = %s
WHERE user_id = %s;
''', (name, uid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def note_m2t(uid, nid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Notes
SET is_deleted = true
WHERE user_id = %s AND note_id = %s;
''', (uid, nid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def get_trash(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute("""
			SELECT
	'Notes' AS note_type,
	note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	Notes
WHERE
	user_id = %s AND is_deleted = true

UNION ALL

SELECT
	'WhiteboardNotes' AS note_type,
	whiteboard_note_id AS note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	WhiteboardNotes
WHERE
	user_id = %s AND is_deleted = true

UNION ALL

SELECT
	'Recordings' AS note_type,
	recording_id AS note_id,
	user_id,
	title,
	content,
	creation_date,
	last_edit,
	favorite,
	is_deleted
FROM
	Recordings
WHERE
	user_id = %s AND is_deleted = true
ORDER BY
	last_edit DESC;
		""", (uid, uid, uid))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_text_note_tags(nid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT tag_name FROM NotesTags
			WHERE id = %s;
''', (nid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def restore_text_note(uid, nid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Notes
SET is_deleted = false
WHERE user_id = %s AND note_id = %s;
''', (uid, nid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def delete_text_note(uid, nid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:

		c.execute('''
			DELETE FROM NotesTags
			WHERE id = %s;
		''', (nid,))

		c.execute('''DELETE FROM Notes
WHERE user_id = %s AND note_id = %s
RETURNING title;
''', (uid, nid))

		title = c.fetchone()[0]

		update_history(uid, 'Delete', title, 'Text Note')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def edit_note_submit(uid, nid, new_title, new_content, fav, tags):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''
			UPDATE Notes
			SET title = %s, content = %s, favorite = %s, last_edit = CURRENT_TIMESTAMP
			WHERE user_id = %s and note_id = %s
			RETURNING title;
		''', (new_title, new_content, fav, uid, nid))

		title = c.fetchone()[0]

		update_history(uid, 'Edit',title, 'Text Note')

		c.execute('''
			DELETE FROM NotesTags
			WHERE id = %s;
		''', (nid,))

		for tag in tags:
			c.execute('''
				INSERT INTO NotesTags (id, tag_name)
				VALUES (%s, %s);
			''', (nid, tag))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_whiteboard_tags(wid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT tag_name FROM WhiteboardsTags
			WHERE id = %s;
''', (wid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def edit_whiteboard_submit(uid, wid, new_title, fav, tags):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''
			UPDATE WhiteboardNotes
			SET title = %s, favorite = %s, last_edit = CURRENT_TIMESTAMP
			WHERE user_id = %s and whiteboard_note_id = %s
			RETURNING title;
		''', (new_title, fav, uid, wid))

		title = c.fetchone()[0]

		update_history(uid, 'Edit', title, 'Whiteboard')

		c.execute('''
			DELETE FROM WhiteboardsTags
			WHERE id = %s;
		''', (wid,))

		for tag in tags:
			c.execute('''
				INSERT INTO WhiteboardsTags (id, tag_name)
				VALUES (%s, %s);
			''', (wid, tag))

		

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ==============================================================

def whiteboard_m2t(uid, wid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE WhiteboardNotes
SET is_deleted = true
WHERE user_id = %s AND whiteboard_note_id = %s;
''', (uid, wid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ==============================================================

def restore_whiteboard(uid, wid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE WhiteboardNotes
SET is_deleted = false
WHERE user_id = %s AND whiteboard_note_id = %s;
''', (uid, wid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def delete_whiteboard(uid, wid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:

		c.execute('''
			DELETE FROM WhiteboardsTags
			WHERE id = %s;
		''', (wid,))

		c.execute('''DELETE FROM WhiteboardNotes
WHERE user_id = %s AND whiteboard_note_id = %s
RETURNING title;
''', (uid, wid))

		title = c.fetchone()[0]

		update_history(uid, 'Delete', title, 'Whiteboard')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def get_recording_tags(rid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT tag_name FROM RecordingsTags
			WHERE id = %s;
''', (rid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def edit_recording_submit(uid, rid, new_title, fav, tags):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''
			UPDATE Recordings
			SET title = %s, favorite = %s, last_edit = CURRENT_TIMESTAMP
			WHERE user_id = %s and recording_id = %s
			RETURNING title;
		''', (new_title, fav, uid, rid))

		title = c.fetchone()[0]
		update_history(uid, 'Edit', title, 'Recording')

		c.execute('''
			DELETE FROM RecordingsTags
			WHERE id = %s;
		''', (rid,))

		for tag in tags:
			c.execute('''
				INSERT INTO RecordingsTags (id, tag_name)
				VALUES (%s, %s);
			''', (rid, tag))

		

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ==============================================================

def recording_m2t(uid, rid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Recordings
SET is_deleted = true
WHERE user_id = %s AND recording_id = %s;
''', (uid, rid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def restore_recording(uid, rid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''UPDATE Recordings
SET is_deleted = false
WHERE user_id = %s AND recording_id = %s;
''', (uid, rid))

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def delete_recording(uid, rid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:

		c.execute('''
			DELETE FROM NotesTags
			WHERE id = %s;
		''', (rid,))

		c.execute('''DELETE FROM Recordings
WHERE user_id = %s AND recording_id = %s
RETURNING title;
''', (uid, rid))

		title = c.fetchone()[0]
		update_history(uid, 'Delete', title, 'Whiteboard')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def remove_statistics():
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''DROP VIEW IF EXISTS Statistics;
''')

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

#remove_statistics()
#create_view_statistics()
#db_test_select()

# ===============================================================

def get_stats(uid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Statistics
WHERE user_id = %s;
''', (uid,))

		result = c.fetchone()
		return result

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def get_current_history(uid):
	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT action_date_formatted, action_time, item_type, item_name, action_type
FROM CurrentHistory
WHERE user_id = %s;
''', (uid,))

		results = c.fetchall()
		return results

	finally:
		db_connect.conn.commit()
		db_connect.conn.close()

# ===============================================================

def search_results(uid, title, favorite, types, tags, last_edit_limit):
	db_connect()
	c = db_connect.conn.cursor()

	if types is None:
		return []

	# Base query parts
	queries = []
	params = []

	# Helper function to add conditions to each subquery
def search_results(uid, title, favorite, types, tags, last_edit_limit):
	db_connect()
	c = db_connect.conn.cursor()

	if not types:
		return []

	queries = []
	params = []

	def add_conditions(type_alias, tag_alias, conditions, params):
		if title:
			conditions.append(f"{type_alias}.title ILIKE %s")
			params.append(f"%{title}%")
		if favorite is not None:
			conditions.append(f"{type_alias}.favorite = %s")
			params.append(favorite)
		if tags:
			tag_conditions = " OR ".join([f"{tag_alias}.tag_name = %s" for _ in tags])
			conditions.append(f"({tag_conditions})")
			params.extend(tags)
		if last_edit_limit == 'Yesterday':
			conditions.append(f"{type_alias}.last_edit <= CURRENT_DATE - INTERVAL '1 day'")
		if last_edit_limit == 'Last week':
			conditions.append(f"{type_alias}.last_edit <= CURRENT_DATE - INTERVAL '1 week'")
		if last_edit_limit == 'Last month':
			conditions.append(f"{type_alias}.last_edit <= CURRENT_DATE - INTERVAL '1 month'")
		if last_edit_limit == 'Last year':
			conditions.append(f"{type_alias}.last_edit <= CURRENT_DATE - INTERVAL '1 year'")

	if 'Text Note' in types:
		note_conditions = ["n.is_deleted = false", "n.user_id = %s"]
		params.append(uid)
		add_conditions('n', 'nt', note_conditions, params)
		note_query = f"""
		SELECT
			'Notes' AS note_type,
			n.note_id,
			n.user_id,
			n.title,
			n.content,
			n.creation_date,
			n.last_edit,
			n.favorite,
			n.is_deleted
		FROM
			Notes n
		LEFT JOIN
			NotesTags nt ON n.note_id = nt.id
		WHERE
			{' AND '.join(note_conditions)}
		"""
		queries.append(note_query)

	if 'Whiteboard' in types:
		wb_conditions = ["wn.is_deleted = false", "wn.user_id = %s"]
		params.append(uid)
		add_conditions('wn', 'wt', wb_conditions, params)
		wb_query = f"""
		SELECT
			'WhiteboardNotes' AS note_type,
			wn.whiteboard_note_id AS note_id,
			wn.user_id,
			wn.title,
			wn.content,
			wn.creation_date,
			wn.last_edit,
			wn.favorite,
			wn.is_deleted
		FROM
			WhiteboardNotes wn
		LEFT JOIN
			WhiteboardsTags wt ON wn.whiteboard_note_id = wt.id
		WHERE
			{' AND '.join(wb_conditions)}
		"""
		queries.append(wb_query)

	if 'Recording' in types:
		rec_conditions = ["r.is_deleted = false", "r.user_id = %s"]
		params.append(uid)
		add_conditions('r', 'rt', rec_conditions, params)
		rec_query = f"""
		SELECT
			'Recordings' AS note_type,
			r.recording_id AS note_id,
			r.user_id,
			r.title,
			r.content,
			r.creation_date,
			r.last_edit,
			r.favorite,
			r.is_deleted
		FROM
			Recordings r
		LEFT JOIN
			RecordingsTags rt ON r.recording_id = rt.id
		WHERE
			{' AND '.join(rec_conditions)}
		"""
		queries.append(rec_query)

	full_query = " UNION ALL ".join(queries)
	full_query += " ) ORDER BY last_edit DESC;"
	full_query = "SELECT DISTINCT * FROM(" + full_query

	try:
		c.execute(full_query, tuple(params))
		result = c.fetchall()
		return result
	finally:
		db_connect.conn.commit()
		db_connect.conn.close()
