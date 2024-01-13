# Import
import tkinter
import tkcalendar
import customtkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import peko_database
import encryption_mech
from user import User

# LOGIN PAGE:
# 2do: 	- whiteboards
#		- recordings
#		- everything else
#		- encryption

# colors:
dgrey = '#1f1f1f'
grey = '#282828'
lgrey = '#323232'
bluey = '#1a6eb5'
bluehover = '#317dbc'

global avatar_file_path
avatar_file_path = ''



def run_login_page():

	# colors:  left #1f1f1f \  middle  #282828 \ right #323232
	# blues:  fg_color= #1a6eb5   hover_color = #317dbc

	# System Settings
	current_path = os.path.dirname(os.path.realpath(__file__))

	# Functions

	def user_log_in():
		# user clicks 'Log In' button
		login_cred = account_name_tb.get().strip()
		pass_cred = account_password_tb.get()
		real_pass = pass_cred
		
		if encryption_mech.log_in(login_cred, real_pass) == 'Success!':
			print(f"Log In Success!")
			user_id = peko_database.get_uid(login_cred)
			global current_user
			current_user = User(user_id)
			login_page.destroy() # kinda works
			run_app()
		else:
			print(f":( {encryption_mech.log_in(login_cred, real_pass)}")


	def create_account():
		# users clicks 'Create Account' button
		acc_name_cred = new_account_name_tb.get().strip()
		new_pass_cred = new_account_password_tb.get()
		new_pass_confirm_cred = new_account_confirm_password_tb.get()

		new_real_pass = new_pass_cred
		new_real_pass_confirm = new_pass_confirm_cred

		valid = encryption_mech.create_new_account(acc_name_cred, new_real_pass, new_real_pass_confirm)
		if valid == 'Success!':
			valid
			user_id = peko_database.get_uid(acc_name_cred)
			global current_user
			current_user = User(user_id)
			login_page.destroy() # kinda works
			run_app()
		else:
			print(valid)


	# App Frame
	login_page = customtkinter.CTk()
	login_page.geometry("640x480")
	login_page.title("PEKO")
	login_page.resizable(0,0)

	# Background Image
	login_page.bg_image = customtkinter.CTkImage(Image.open(current_path + "/gui/login_background.png"), size=(640, 480))
	login_page.bg_image_label = customtkinter.CTkLabel(login_page, image=login_page.bg_image, text="")
	login_page.bg_image_label.place(relx=0, rely=0, anchor="nw")  # Place the image in the top-left corner
	login_page.bg_image_label.lower()

	# Icon
	login_page.iconbitmap(current_path + "/gui/icon.ico")

	# BUTTONS

	# 'Log In' Button 
	log_in_button = customtkinter.CTkButton(
	master = login_page,
	command = user_log_in,
	text = 'Log In',
	width = 160,
	height = 30,
	font = ('Segoe', 14, 'bold'),
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f'
		     )
	log_in_button.place(x=105, y=282)


	# 'Create Account' Button 
	create_account_button = customtkinter.CTkButton(
	master = login_page,
	command = create_account,
	text = 'Create Account',
	width = 160,
	height = 30,
	font = ('Segoe', 14, 'bold'),
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f'
		     )
	create_account_button.place(x=375, y=332)


	# TEXT BOXES // ENTRIES

	# Account Name TB
	account_name_tb = customtkinter.CTkEntry(
	master = login_page,
	width = 180,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	account_name_tb.place(x=95, y=182)

	# Log In Password TB
	account_password_tb = customtkinter.CTkEntry(
	master = login_page,
	width = 180,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = '',
	show = '*'
			)
	account_password_tb.place(x=95, y=232)

	# New Account Name TB
	new_account_name_tb = customtkinter.CTkEntry(
	master = login_page,
	width = 180,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	new_account_name_tb.place(x=365, y=182)

	# New Account Password TB
	new_account_password_tb = customtkinter.CTkEntry(
	master = login_page,
	width = 180,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = '',
	show = '*'
			)
	new_account_password_tb.place(x=365, y=232)

	# New Account Password TB
	new_account_confirm_password_tb = customtkinter.CTkEntry(
	master = login_page,
	width = 180,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = '',
	show = '*'
			)
	new_account_confirm_password_tb.place(x=365, y=282)


	# TEXT ELEMENTS

	# Bottom text: created



	# Bottom text: git link


	# Error text



	# Run
	login_page.mainloop()


# MAIN APP

def run_app():

	# colors:  left #1f1f1f \  middle  #282828 \ right #323232

	# System Settings
	current_path = os.path.dirname(os.path.realpath(__file__))
	default_avatar_display_image = customtkinter.CTkImage(Image.open(current_path + '/gui/avatar_default.png'), size=(128, 128))
	default_user_avatar =  customtkinter.CTkImage(Image.open(current_path + '/gui/avatars/test_user_avatar.jpg'), size=(64, 64))
	font = ('Segoe', 15)

	# App Frame
	app = customtkinter.CTk()
	app.geometry("1080x720")
	app.title("PEKO")
	app.resizable(0,0)

	# Background Image
	app.bg_image = customtkinter.CTkImage(Image.open(current_path + "/gui/background.png"), size=(1080, 720))
	app.bg_image_label = customtkinter.CTkLabel(app, image=app.bg_image, text="")
	app.bg_image_label.place(relx=0, rely=0, anchor="nw")  # Place the image in the top-left corner
	app.bg_image_label.lower()

	# Icon
	app.iconbitmap(current_path + "/gui/icon.ico")

	def set_wawla(value):
	    global wawla
	    wawla = value

	def update_wawla_text():
	    wawla_text.configure(text=wawla)   

	# return to default color (it is so cheap and stupid, but it will work)
	def lights_out(except_me):
		for btn in button_list:
			if except_me != btn:
				btn.configure(fg_color="#1f1f1f", hover_color = '#282828')

	# tab (frame) switcher
	def switch_frame(frame_name):
		for frame in frame_list:
			if frame_name != frame:
				frame_name.place(x=220, y=100)
				#frame.place_forget()
				frame.grid_forget()
				frame.place_forget()

	# showscreen switcher
	def switch_screen(screen_name):
		for screen in screen_list:
			if screen_name != screen:
				screen_name.place(x=560, y=50)
				screen.place_forget()

	# Functions
	def show_all_notes():
		# self-explanatory
		lights_out(all_notes_button)
		all_notes_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('All notes')
		update_wawla_text()
		switch_frame(all_notes_frame)
		print(f"test: all notes")

	def show_all_reminders():
		# self-explanatory
		lights_out(reminders_button)
		reminders_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Reminders')
		update_wawla_text()
		switch_frame(reminders_frame)
		print("test: reminders")

	def show_all_favorites():
		# self-explanatory
		lights_out(favorites_button)
		set_wawla('Favorites')
		update_wawla_text()
		switch_frame(favorites_frame)
		favorites_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		print("test: favorites")

	def show_statistics():
		# self-explanatory
		lights_out(statistics_button)
		statistics_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Statistics')
		switch_frame(statistics_frame)
		update_wawla_text()
		print("test: statistics")

	def show_all_text():
		# self-explanatory
		lights_out(text_button)
		text_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Text notes')
		switch_frame(only_text_notes_frame)
		update_wawla_text()
		print("test: text notes")

		text_notes_list = []

		# Just Text Note Buttons Creation on TEXT
		text_notes = current_user.get_text_notes()
		row = 0
		buttons = []
		newline = '\n'
		for elem in text_notes:

			text_note = customtkinter.CTkButton(
				master = only_text_notes_frame,
				command = lambda x=elem[0]: text_note_display(x),
				image = text_image,
				width = 250,
				height = 50,
				text = f"{elem[2]} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = '#1a6eb5',
				hover_color = '#323232',
				border_width = 1,
				)
			text_note.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(text_note)

	def text_note_display(note_id):

		notes = peko_database.get_text_note(note_id)

		switch_screen(text_note_display_screen)
		text_note_title_label.configure(text = notes[2])
		text_note_content_tb.configure(state = 'normal')
		text_note_content_tb.delete("0.0", "end")
		text_note_content_tb.insert("0.0", notes[3])
		text_note_content_tb.configure(state = 'disabled')

		text_note_title_label.grid(row=0, column=0, padx=10, pady=(0, 20))
		text_note_content_tb.grid(row=1, column=0, padx=10, pady=(0, 20))
		
	def show_all_whiteboards():
		# self-explanatory
		lights_out(whiteboards_button)
		whiteboards_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Whiteboards')
		switch_frame(only_whiteboards_frame)
		update_wawla_text()
		print("test: whiteboards")

		whiteboards_list = []

		# Just Text Note Buttons Creation on TEXT
		whiteboards = current_user.get_whiteboards()
		row = 0
		buttons = []
		newline = '\n'
		for elem in whiteboards:

			whiteboard = customtkinter.CTkButton(
				master = only_whiteboards_frame,
				command = lambda x=elem[0]: whiteboard_display(x),
				image = whiteboards_image,
				width = 250,
				height = 50,
				text = f"{elem[2]} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = '#1a6eb5',
				hover_color = '#323232',
				border_width = 1,
				)
			whiteboard.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(whiteboard)

	def whiteboard_display(whiteboard_id):

		whiteboards = peko_database.get_whiteboard(whiteboard_id)

		switch_screen(whiteboard_display_screen)

		whiteboard_title_label.configure(text = whiteboards[2])
		whiteboard_picture = customtkinter.CTkImage(Image.open(whiteboards[3]), size = (476, 564))
		whiteboard_title_label.place(x=20, y=20)

		whiteboard_picture_button = customtkinter.CTkButton(
			master = whiteboard_display_screen,
			image = whiteboard_picture,
			width = 476,
			height = 564,
			bg_color = lgrey,
			fg_color = lgrey,
			text = '',
			border_width = 0,
			hover_color = lgrey
			)
		whiteboard_picture_button.place(x=3,y=60)

	def show_all_recordings():
		# self-explanatory
		lights_out(recordings_button)
		recordings_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Recordings')
		switch_frame(only_recordings_frame)
		update_wawla_text()
		print("test: recordings")

	def show_all_contacts():
		# self-explanatory
		lights_out(contacts_button)
		contacts_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Contacts')
		switch_frame(contacts_frame)
		update_wawla_text()

		contacts_list = []

		contacts = current_user.get_contacts()
		row = 1
		buttons = []
		for elem in contacts:

			path = elem[2]

			if path == '/gui/avatar_default.png':
				path = current_path + '/gui/avatar_default.png'

			contact = customtkinter.CTkButton(
				master = contacts_frame,
				command = lambda x=elem[0]: contact_display(x),
				image = customtkinter.CTkImage(Image.open(path), size=(32, 32)),
				width = 250,
				height = 50,
				text = f'{elem[3]}',
				font=('Segoe', 15, 'bold'),
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = '#1a6eb5',
				hover_color = '#323232',
				)
			contact.grid(row=row, column=0, padx=10, pady=(0, 20))
			row += 1
			buttons.append(contact)

	def contact_display(contact_id):

		contact = peko_database.get_contact(contact_id)
		contact = [x if x != None else '-' for x in contact]
		path = contact[2]

		if path == '/gui/avatar_default.png':
			path = current_path + '/gui/avatar_default.png'
		
		avatar = customtkinter.CTkImage(Image.open(path), size=(128, 128))

		switch_screen(contact_display_screen)
		contact_display_name_label.configure(text = contact[3])
		contact_display_avatar_button.configure(image = avatar)

		contact_display_first_name.configure(text = contact[-4])
		contact_display_last_name.configure(text = contact[-3])
		contact_display_email.configure(text = contact[-1])
		contact_display_phone.configure(text = contact[-2])

		contact_display_name_label.place(x=30,y=50)
		contact_display_avatar_button.place(x=20,y=120)

	def show_history():
		# self-explanatory
		lights_out(history_button)
		history_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('History')
		switch_frame(history_frame)
		update_wawla_text()

	def show_settings():
		# self-explanatory
		lights_out(settings_button)
		settings_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Settings')
		switch_frame(settings_frame)
		update_wawla_text()

	def show_add_content_screen():
		switch_screen(add_content_screen)
		print('test: add some note.')

	def add_new_text_note():
		switch_screen(add_text_note_screen)

	def	add_new_whiteboard_note():
		switch_screen(add_whiteboard_screen)

	def add_new_recording_note():
		pass

	def new_note_cancel():
		switch_screen(add_content_screen)

	def note_tags():
		tags = []
		if note_tag_personal_button.cget('fg_color') == bluey:
			tags.append('Personal')
		if note_tag_work_button.cget('fg_color') == bluey:
			tags.append('School')
		if note_tag_school_button.cget('fg_color') == bluey:
			tags.append('Work')
		if note_tag_other_button.cget('fg_color') == bluey:
			tags.append('Other')
		return tags

	def whiteboard_tags():
		tags = []
		if whiteboard_tag_personal_button.cget('fg_color') == bluey:
			tags.append('Personal')
		if whiteboard_tag_work_button.cget('fg_color') == bluey:
			tags.append('School')
		if whiteboard_tag_school_button.cget('fg_color') == bluey:
			tags.append('Work')
		if whiteboard_tag_other_button.cget('fg_color') == bluey:
			tags.append('Other')
		return tags

	def new_note_submit():
		title = new_note_title_tb.get().strip()
		favorite = check_if_fav_button()
		content = new_note_content_tb.get('0.0', 'end').strip()

		tags = note_tags()

		peko_database.insert_text_note(current_user.user_id, title, content, favorite, tags)
		switch_screen(add_content_screen)

	def check_if_fav_button():
		if new_note_favorite_button.cget("image") == favorites_empty_image:
			return False
		return True

	def check_if_fav_button2():
		if new_whiteboard_favorite_button.cget("image") == favorites_empty_image:
			return False
		return True

	def check_if_fav_button3():
		if new_reminder_favorite_button.cget("image") == favorites_empty_image:
			return False
		return True

	def new_note_fav():
		if new_note_favorite_button.cget("image") == favorites_empty_image:
			new_note_favorite_button.configure(image = favorites_filled_image)
		else:
			new_note_favorite_button.configure(image = favorites_empty_image)

	def new_whiteboard_fav():
		if new_whiteboard_favorite_button.cget("image") == favorites_empty_image:
			new_whiteboard_favorite_button.configure(image = favorites_filled_image)
		else:
			new_whiteboard_favorite_button.configure(image = favorites_empty_image)

	def new_reminder_fav():
		if new_reminder_favorite_button.cget("image") == favorites_empty_image:
			new_reminder_favorite_button.configure(image = favorites_filled_image)
		else:
			new_reminder_favorite_button.configure(image = favorites_empty_image)

	def add_new_contact_clicked():
		switch_screen(add_contact_screen)

	def add_avatar_to_contact():

		file_path = askopenfilename()
		if file_path:
			global avatar_file_path
			avatar_file_path = file_path
			avatar = customtkinter.CTkImage(Image.open(avatar_file_path), size=(128, 128))
			contact_avatar_button.configure(image = avatar)

	def new_contact_cancel():
		switch_screen(add_content_screen)

	def cancel_new_whiteboard():
		switch_screen(add_content_screen)

	def save_new_whiteboard():
		# Allow the user to choose the location and file name
		file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
		# how?
		if file_path:
			x = add_whiteboard_screen.winfo_rootx() + canvas.winfo_x()
			y = add_whiteboard_screen.winfo_rooty() + canvas.winfo_y()
			x1 = x + canvas.winfo_width()
			y1= y + canvas.winfo_height()
			ImageGrab.grab().crop((x,y,x1,y1)).save(file_path)

		# add to database
		title = whiteboard_title_tb.get().strip()
		content = file_path
		favorite = new_whiteboard_fav()
		tags = whiteboard_tags()
		print(tags)
		peko_database.insert_whiteboard(current_user.user_id, title, content, favorite, tags)

	def new_contact_submit():
		global avatar_file_path

		uid = current_user.user_id
		display_name = display_name_tb.get().strip()
		first_name = first_name_tb.get().strip()
		last_name = last_name_tb.get().strip()
		email = email_tb.get().strip()
		phone = phone_tb.get().strip()
		avatar = avatar_file_path

		peko_database.insert_contact(uid, display_name, first_name, last_name, email, phone, avatar)
		avatar_file_path = ''
		switch_screen(add_content_screen)
		show_all_contacts()

	def add_new_reminder_clicked():
		switch_screen(add_reminder_screen)

	def new_reminder_submit():
		pass

	def new_reminder_cancel():
		pass

	def show_all_personal():
		# self-explanatory
		lights_out(personal_button)
		personal_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Personal')
		switch_frame(only_personal_frame)
		update_wawla_text()

	def show_all_work():
		# self-explanatory
		lights_out(work_button)
		work_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Work')
		switch_frame(only_work_frame)
		update_wawla_text()

	def show_all_school():
		# self-explanatory
		lights_out(school_button)
		school_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('School')
		switch_frame(only_school_frame)
		update_wawla_text()

	def show_all_other():
		# self-explanatory
		lights_out(other_button)
		other_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Other')
		switch_frame(only_other_frame)
		update_wawla_text()

	def show_search():
		pass

	def note_tags_light_up(button):
	    if button.cget('fg_color') == grey:
	        button.configure(fg_color = bluey, hover_color = bluehover)
	    else:
	        button.configure(fg_color = grey, hover_color = '#474747')

	def whiteboard_tags_light_up(button):
	    if button.cget('fg_color') == grey:
	        button.configure(fg_color = bluey, hover_color = bluehover)
	    else:
	        button.configure(fg_color = grey, hover_color = '#474747')

	# Left Panel Image and Buttons - MAIN

	# All Notes Button
	all_notes_image = customtkinter.CTkImage(Image.open(current_path + "/gui/all_notes_icon.png"), size=(20, 20))
	all_notes_button = customtkinter.CTkButton(
	master = app,
	command = show_all_notes,
	image = all_notes_image,
	text = 'All notes',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	all_notes_button.place(x=20, y=50)

	# Reminders Button
	reminders_image = customtkinter.CTkImage(Image.open(current_path + "/gui/reminders_icon.png"), size=(20, 20))
	reminders_button = customtkinter.CTkButton(
	master = app,
	command = show_all_reminders,
	image = reminders_image,
	text = 'Reminders',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	reminders_button.place(x=20, y=80)

	# Favorites Button
	favorites_image = customtkinter.CTkImage(Image.open(current_path + "/gui/favorites_icon.png"), size=(20, 20))
	favorites_button = customtkinter.CTkButton(
	master = app,
	command = show_all_favorites,
	image = favorites_image,
	text = 'Favorites',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	favorites_button.place(x=20, y=110)

	# Contacts Button
	contacts_image = customtkinter.CTkImage(Image.open(current_path + "/gui/contacts_icon.png"), size=(20, 20))
	contacts_button = customtkinter.CTkButton(
	master = app,
	command = show_all_contacts,
	image = contacts_image,
	text = 'Contacts',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	contacts_button.place(x=20, y=140)

	# Statistics Button
	statistics_image = customtkinter.CTkImage(Image.open(current_path + "/gui/statistics_icon.png"), size=(20, 20))
	statistics_button = customtkinter.CTkButton(
	master = app,
	command = show_statistics,
	image = statistics_image,
	text = 'Statistics',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	statistics_button.place(x=20, y=170)

	# Text Button
	text_image = customtkinter.CTkImage(Image.open(current_path + "/gui/text_icon.png"), size=(20, 20))
	text_button = customtkinter.CTkButton(
	master = app,
	command = show_all_text,
	image = text_image,
	text = 'Text',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	text_button.place(x=20, y=250)

	# Whiteboards Button
	whiteboards_image = customtkinter.CTkImage(Image.open(current_path + '/gui/whiteboards_icon.png'), size=(20, 20))
	whiteboards_button = customtkinter.CTkButton(
	master = app,
	command = show_all_whiteboards,
	image = whiteboards_image,
	text = 'Whiteboards',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	whiteboards_button.place(x=20, y=280)

	# Recordings Button
	recordings_image = customtkinter.CTkImage(Image.open(current_path + "/gui/recordings_icon.png"), size=(20, 20))
	recordings_button = customtkinter.CTkButton(
	master = app,
	command = show_all_recordings,
	image = recordings_image,
	text = 'Recordings',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	recordings_button.place(x=20, y=310)

	# Personal Button
	personal_image = customtkinter.CTkImage(Image.open(current_path + "/gui/personal_icon.png"), size=(20, 20))
	personal_button = customtkinter.CTkButton(
	master = app,
	command = show_all_personal,
	image = personal_image,
	text = 'Personal',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	personal_button.place(x=20, y=390)

	# Work Button
	work_image = customtkinter.CTkImage(Image.open(current_path + "/gui/work_icon.png"), size=(20, 20))
	work_button = customtkinter.CTkButton(
	master = app,
	command = show_all_work,
	image = work_image,
	text = 'Work',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	work_button.place(x=20, y=420)

	# School Button
	school_image = customtkinter.CTkImage(Image.open(current_path + "/gui/school_icon.png"), size=(20, 20))
	school_button = customtkinter.CTkButton(
	master = app,
	command = show_all_school,
	image = school_image,
	text = 'School',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	school_button.place(x=20, y=450)

	# Other Button
	other_image = customtkinter.CTkImage(Image.open(current_path + "/gui/other_icon.png"), size=(20, 20))
	other_button = customtkinter.CTkButton(
	master = app,
	command = show_all_other,
	image = other_image,
	text = 'Other',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	other_button.place(x=20, y=480)

	# Hisory Button
	history_image = customtkinter.CTkImage(Image.open(current_path + "/gui/history_icon.png"), size=(20, 20))
	history_button = customtkinter.CTkButton(
	master = app,
	command = show_history,
	image = history_image,
	text = 'History',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	history_button.place(x=20, y=560)

	# Settings Button
	settings_image = customtkinter.CTkImage(Image.open(current_path + "/gui/settings_icon.png"), size=(20, 20))
	settings_button = customtkinter.CTkButton(
	master = app,
	command = show_settings,
	image = settings_image,
	text = 'Settings',
	width = 160,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = '#1f1f1f',
	hover_color = '#282828',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f',
	font = font
		     )
	settings_button.place(x=20, y=590)

	# User Avatar Button
	user_avatar_button = customtkinter.CTkButton(
	master = app,
	image = default_user_avatar,
	text = '',
	width = 64,
	height = 64,
	fg_color = '#1f1f1f',
	hover_color = '#1f1f1f',
	background_corner_colors=['#1f1f1f', '#1f1f1f', '#1f1f1f', '#1f1f1f'],
	bg_color = '#1f1f1f'
		     )
	user_avatar_button.place(x=10, y=630) # 640

	# ==========================================================================================================
	# Middle Panel Image and Buttons and Frames - MAIN

	# How Do Tabs (Frames) Work?

	all_notes_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = '#1a6eb5',
		border_width = 3
		)
	all_notes_frame.place(x=220, y=100)

	reminders_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = '#1a6eb5',
		border_width = 3,
		)

	favorites_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = '#1a6eb5',
		border_width = 3,
		)

	contacts_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = '#1a6eb5',
		border_width = 3,
		)

	statistics_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = '#1a6eb5',
		border_width = 3,
		)

	only_text_notes_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	only_whiteboards_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	only_recordings_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	only_personal_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	only_work_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	only_school_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	only_other_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	history_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)

	settings_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	)


# =============================================


	# Add Button
	add_button = customtkinter.CTkButton(
	master = app,
	command = show_add_content_screen,
	text = '+',
	font=('Segoe', 24),
	width = 36,
	height = 36,
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
	bg_color = '#282828'
		     )
	add_button.place(x=490, y=10)

	# Search Button
	search_image = customtkinter.CTkImage(Image.open(current_path + "/gui/search_icon.png"), size=(20, 20))
	search_button = customtkinter.CTkButton(
	master = app,
	command = show_search,
	image = search_image,
	text = 'Search...                                ',
	font=('Segoe', 16),
	compound = 'right',
	anchor = 'w',
	width = 250,
	height = 36,
	fg_color = lgrey,
	hover_color = '#474747',
	background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
	bg_color = '#282828'
		     )
	search_button.place(x=220, y=10)

	# Text Elements - Left Panel

	# Quick Links Text
	quick_links_text = customtkinter.CTkLabel(
	master = app,
	text = 'Quick links',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	quick_links_text.place(x=28, y=20)

	# Categories Text
	categories_text = customtkinter.CTkLabel(
	master = app,
	text = 'Categories',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	categories_text.place(x=28, y=220)

	# Tags Text
	tags_text = customtkinter.CTkLabel(
	master = app,
	text = 'Tags',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	tags_text.place(x=28, y=360)

	# Account Text
	account_text = customtkinter.CTkLabel(
	master = app,
	text = 'Account',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	account_text.place(x=28, y=530)

	# Welcome, Text
	welcome_text = customtkinter.CTkLabel(
	master = app,
	text = 'Welcome,',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	welcome_text.place(x=95, y=635) # 28

	# Username Text
	username_text = customtkinter.CTkLabel(
	master = app,
	text = current_user.get_username(), 
	bg_color = '#1f1f1f',
	font=('Segoe', 15, 'bold'),
	text_color = 'White'
		)
	username_text.place(x=95, y=655) # 28

	# Text Elements - Middle Panel

	# What are we looking at Text
	wawla_text = customtkinter.CTkLabel(
	master = app,
	text = 'All notes',
	bg_color = '#282828',
	font=('Segoe', 22, 'bold'),
	text_color = '#999999'
		)
	wawla_text.place(x=220, y=60)

	# great job so far!

	# Right Panel Stuff

	add_content_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 620,
		bg_color = '#323232',
		fg_color = '#323232',
		border_color = '#1a6eb5',
		border_width = 3
		)
	add_content_screen.place(x=560, y=50)

	# Create New Note... (text)
	create_new_text = customtkinter.CTkLabel(
	master = add_content_screen,
	text = 'Create new note...',
	bg_color = '#323232',
	font=('Segoe', 32, 'bold'),
	text_color = 'white'
		)
	create_new_text.place(x=50, y=50)

	# Create New Text Note Button
	new_text_image = customtkinter.CTkImage(Image.open(current_path + "/gui/text_icon.png"), size=(32, 32))
	new_text_note_button = customtkinter.CTkButton(
	master = add_content_screen,
	command = add_new_text_note,
	image = new_text_image,
	width = 64,
	height = 64,
	text = '',
	compound = 'left',
	#anchor = 'w',
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232',
	font = font
		     )
	new_text_note_button.place(x=75, y=150)

	# Create New Whiteboard Note Button
	new_whiteboards_image = customtkinter.CTkImage(Image.open(current_path + "/gui/whiteboards_icon.png"), size=(32, 32))
	new_whiteboard_note_button = customtkinter.CTkButton(
	master = add_content_screen,
	command = add_new_whiteboard_note,
	image = new_whiteboards_image,
	width = 64,
	height = 64,
	text = '',
	compound = 'left',
	#anchor = 'w',
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232',
	font = font
		     )
	new_whiteboard_note_button.place(x=218, y=150)

	# Create New Recording Note Button
	new_recordings_image = customtkinter.CTkImage(Image.open(current_path + "/gui/recordings_icon.png"), size=(32, 32))
	new_recording_note_button = customtkinter.CTkButton(
	master = add_content_screen,
	command = add_new_recording_note,
	image = new_recordings_image,
	width = 64,
	height = 64,
	text = '',
	compound = 'left',
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232',
	font = font
		     )
	new_recording_note_button.place(x=361, y=150)

	# Text (text)
	text_text = customtkinter.CTkLabel(
	master = add_content_screen,
	text = 'Text',
	bg_color = '#323232',
	font=('Segoe', 16, 'bold'),
	text_color = 'white'
		)
	text_text.place(x=89, y=220)

	# Whiteboard (text)
	whiteboard_text = customtkinter.CTkLabel(
	master = add_content_screen,
	text = 'Whiteboard',
	bg_color = '#323232',
	font=('Segoe', 16, 'bold'),
	text_color = 'white'
		)
	whiteboard_text.place(x=206, y=220)

	# Recording (text)
	recording_text = customtkinter.CTkLabel(
	master = add_content_screen,
	text = 'Recording',
	bg_color = '#323232',
	font = ('Segoe', 16, 'bold'),
	text_color = 'white'
		)
	recording_text.place(x=356, y=220)

# ===============================================================================================

	add_text_note_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		#border_color = '#1a6eb5',
		border_width = 3
		)

	new_note_title_tb = customtkinter.CTkEntry(
		master = add_text_note_screen,
		width = 400,
		height = 30,
		font = ('Segoe', 16, 'bold'),
		placeholder_text = 'Title...',
		border_width = 1,
		fg_color = '#474747'
		)
	new_note_title_tb.place(x=25, y=25)

	favorites_filled_image = customtkinter.CTkImage(Image.open(current_path + "/gui/favorites_filled.png"), size=(32, 32))
	favorites_empty_image = customtkinter.CTkImage(Image.open(current_path + "/gui/favorites_icon.png"), size=(32, 32))

	new_note_favorite_button = customtkinter.CTkButton(
		master = add_text_note_screen,
		width = 32,
		height = 32,
		command = new_note_fav,
		text = "",
		image = favorites_empty_image,
		fg_color = '#323232',
		bg_color = '#323232',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		hover_color = '#323232'
		)
	new_note_favorite_button.place(x=437, y=18)

	new_note_content_tb = customtkinter.CTkTextbox(
		master = add_text_note_screen,
		width = 450,
		height = 420,
		wrap = 'word',
		font = ('Segoe', 16),
		#border_color = '#317dbc',
		border_width = 1,
		fg_color = '#474747'
		)
	new_note_content_tb.place(x=25, y=70)

	new_note_tag_text = customtkinter.CTkLabel(
		master = add_text_note_screen,
		text = 'Tags',
		font = ('Segoe', 14, 'bold')
		)
	new_note_tag_text.place(x=25, y=490)

	# Personal Tag
	note_tag_personal_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = lambda: note_tags_light_up(note_tag_personal_button),
	image = personal_image,
	text = 'Personal',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	note_tag_personal_button.place(x=24, y=520)

	# Work Tag
	note_tag_work_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = lambda: note_tags_light_up(note_tag_work_button),
	image = work_image,
	text = 'Work',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	note_tag_work_button.place(x=139, y=520)

	# School Tag
	note_tag_school_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = lambda: note_tags_light_up(note_tag_school_button),
	image = school_image,
	text = 'School',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	note_tag_school_button.place(x=254, y=520)

	# Other Tag
	note_tag_other_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = lambda: note_tags_light_up(note_tag_other_button),
	image = other_image,
	text = 'Other',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	note_tag_other_button.place(x=369, y=520)

	new_note_cancel_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = new_note_cancel,
	text = 'Cancel',
	font=('Segoe', 16),
	width = 110,
	height = 36,
	fg_color = '#474747',
	hover_color = '#317dbc',
	background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
		     )
	new_note_cancel_button.place(x=250, y=580)

	new_note_submit_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = new_note_submit,
	text = 'Submit',
	font=('Segoe', 16, 'bold'),
	width = 110,
	height = 36,
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
		     )
	new_note_submit_button.place(x=365, y=580)

	text_note_display_screen = customtkinter.CTkFrame(
	master = app,
	width = 480,
	height = 600,
	bg_color = '#323232',
	fg_color = '#323232',
	border_color = '#1a6eb5',
	border_width = 3
	)

	text_note_title_label = customtkinter.CTkLabel(
		master = text_note_display_screen,
		width = 450,
		height = 100,
		text = '',
		font = ('Segoe', 34, 'bold'),
		text_color = '#474747',
		wraplength=480,
		justify = 'left'
		)

	text_note_content_tb = customtkinter.CTkTextbox(
		master = text_note_display_screen,
		width = 480,
		height = 500,
		fg_color = '#323232',
		font = font,
		text_color = 'white',
		wrap = 'word'
		)

# =======================================================================================

	# CONTACTS
	
	add_new_contact_button = customtkinter.CTkButton(
	master = contacts_frame,
	command = add_new_contact_clicked,
	text = '+   Add a new contact',
	font=('Segoe', 16),
	width = 260,
	height = 36,
	fg_color = lgrey,
	hover_color = '#474747',
	background_corner_colors=[grey, grey, grey, grey],
	bg_color = grey		     )
	add_new_contact_button.grid(row=0, column=0, padx=10, pady=(0, 20))

	#=====================================================================

	# New contact addition

	# New Contact Add Screen
	add_contact_screen = customtkinter.CTkFrame(
	master = app,
	width = 500,
	height = 650,
	bg_color = '#323232',
	fg_color = '#323232',
	)

	# Add a New Contact... (text)
	add_a_new_contact_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'Add a new contact...',
	bg_color = '#323232',
	font=('Segoe', 32, 'bold'),
	text_color = 'white'
		)
	add_a_new_contact_text.place(x=20, y=40)

	# Contact Avatar Add Button
	photo_image = customtkinter.CTkImage(Image.open(current_path + "/gui/camera_icon.png"), size=(32, 32))
	contact_avatar_button = customtkinter.CTkButton(
	master = add_contact_screen,
	command = add_avatar_to_contact,
	image = photo_image,
	text = '',
	width = 128,
	height = 128,
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey
		     )
	contact_avatar_button.place(x=20, y=143)

	# Avatar (text)
	avatar_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'AVATAR',
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	avatar_text.place(x=68, y=272)

	# Display Name (text)
	display_name_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'DISPLAY NAME',
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	display_name_text.place(x=170, y=105)

	# Display Name TextBox
	display_name_tb = customtkinter.CTkEntry(
	master = add_contact_screen,
	width = 315,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	display_name_tb.place(x=170, y=130)

	# First Name (text)
	first_name_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'FIRST NAME',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	first_name_text.place(x=170, y=164)

	# First Name TextBox
	first_name_tb = customtkinter.CTkEntry(
	master = add_contact_screen,
	width = 150,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	first_name_tb.place(x=170, y=180)

	# Last Name (text)
	last_name_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'LAST NAME',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	last_name_text.place(x=335, y=164)

	# Last Name TextBox
	last_name_tb = customtkinter.CTkEntry(
	master = add_contact_screen,
	width = 150,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	last_name_tb.place(x=335, y=180)

	# Email (text)
	email_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'EMAIL',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	email_text.place(x=170, y=214)

	# Email TextBox
	email_tb = customtkinter.CTkEntry(
	master = add_contact_screen,
	width = 315,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	email_tb.place(x=170, y=230)

	# Phone # (text)
	phone_text = customtkinter.CTkLabel(
	master = add_contact_screen,
	text = 'PHONE',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	phone_text.place(x=170, y=264)

	# Phone # TextBox
	phone_tb = customtkinter.CTkEntry(
	master = add_contact_screen,
	width = 315,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	phone_tb.place(x=170, y=280)

	new_contact_cancel_button = customtkinter.CTkButton(
	master = add_contact_screen,
	command = new_contact_cancel,
	text = 'Cancel',
	font=('Segoe', 16),
	width = 110,
	height = 36,
	fg_color = '#474747',
	hover_color = '#585858',
	background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
		     )
	new_contact_cancel_button.place(x=245, y=330)

	new_contact_submit_button = customtkinter.CTkButton(
	master = add_contact_screen,
	command = new_contact_submit,
	text = 'Submit',
	font=('Segoe', 16, 'bold'),
	width = 110,
	height = 36,
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
		     )
	new_contact_submit_button.place(x=375, y=330)


# =========	               CONTACT DISPLAY                  ==============

	contact_display_screen = customtkinter.CTkFrame(
	master = app,
	width = 480,
	height = 600,
	bg_color = '#323232',
	fg_color = '#323232'
	)

	contact_display_name_label = customtkinter.CTkLabel(
		master = contact_display_screen,
		text = '',
		font = ('Segoe', 34, 'bold'),
		text_color = 'white'
	)
	
	contact_display_avatar_button = customtkinter.CTkButton(
	master = contact_display_screen,
	image = default_avatar_display_image,
	text = '',
	width = 128,
	height = 128,
	hover_color = lgrey,
	fg_color = lgrey,
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey
	)

	# First Name (text)
	contact_display_first_name_dec = customtkinter.CTkLabel(
	master = contact_display_screen,
	text = 'FIRST NAME',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = '#9b9b9b'
		)
	contact_display_first_name_dec.place(x=170, y=120)

	# First Name TextBox
	contact_display_first_name = customtkinter.CTkLabel(
	master = contact_display_screen,
	bg_color = '#323232',
	font=('Segoe', 16, 'bold'),
	text_color = 'white',
	text = ':)'
			)
	contact_display_first_name.place(x=170, y=136)

	# Last Name (text)
	contact_display_last_name_dec = customtkinter.CTkLabel(
	master = contact_display_screen,
	text = 'LAST NAME',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = '#9b9b9b'
		)
	contact_display_last_name_dec.place(x=335, y=120)

	# Last Name TextBox
	contact_display_last_name = customtkinter.CTkLabel(
	master = contact_display_screen,
	bg_color = '#323232',
	font=('Segoe', 16, 'bold'),
	text_color = 'white',
	text = ':)'
			)
	contact_display_last_name.place(x=335, y=136)

	# Email (text)
	contact_display_email_dec = customtkinter.CTkLabel(
	master = contact_display_screen,
	text = 'EMAIL',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = '#9b9b9b'
		)
	contact_display_email_dec.place(x=170, y=170)

	# Email TextBox
	contact_display_email = customtkinter.CTkLabel(
	master = contact_display_screen,
	bg_color = '#323232',
	font=('Segoe', 16, 'bold'),
	text_color = 'white',
	text = ':)'
			)
	contact_display_email.place(x=170, y=186)

	# Phone # (text)
	contact_display_phone_dec = customtkinter.CTkLabel(
	master = contact_display_screen,
	text = 'PHONE',
	height = 10,
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = '#9b9b9b'
		)
	contact_display_phone_dec.place(x=170, y=220)

	# Phone # TextBox
	contact_display_phone = customtkinter.CTkLabel(
	master = contact_display_screen,
	bg_color = '#323232',
	font=('Segoe', 16, 'bold'),
	text_color = 'white',
	text = ':)'
			)
	contact_display_phone.place(x=170, y=236)


# =============================== WHITEBOARDS =================================

# ========================= CREATE NEW WHITEBOARD =============================

	add_whiteboard_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3,
		border_color = bluey
		)

	global is_drawing
	global prev_x
	global prev_y
	is_drawing = False
	prev_x, prev_y = 0, 0 
	drawing_color = "black"
	line_width = 5

	def start_drawing(event):
	    global is_drawing, prev_x, prev_y
	    is_drawing = True
	    prev_x, prev_y = event.x, event.y

	def draw(event):
	    global is_drawing, prev_x, prev_y
	    if is_drawing:
	        current_x, current_y = event.x, event.y
	        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tkinter.ROUND, smooth=True)
	        prev_x, prev_y = current_x, current_y

	def stop_drawing(event):
	    global is_drawing
	    is_drawing = False

	canvas = tkinter.Canvas(add_whiteboard_screen, bg="white")
	canvas.place(x=4, y=90)
	canvas.config(width=612, height=560)

	canvas.bind("<Button-1>", start_drawing)
	canvas.bind("<B1-Motion>", draw)
	canvas.bind("<ButtonRelease-1>", stop_drawing)

	save_whiteboard_button = customtkinter.CTkButton(
		master = add_whiteboard_screen,
		command = save_new_whiteboard,
		text = 'Save',
		font=('Segoe', 16, 'bold'),
		width = 110,
		height = 36,
		fg_color = '#1a6eb5',
		hover_color = '#317dbc',
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
		     )
	save_whiteboard_button.place(x=365, y=600)

	cancel_new_whiteboard_button = customtkinter.CTkButton(
		master = add_whiteboard_screen,
		command = cancel_new_whiteboard,
		text = 'Cancel',
		font=('Segoe', 16),
		width = 110,
		height = 36,
		fg_color = '#474747',
		hover_color = '#317dbc',
		background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
		bg_color = lgrey
		     )
	cancel_new_whiteboard_button.place(x=250, y=600)

	def clear_canvas():
		canvas.delete("all")

	clear_canvas_button = customtkinter.CTkButton(
	master = add_whiteboard_screen,
	command = clear_canvas,
	text = 'Clear canvas',
	font=('Segoe', 16),
	width = 110,
	height = 36,
	fg_color = '#474747',
	hover_color = '#317dbc',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey
	     )
	clear_canvas_button.place(x=20, y=600)

	whiteboard_title_tb = customtkinter.CTkEntry(
		master = add_whiteboard_screen,
		placeholder_text = 'Title...',
		font = ('Segoe', 16, 'bold'),
		width = 400,
		height = 30,
		border_width = 1,
		fg_color = '#474747'
		)
	whiteboard_title_tb.place(x=25, y=25)

	new_whiteboard_favorite_button = customtkinter.CTkButton(
		master = add_whiteboard_screen,
		width = 32,
		height = 32,
		command = new_whiteboard_fav,
		text = "",
		image = favorites_empty_image,
		fg_color = lgrey,
		bg_color = lgrey,
		background_corner_colors = [lgrey, lgrey, lgrey, lgrey],
		hover_color = lgrey
		)
	new_whiteboard_favorite_button.place(x=437, y=18)

	new_whiteboard_tag_text = customtkinter.CTkLabel(
		master = add_whiteboard_screen,
		text = 'Tags',
		font = ('Segoe', 14, 'bold')
		)
	new_whiteboard_tag_text.place(x=25, y=530)

	# Personal Tag
	whiteboard_tag_personal_button = customtkinter.CTkButton(
	master = add_whiteboard_screen,
	command = lambda: whiteboard_tags_light_up(whiteboard_tag_personal_button),
	image = personal_image,
	text = 'Personal',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	whiteboard_tag_personal_button.place(x=24, y=560)

	# Work Tag
	whiteboard_tag_work_button = customtkinter.CTkButton(
	master = add_whiteboard_screen,
	command = lambda: whiteboard_tags_light_up(whiteboard_tag_work_button),
	image = work_image,
	text = 'Work',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	whiteboard_tag_work_button.place(x=139, y=560)

	# School Tag
	whiteboard_tag_school_button = customtkinter.CTkButton(
	master = add_whiteboard_screen,
	command = lambda: whiteboard_tags_light_up(whiteboard_tag_school_button),
	image = school_image,
	text = 'School',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	whiteboard_tag_school_button.place(x=254, y=560)

	# Other Tag
	whiteboard_tag_other_button = customtkinter.CTkButton(
	master = add_whiteboard_screen,
	command = lambda: whiteboard_tags_light_up(whiteboard_tag_other_button),
	image = other_image,
	text = 'Other',
	width = 110,
	height = 30,
	compound = 'left',
	anchor = 'w',
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	font = font
		     )
	whiteboard_tag_other_button.place(x=369, y=560)

	whiteboard_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 640,
		bg_color = '#323232',
		fg_color = '#323232',
		border_color = '#1a6eb5',
		border_width = 3
	)

	whiteboard_title_label = customtkinter.CTkLabel(
		master = whiteboard_display_screen,
		width = 450,
		height = 30,
		text = '',
		font = ('Segoe', 24, 'bold'),
		text_color = '#474747',
		wraplength=480,
		justify = 'left'
		)










# ==================================== REMINDERS ==========================================

	add_reminder_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3,
		border_color = bluey
		)

	add_new_reminder_button = customtkinter.CTkButton(
		master = reminders_frame,
		command = add_new_reminder_clicked,
		text = '+   Add a new reminder',
		font=('Segoe', 16),
		width = 260,
		height = 36,
		fg_color = lgrey,
		hover_color = '#474747',
		background_corner_colors=[grey, grey, grey, grey],
		bg_color = grey
		)
	add_new_reminder_button.grid(row=0, column=0, padx=10, pady=(0, 20))

# ====================== Create screen =================================

	new_reminder_title_text = customtkinter.CTkLabel(
		master = add_reminder_screen,
		text = 'Title:',
		font = ('Segoe', 24, 'bold')
		)
	new_reminder_title_text.place(x=25, y=25)

	new_reminder_title_tb = customtkinter.CTkEntry(
		master = add_reminder_screen,
		width = 400,
		height = 30,
		font = font,
		border_width = 1,
		#border_color = '#317dbc',
		fg_color = '#474747'
		)
	new_reminder_title_tb.place(x=25, y=60)

	new_reminder_favorite_button = customtkinter.CTkButton(
		master = add_reminder_screen,
		width = 32,
		height = 32,
		command = new_reminder_fav,
		text = "",
		image = favorites_empty_image,
		fg_color = '#323232',
		bg_color = '#323232',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		hover_color = '#323232'
		)
	new_reminder_favorite_button.place(x=437, y=54)

	new_reminder_content_text = customtkinter.CTkLabel(
		master = add_reminder_screen,
		text = 'Description:',
		font = ('Segoe', 16, 'bold')
		)
	new_reminder_content_text.place(x=25, y=90)

	new_reminder_content_tb = customtkinter.CTkTextbox(
		master = add_reminder_screen,
		width = 450,
		height = 200,
		wrap = 'word',
		font = font,
		#border_color = '#317dbc',
		border_width = 1,
		fg_color = '#474747'
		)
	new_reminder_content_tb.place(x=25, y=120)

	new_reminder_date_text = customtkinter.CTkLabel(
		master = add_reminder_screen,
		text = 'Due date:',
		font = ('Segoe', 16, 'bold')
		)
	new_reminder_date_text.place(x=25, y=325)

	cal = tkcalendar.DateEntry(add_reminder_screen, width=12, background='#1a6eb5', foreground='#323232',
		borderwidth=2, year=2024, state='readonly')
	cal.place(x=32,y=436)

	dt = cal.get_date()
	str_dt = dt.strftime("%Y-%m-%d")

	new_reminder_cancel_button = customtkinter.CTkButton(
		master = add_reminder_screen,
		command = new_reminder_cancel,
		text = 'Cancel',
		font=('Segoe', 16),
		width = 110,
		height = 36,
		fg_color = '#474747',
		hover_color = '#317dbc',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
		)
	new_reminder_cancel_button.place(x=240, y=335)

	new_reminder_submit_button = customtkinter.CTkButton(
		master = add_reminder_screen,
		command = new_reminder_submit,
		text = 'Submit',
		font=('Segoe', 16, 'bold'),
		width = 110,
		height = 36,
		fg_color = '#1a6eb5',
		hover_color = '#317dbc',
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
		)
	new_reminder_submit_button.place(x=365, y=335)


	





















	# List of All Buttons
	button_list = [all_notes_button, reminders_button, favorites_button, statistics_button,
	text_button, recordings_button, whiteboards_button, contacts_button, history_button, settings_button,
	personal_button, work_button, school_button, other_button]

	# List of All Frames
	frame_list = [all_notes_frame, reminders_frame, contacts_frame, favorites_frame, statistics_frame,
	only_text_notes_frame, history_frame, settings_frame, only_work_frame, only_personal_frame, only_recordings_frame,
	only_whiteboards_frame, only_school_frame, only_other_frame]

	# List of ShowScreens
	screen_list = [add_content_screen, add_text_note_screen, text_note_display_screen, add_contact_screen,
	contact_display_screen, add_whiteboard_screen, add_reminder_screen, whiteboard_display_screen]

	#run app
	app.mainloop()

run_login_page()
#run_app()