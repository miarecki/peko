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
    duration NUMERIC,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_edit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    favorite BOOLEAN,
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
    display_name VARCHAR(255),
    avatar VARCHAR(255) DEFAULT '/gui/avatar_default.png',
    color_scheme VARCHAR(50) DEFAULT '#1A6EB5'
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
CREATE TABLE RecordingsTags (
    id INTEGER REFERENCES Recordings(recording_id) ON DELETE CASCADE ON UPDATE CASCADE,
    tag_name VARCHAR(50) REFERENCES Tags(tag_name) ON UPDATE CASCADE ON DELETE RESTRICT,
    PRIMARY KEY (id, tag_name)
);

CREATE OR REPLACE FUNCTION set_default_display_name()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.display_name := (SELECT username FROM Users WHERE user_id = NEW.user_id);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER set_display_name_before_insert
    BEFORE INSERT ON Settings
    FOR EACH ROW
    EXECUTE FUNCTION set_default_display_name();

CREATE VIEW Statistics AS
SELECT
    U.user_id,
    -- General statistics
    COUNT(DISTINCT N.note_id) + COUNT(DISTINCT WN.whiteboard_note_id) + COUNT(DISTINCT R.recording_id) AS total_notes,
    COUNT(DISTINCT N.note_id) AS unique_notes,
    COUNT(DISTINCT WN.whiteboard_note_id) AS unique_whiteboards,
    COUNT(DISTINCT R.recording_id) AS unique_recordings,

    -- Note statistics
    MIN(LENGTH(N.content)) AS min_note_length,
    MAX(LENGTH(N.content)) AS max_note_length,
    AVG(LENGTH(N.content)) AS avg_note_length,

    -- Recording statistics
    MIN(R.duration) AS min_recording_duration,
    MAX(R.duration) AS max_recording_duration,
    AVG(R.duration) AS avg_recording_duration,

    -- Reminder statistics
    COUNT(DISTINCT REM.reminder_id) AS total_reminders,

    -- Contact statistics
    COUNT(DISTINCT C.contact_id) AS total_contacts

FROM
    Users U
LEFT JOIN Notes N ON U.user_id = N.user_id AND N.is_deleted = false
LEFT JOIN WhiteboardNotes WN ON U.user_id = WN.user_id AND WN.is_deleted = false
LEFT JOIN Recordings R ON U.user_id = R.user_id AND R.is_deleted = false
LEFT JOIN Reminders REM ON U.user_id = REM.user_id
LEFT JOIN Contacts C ON U.user_id = C.user_id

GROUP BY
    U.user_id;

 -- Current History view   
CREATE VIEW CurrentHistory AS
SELECT 
    user_id, 
    TO_CHAR(action_date, 'DD-MM-YYYY') as action_date_formatted,
    TO_CHAR(action_date, 'HH24:MI') as action_time,
    item_type, 
    item_name, 
    action_type
FROM 
    History
WHERE 
    action_date > CURRENT_TIMESTAMP - INTERVAL '1 week'
GROUP BY 
    user_id, action_date, item_type, item_name, action_type
ORDER BY 
    action_date DESC;