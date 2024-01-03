-- Create Users table
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
