# Import
import customtkinter
import os
from PIL import Image, ImageTk
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

global buttons
buttons = []
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
			user_id = peko_database.get_uid(login_cred)
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
		for elem in text_notes:

			text_note = customtkinter.CTkButton(
				master = only_text_notes_frame,
				command = lambda x=elem[0]: text_note_display(x),
				image = text_image,
				width = 250,
				height = 50,
				text = f'{elem[0]}: {elem[2]}',
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = '#1a6eb5',
				hover_color = '#323232',
				border_width = 1,
				)
			text_note.grid(row=row, column=0, padx=10, pady=(0, 20))
			row += 1
			buttons.append(text_note)


	def text_note_display(note_id):

		switch_screen(text_note_display_screen)
		text_note_title_label.configure(text = peko_database.get_note_title(note_id))
		text_note_content_tb.configure(state = 'normal')
		text_note_content_tb.delete("0.0", "end")
		text_note_content_tb.insert("0.0", peko_database.get_note_content(note_id))
		text_note_content_tb.configure(state = 'disabled')

		text_note_title_label.grid(row=0, column=0, padx=10, pady=(0, 20))
		text_note_content_tb.grid(row=1, column=0, padx=10, pady=(0, 20))
		

	def show_all_whiteboards():
		# self-explanatory
		lights_out(whiteboards_button)
		whiteboards_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Whiteboards')
		update_wawla_text()
		print("test: whiteboards")


	def show_all_recordings():
		# self-explanatory
		lights_out(recordings_button)
		recordings_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Recordings')
		update_wawla_text()
		print("test: recordings")


	def show_all_contacts():
		# self-explanatory
		lights_out(contacts_button)
		contacts_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Contacts')
		switch_frame(contacts_frame)
		update_wawla_text()
		print("test: contacts")


	def show_trash():
		# self-explanatory
		lights_out(trash_button)
		trash_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Trash')
		update_wawla_text()
		print("test: trash")


	def show_settings():
		# self-explanatory
		lights_out(settings_button)
		settings_button.configure(fg_color="#1a6eb5", hover_color = '#317dbc')
		set_wawla('Settings')
		update_wawla_text()
		print("test: settings")


	def show_add_content_screen():
		switch_screen(add_content_screen)
		print('test: add some note.')


	def add_new_text_note():
		switch_screen(add_text_note_screen)


	def	add_new_whiteboard_note():
		print(current_user.get_text_notes())


	def add_new_recording_note():
		pass


	def new_note_cancel():
		switch_screen(add_content_screen)


	def new_note_submit():
		title = new_note_title_tb.get().strip()
		favorite = check_if_fav_button()
		content = new_note_content_tb.get('0.0', 'end').strip()

		tag_name = new_note_tag_combobox.get().strip()
		peko_database.insert_tag(current_user.user_id, tag_name)

		tag_id = peko_database.get_tag_id(tag_name)

		peko_database.insert_text_note(current_user.user_id, title, content, favorite, tag_id)
		switch_screen(add_content_screen)


	def check_if_fav_button():
		if new_note_favorite_button.cget("image") == favorites_empty_image:
			return False
		return True


	def new_note_fav():
		if new_note_favorite_button.cget("image") == favorites_empty_image:
			new_note_favorite_button.configure(image = favorites_filled_image)
		else:
			new_note_favorite_button.configure(image = favorites_empty_image)


	def add_new_contact_clicked():
		switch_screen(add_contact_screen)


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
	whiteboards_image = customtkinter.CTkImage(Image.open(current_path + "/gui/whiteboards_icon.png"), size=(20, 20))
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

	# Trash Button
	trash_image = customtkinter.CTkImage(Image.open(current_path + "/gui/trash_icon.png"), size=(20, 20))
	trash_button = customtkinter.CTkButton(
	master = app,
	command = show_trash,
	image = trash_image,
	text = 'Trash',
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
	trash_button.place(x=20, y=500)

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
	settings_button.place(x=20, y=530)

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

	# Welcome, Text
	welcome_text = customtkinter.CTkLabel(
	master = app,
	text = 'Welcome,',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	welcome_text.place(x=28, y=640)

	# Username Text
	username_text = customtkinter.CTkLabel(
	master = app,
	text = current_user.get_username(), 
	bg_color = '#1f1f1f',
	font=('Segoe', 15, 'bold'),
	text_color = 'White'
		)
	username_text.place(x=28, y=660)

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
	font=('Segoe', 16, 'bold'),
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

	new_note_title_text = customtkinter.CTkLabel(
		master = add_text_note_screen,
		text = 'Title:',
		font = ('Segoe', 24, 'bold')
		)
	new_note_title_text.place(x=25, y=25)

	new_note_title_tb = customtkinter.CTkEntry(
		master = add_text_note_screen,
		width = 400,
		height = 30,
		font = font,
		border_width = 1,
		#border_color = '#317dbc',
		fg_color = '#474747'

		)
	new_note_title_tb.place(x=25, y=60)

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
	new_note_favorite_button.place(x=437, y=54)

	new_note_content_text = customtkinter.CTkLabel(
		master = add_text_note_screen,
		text = 'Content:',
		font = ('Segoe', 16, 'bold')
		)
	new_note_content_text.place(x=25, y=90)

	new_note_content_tb = customtkinter.CTkTextbox(
		master = add_text_note_screen,
		width = 450,
		height = 420,
		wrap = 'word',
		font = font,
		#border_color = '#317dbc',
		border_width = 1,
		fg_color = '#474747'
		)
	new_note_content_tb.place(x=25, y=120)

	new_note_tag_text = customtkinter.CTkLabel(
		master = add_text_note_screen,
		text = 'Tag:',
		font = ('Segoe', 16, 'bold')
		)
	new_note_tag_text.place(x=25, y=540)

	new_note_tag_combobox = customtkinter.CTkComboBox(
		master = add_text_note_screen,
		width = 160,
		font = font,
		dropdown_font = font,
		values = ['I', 'am', 'testing', 'stuff'],
		border_width = 1,
		#border_color = '#317dbc',
		fg_color = '#474747',
		button_color = '#1a6eb5',
		button_hover_color = '#317dbc',
		dropdown_fg_color = '#474747',
		dropdown_hover_color = '#317dbc'
		)
	new_note_tag_combobox.place(x=25, y=570)

	new_note_cancel_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = new_note_cancel,
	text = 'Cancel',
	font=('Segoe', 22),
	width = 110,
	height = 36,
	fg_color = '#474747',
	hover_color = '#317dbc',
	background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
		     )
	new_note_cancel_button.place(x=225, y=570)

	new_note_submit_button = customtkinter.CTkButton(
	master = add_text_note_screen,
	command = new_note_submit,
	text = 'Submit',
	font=('Segoe', 22, 'bold'),
	width = 110,
	height = 36,
	fg_color = '#1a6eb5',
	hover_color = '#317dbc',
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
		     )
	new_note_submit_button.place(x=365, y=570)


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
	create_new_text.place(x=50, y=50)

	# TEXT


	# display_name_tb
	display_name_tb = customtkinter.CTkEntry(
	master = add_contact_screen,
	width = 300,
	height = 30,
	fg_color = '#282828',
	border_color = '#1a6eb5',
	border_width = 3,
	placeholder_text = ''
			)
	display_name_tb.place(x=95, y=182)





















	# List of All Buttons
	button_list = [all_notes_button, reminders_button, favorites_button, statistics_button,
	text_button, recordings_button, whiteboards_button, contacts_button, trash_button, settings_button]

	# List of All Frames
	frame_list = [all_notes_frame, reminders_frame, contacts_frame, favorites_frame, statistics_frame,
	 only_text_notes_frame]

	# List of ShowScreens
	screen_list = [add_content_screen, add_text_note_screen, text_note_display_screen, add_contact_screen]

	#run app
	app.mainloop()

run_login_page()
#run_app()