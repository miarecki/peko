import psycopg2
from argon2 import PasswordHasher

# this needs to be secret - leave for now.
def db_connect():
	db_connect.conn = psycopg2.connect(
		host = 'clqu6b0gqk6s73914ud0-a.frankfurt-postgres.render.com',
		database = 'peko_postgresql_instance',
		user = 'peko_postgresql_instance_user',
		password = 'xXz1d3dAxeOKPmJEWKv7h02hj3L0MuqM',
		port = '5432',
		)

# =========================================================

# create users only (for now) - no encryption
def db_create():
	db_connect()

	c = db_connect.conn.cursor()

	c.execute('''
       CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    encryption_key VARCHAR(255) NOT NULL
);

-- Create Contacts table
CREATE TABLE Contacts (
    contact_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    contact_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL
);

-- Create Settings table
CREATE TABLE Settings (
    setting_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    mode VARCHAR(50) NOT NULL,
    button_color VARCHAR(50) NOT NULL
);

-- Create Trash table
CREATE TABLE Trash (
    trash_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    note_id INT,
    whiteboard_note_id INT,
    reminder_id INT,
    recording_id INT,
    deleted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tags table
CREATE TABLE Tags (
    tag_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL
);

-- Create Notes table
CREATE TABLE Notes (
    note_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_edit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    favorite BOOLEAN,
    tag_id INT REFERENCES Tags(tag_id) ON DELETE SET NULL
);

-- Create WhiteboardNotes table
CREATE TABLE WhiteboardNotes (
    whiteboard_note_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    favorite BOOLEAN,
    tag_id INT REFERENCES Tags(tag_id) ON DELETE SET NULL
);

-- Create Recordings table
CREATE TABLE Recordings (
    recording_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    favorite BOOLEAN,
    tag_id INT REFERENCES Tags(tag_id) ON DELETE SET NULL
);

-- Create Reminders table
CREATE TABLE Reminders (
    reminder_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_edit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Statistics table
CREATE TABLE Statistics (
    statistics_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    notes_created INT DEFAULT 0,
    whiteboardnotes_created INT DEFAULT 0,
    notes_deleted INT DEFAULT 0,
    whiteboardnotes_deleted INT DEFAULT 0
);
    ''')

    # Close the cursor and connection
	db_connect.conn.commit()
	db_connect.conn.close()

# =========================================================

def db_add_user(acc_name, hashed_password, enc_key):
	db_connect()

	c = db_connect.conn.cursor() 

	c.execute('''
        INSERT INTO Users (username, password_hash, encryption_key)
        VALUES (%s, %s, %s);''', (acc_name, hashed_password, enc_key))


    # Close the cursor and connection
	db_connect.conn.commit()
	db_connect.conn.close()


# =========================================================

def db_test_select():
	db_connect()

	c = db_connect.conn.cursor() 

	c.execute('''
        SELECT * FROM Users;''')
	records = c.fetchall()

    # Close the cursor and connection
	db_connect.conn.commit()
	db_connect.conn.close()

	print(records)

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

# =========================================================


def db_nuke():
	db_connect()

	c = db_connect.conn.cursor() 

	try:
		c.execute('''

DROP TABLE IF EXISTS Trash CASCADE;

DROP TABLE IF EXISTS Notes CASCADE;

DROP TABLE IF EXISTS WhiteboardNotes CASCADE;

DROP TABLE IF EXISTS Reminders CASCADE;

DROP TABLE IF EXISTS Tags CASCADE;

DROP TABLE IF EXISTS Settings CASCADE;

DROP TABLE IF EXISTS Contacts CASCADE;

DROP TABLE IF EXISTS Users CASCADE;

DROP TABLE IF EXISTS Statistics CASCADE;

DROP TABLE IF EXISTS Recordings CASCADE;
''')

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_text_notes(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Notes
			WHERE user_id = %s;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def insert_text_note(uid, t, con, fav, tag):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''INSERT INTO Notes(user_id, title, content, favorite, tag_id)
			VALUES (%s, %s, %s, %s, %s);
''', (uid, t, con, fav, tag))

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

# ========================================================

def get_tag_id(tag_name):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT tag_id FROM Tags
			WHERE tag = %s;
''', (tag_name,))

		result = c.fetchone()
		return result[0]

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def insert_tag(uid, tag_name):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''INSERT INTO Tags(user_id, tag)
			VALUES (%s, %s);
''', (uid, tag_name))

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_note_content(nid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT content FROM Notes
			WHERE note_id = %s;
''', (nid,))

		result = c.fetchone()
		return result[0]

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# ========================================================

def get_note_title(nid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT title FROM Notes
			WHERE note_id = %s;
''', (nid,))

		result = c.fetchone()
		return result[0]

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()