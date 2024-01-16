-- Create Users table
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




