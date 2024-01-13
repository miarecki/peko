import psycopg2
from argon2 import PasswordHasher

# this needs to be secret - leave for now.
def db_connect():
	db_connect.conn = psycopg2.connect(
		host = ':)',
		database = ':)',
		user = ':)',
		password = ':)',
		port = '5432',
		)

# =========================================================

def db_create():
	db_connect()

	c = db_connect.conn.cursor()

	c.execute('''

CREATE TABLE Users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Create Notes table
CREATE TABLE Notes (
    note_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_edit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    favorite BOOLEAN,
    is_deleted BOOLEAN DEFAULT false
);

-- Create WhiteboardNotes table
CREATE TABLE WhiteboardNotes (
    whiteboard_note_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_edit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    favorite BOOLEAN,
    is_deleted BOOLEAN DEFAULT false
);

-- Create Recordings table
CREATE TABLE Recordings (
    recording_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    favorite BOOLEAN,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT false
);

-- Create Reminders table
CREATE TABLE Reminders (
    reminder_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remind_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Contacts table
CREATE TABLE Contacts (
    contact_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    contact_avatar VARCHAR(255) DEFAULT '/gui/avatar_default.png',
    contact_display_name VARCHAR(255) NOT NULL,
    contact_first_name VARCHAR(255),
    contact_last_name VARCHAR(255),
    contact_phone VARCHAR(255),
    contact_email VARCHAR(255)
);

-- Create Settings table
CREATE TABLE Settings (
    setting_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    theme VARCHAR(50) NOT NULL
);

--- Type Enum Table
CREATE TABLE Type (
    type_name VARCHAR(50) PRIMARY KEY NOT NULL);
INSERT INTO Type(type_name) VALUES ('Text Note'), ('Whiteboard'), ('Recording'), ('Reminder'), ('Contact');

--- Action Enum Table
CREATE TABLE Action (
    action_name VARCHAR(50) PRIMARY KEY NOT NULL);
INSERT INTO Action(action_name) VALUES ('Create'), ('Edit'), ('Delete');

-- Create History table
CREATE TABLE History (
    history_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    action_type VARCHAR(50) REFERENCES Action(action_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    item_type VARCHAR(50) REFERENCES Type(type_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    item_name VARCHAR(255),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--- Tag Enum Table
CREATE TABLE Tags (
    tag_name VARCHAR(50) PRIMARY KEY NOT NULL);
INSERT INTO Tags(tag_name) VALUES ('Personal'), ('School'), ('Work'), ('Other');

-- Junction table for many-to-many relationship between Tags and Notes
CREATE TABLE NotesTags (
    id INTEGER REFERENCES Notes(note_id) ON DELETE CASCADE ON UPDATE CASCADE,
    tag_name VARCHAR(50) REFERENCES Tags(tag_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    PRIMARY KEY (id, tag_name)
);

-- Junction table for many-to-many relationship between Tags and WhiteboardNotes
CREATE TABLE WhiteboardsTags (
    id INTEGER REFERENCES WhiteboardNotes(whiteboard_note_id) ON DELETE CASCADE ON UPDATE CASCADE,
    tag_name VARCHAR(50) REFERENCES Tags(tag_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    PRIMARY KEY (id, tag_name)
);

-- Junction table for many-to-many relationship between Tags and Recordings
CREATE TABLE RecoringsTags (
    id INTEGER REFERENCES Recordings(recording_id) ON DELETE CASCADE ON UPDATE CASCADE,
    tag_name VARCHAR(50) REFERENCES Tags(tag_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    PRIMARY KEY (id, tag_name)
);

    ''')

    # Close the cursor and connection
	db_connect.conn.commit()
	db_connect.conn.close()

# =========================================================

def db_add_user(acc_name, hashed_password):
	db_connect()

	c = db_connect.conn.cursor() 

	c.execute('''
        INSERT INTO Users (username, password_hash)
        VALUES (%s, %s);''', (acc_name, hashed_password))

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

    finally:
        db_connect.conn.commit()
        db_connect.conn.close()

# Example usage:
# insert_text_note(1, "Note Title", "Note Content", True, ["Personal", "Work"])


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

    finally:
        db_connect.conn.commit()
        db_connect.conn.close()

#===============

def get_contacts(uid):
    db_connect()
    c = db_connect.conn.cursor()

    try:
        # Check if the view already exists
        c.execute('''SELECT EXISTS (
            SELECT 1 FROM information_schema.views 
            WHERE table_name = 'current_user_contacts'
        );''')

        view_exists = c.fetchone()[0]

        if not view_exists:
            # Create the view if it doesn't exist
            c.execute('''CREATE VIEW current_user_contacts AS 
                SELECT * FROM Contacts
                WHERE user_id = %s;
            ''', (uid,))

        # Fetch the data from the view
        c.execute('''SELECT * FROM current_user_contacts
            WHERE user_id = %s;
        ''', (uid,))

        result = c.fetchall()
        return result

    finally:
        db_connect.conn.commit()
        db_connect.conn.close()


# =======

def get_text_note(nid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Notes
			WHERE note_id = %s;
''', (nid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =================

def test_select_contacts():

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM Contacts;''')

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()


# =======

def get_contact(cid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM current_user_contacts
			WHERE contact_id = %s;
''', (cid,))

		result = c.fetchone()
		return result

	except:

		c.execute('''SELECT * FROM Contacts
			WHERE contact_id = %s;
''', (cid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()



# =================

def remove_contact(contact_id):
    db_connect()
    c = db_connect.conn.cursor()

    try:
        query = '''
            DELETE FROM current_user_contacts
            WHERE contact_id = %s;
        '''
        c.execute(query, (contact_id,))
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

    finally:
        db_connect.conn.commit()
        db_connect.conn.close()

# =========================

def get_whiteboards(uid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM WhiteboardNotes
			WHERE user_id = %s;
''', (uid,))

		result = c.fetchall()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()

# =========================

def get_whiteboard(wid):

	db_connect()
	c = db_connect.conn.cursor() 

	try:
		c.execute('''SELECT * FROM WhiteboardNotes
			WHERE whiteboard_note_id = %s;
''', (wid,))

		result = c.fetchone()
		return result

	finally:

		db_connect.conn.commit()
		db_connect.conn.close()