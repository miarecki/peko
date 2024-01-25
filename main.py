# Import
import tkinter
from tkinter import colorchooser
import tkcalendar
import customtkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import sys
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import pyaudio
import wave
import threading 
import webbrowser
from pydub import AudioSegment
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import datetime
from collections import defaultdict
import peko_database
import encryption_mech
from user import User

# colors:
dgrey = '#1f1f1f'
grey = '#282828'
lgrey = '#323232'
bluey = '#1a6eb5'
bluehover = '#317dbc'

global avatar_file_path
avatar_file_path = ''
is_stopped = threading.Event()

search_window = None
sr = []

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

		valid = encryption_mech.log_in(login_cred, real_pass)
		
		if valid == 'Success!':
			error_text_label.configure(text = valid, text_color = 'green')
			user_id = peko_database.get_uid(login_cred)
			global current_user
			current_user = User(user_id)
			login_page.destroy() 
			run_app()
		else:
			error_text_label.configure(text = valid, text_color = 'red')

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
			error_text_label.configure(text = valid, text_color = 'green')
			user_id = peko_database.get_uid(acc_name_cred)
			global current_user
			current_user = User(user_id)
			login_page.destroy()
			run_app()
		else:
			error_text_label.configure(text = valid, text_color = 'red')

	def open_github_page():
		webbrowser.open('https://github.com/miarecki')

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

	# Error Text
	error_text_label = customtkinter.CTkLabel(
		master = login_page,
		text = '',
		bg_color = dgrey,
		font=('Segoe', 13, 'bold'),
		text_color = 'red',
		width = 320,
		height = 20
		)
	error_text_label.place(x=160, y=395)

	# GitHub Button 
	github_image = customtkinter.CTkImage(Image.open(current_path + '/gui/github_icon.png'), size=(32, 32))
	github_button = customtkinter.CTkButton(
		master = login_page,
		command = open_github_page,
		image = github_image,
		text = '',
		width = 32,
		height = 32,
		hover_color = bluehover,
		corner_radius = 0,
		border_width = 0,
		border_spacing = 0,
		fg_color = bluey
			 )
	github_button.place(x=592, y=435)

	# Run
	login_page.mainloop()

# MAIN APP

def run_app():

	# colors:  left #1f1f1f \  middle  #282828 \ right #323232
	# colors:

	def get_hover_color(hex_color):
		#  hex to RGB
		hex_color = hex_color.lstrip('#')
		r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

		r = int(r + (255 - r) * .1)
		g = int(g + (255 - g) * .1)
		b = int(b + (255 - b) * .1)

		# back to hex
		return f"#{r:02x}{g:02x}{b:02x}"

	dgrey = '#1f1f1f'
	grey = '#282828'
	lgrey = '#323232'

	current_path = os.path.dirname(os.path.realpath(__file__))

	user_settings = current_user.get_settings()

	current_user_display_name = user_settings[2]

	current_user_avatar_path = user_settings[3]
	try:
		current_user_avatar64 = customtkinter.CTkImage(Image.open(current_path + current_user_avatar_path), size=(64, 64))
	except Exception as e:
		current_user_avatar64 = customtkinter.CTkImage(Image.open(current_user_avatar_path), size=(64, 64))

	user_button_color = user_settings[4]
	user_button_color_hover = get_hover_color(user_button_color)

	# System Settings
	default_avatar_display_image = customtkinter.CTkImage(Image.open(current_path + '/gui/avatar_default.png'), size=(128, 128))
	font = ('Segoe', 15)

	is_recording = False
	frames = []
	is_playing = False
	stream = None
	audio_thread = None

	last_text_note_id = 1

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

	def forget_buttons(frame):
		for widget in frame.winfo_children():
			widget.destroy()

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
				frame.grid_forget()
				frame.place_forget()

	# showscreen switcher
	def switch_screen(screen_name):
		for screen in screen_list:
			if screen_name != screen:
				screen_name.place(x=560, y=50)
				screen.place_forget()

	# short the title
	def short(string):
		if len(string) > 22:
			string = string[:22] + '...'
		return string

	# Functions
	def show_all_notes():
		# self-explanatory
		all_notes_frame.place(x=220, y=100)
		lights_out(all_notes_button)
		all_notes_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('All notes')
		update_wawla_text()
		switch_frame(all_notes_frame)
		forget_buttons(all_notes_frame)

		all_notes = current_user.get_all_notes()

		row = 0
		buttons = []
		newline = '\n'

		for elem in all_notes:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: recording_display(x)

			note_button = customtkinter.CTkButton(
				master= all_notes_frame,
				command=note_display_command,
				image=note_image,
				width=250,
				height=50,
				font = font,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)

	def show_all_reminders():
		# self-explanatory
		lights_out(reminders_button)
		reminders_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Reminders')
		update_wawla_text()
		switch_frame(reminders_frame)
		forget_buttons(reminders_frame)

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

		def get_button_color(current_date, due_date):
			delta = (due_date - current_date).days

			if delta < 0:  # Past due date
				return "#8B0000"  # Dark red
			elif delta <= 7:  # A week or less
				# Gradually turn red as the due date approaches
				red = 255
				green = round(255 * (delta / 7))
				return f"#{red:02x}{green:02x}00"
			else:
				return "#008000"  # Nice green

		reminders = current_user.get_reminders() 

		row = 1
		buttons = []
		newline = '\n'
		current_date = datetime.datetime.now().date()

		for elem in reminders:
			due_date = elem[5].date()  # Assuming elem[5] is a datetime object
			button_color = get_button_color(current_date, due_date)

			reminder = customtkinter.CTkButton(
				master = reminders_frame,
				command = lambda x=elem[0]: reminder_display(x),
				image = reminders_image,
				width = 250,
				height = 50,
				text = f"{short(elem[2])} {newline} {due_date.strftime('%d-%m-%Y')}",
				font = font,
				anchor = 'w',
				fg_color = button_color,
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = user_button_color,
				hover_color = get_hover_color(button_color),
				border_width=1
				)
			reminder.grid(row=row, column=0, padx=10, pady=(0, 20))
			row += 1
			buttons.append(reminder)

	def reminder_display(reminder_id):

		reminder = peko_database.get_reminder(current_user.user_id, reminder_id)
		switch_screen(reminder_display_screen)

		reminder_display_title_label.configure(text = reminder[2])
		reminder_display_description_label.configure(text = reminder[3])
		reminder_display_due_date_label.configure(text = reminder[5].strftime('%d-%m-%Y'))

		reminder_display_title_label.place(x=20,y=50)
		reminder_display_description_label.place(x=20,y=80)
		reminder_display_due_date_label.place(x=20,y=120)

		def delete_reminder_forever():
			peko_database.delete_reminder(current_user.user_id, reminder_id)
			show_all_reminders()
			switch_screen(add_content_screen)

		reminder_delete_button = customtkinter.CTkButton(
			master = reminder_display_screen,
			command = delete_reminder_forever,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		reminder_delete_button.place(x=335, y=280)

	def show_all_favorites():
		# self-explanatory
		lights_out(favorites_button)
		set_wawla('Favorites')
		update_wawla_text()
		switch_frame(favorites_frame)
		forget_buttons(favorites_frame)
		favorites_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)

		all_favorites = current_user.get_all_favorites()

		row = 0
		buttons = []
		newline = '\n'

		for elem in all_favorites:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: recording_display(x)

			note_button = customtkinter.CTkButton(
				master= favorites_frame,
				command=note_display_command,
				image=note_image,
				font = font,
				width=250,
				height=50,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)

	def stats_plot(data):

		# Create a Matplotlib figure
		fig, ax = plt.subplots(figsize=(2, 2), tight_layout=True)
		fig.patch.set_facecolor(lgrey)
		ax.set_xticks([])  # Remove x-axis ticks
		ax.set_facecolor(lgrey)  # Grey background
		ax.yaxis.set_visible(False)  # Hide y-axis
		ax.set_xticklabels([])  # Hide x-axis labels
		ax.spines['right'].set_visible(False)  # Hide right border
		ax.spines['top'].set_visible(False)  # Hide top border
		ax.spines['left'].set_visible(False)  # Hide left border
		ax.spines['bottom'].set_color('white')  # White bottom border

		# Data for the bar plot
		note_types = ['Notes', 'Whiteboards', 'Recordings']
		note_counts = data

		# Bar plot
		bars = ax.bar(note_types, note_counts, color = user_button_color)

		# Display the count above each bar with bold white text
		for bar in bars:
			height = bar.get_height()
			ax.annotate(
				f'{height}',
				xy=(bar.get_x() + bar.get_width() / 2, height),
				xytext=(0, 3),  # 3 points vertical offset
				textcoords="offset points",
				ha='center', va='bottom',
				fontsize=12, fontweight='bold', color='white'
			)

		return fig

	def show_statistics():
		# self-explanatory
		lights_out(statistics_button)
		statistics_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		switch_screen(statistics_display_screen)

		data = current_user.get_stats()

		stats_plot_image = FigureCanvasTkAgg(stats_plot(data[2:5]), master = statistics_display_screen)
		actual_plot = stats_plot_image.get_tk_widget()
		actual_plot.place(x=400, y=30)

		data = [x if x is not None else 0 for x in list(data)]

		statistics_display_screen_total_label.configure(text = 'Total number of notes:' + '  ' + str(data[1]))

		statistics_display_screen_total_text_label.configure(text = 'Text notes:' + '      ' + str(data[2]))
		statistics_display_screen_total_whiteboard_label.configure(text = 'Whiteboards:' + '  ' + str(data[3]))
		statistics_display_screen_total_recording_label.configure(text = 'Recordings:' + '    ' + str(data[4]))

		statistics_display_screen_shortest_text_label.configure(text = 'Shortest text note:' + '  ' + str(data[5]) + ' characters')
		statistics_display_screen_longest_text_label.configure(text = 'Longest text note:' + '  ' + str(data[6]) + ' characters')
		statistics_display_screen_average_text_label.configure(text = 'Average length:' + '      ' + str(round(data[7],2)) + ' characters')

		statistics_display_screen_shortest_rec_label.configure(text = 'Shortest recording:' + '  ' + str(data[8]) + ' seconds')
		statistics_display_screen_longest_rec_label.configure(text = 'Longest recording:' + '   ' + str(data[9]) + ' seconds')
		statistics_display_screen_average_rec_label.configure(text = 'Average length:' + '         ' + str(round(data[10],2)) + ' seconds')

		statistics_display_screen_total_reminder_label.configure(text = 'Total number of reminders:' + '  ' + str(data[11]))

		statistics_display_screen_total_contact_label.configure(text = 'Total number of contacts:' + '  ' + str(data[12]))

	def show_all_text():
		# self-explanatory
		lights_out(text_button)
		text_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Text notes')
		switch_frame(only_text_notes_frame)
		forget_buttons(only_text_notes_frame)
		update_wawla_text()

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
				font = font,
				text = f"{short(elem[2])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = user_button_color,
				hover_color = '#323232',
				border_width = 1,
				)
			text_note.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(text_note)

	def display_text_note_favorite():
		if text_note_display_favorite_button.cget("image") == favorites_filled_image:
			text_note_display_favorite_button.configure(image = favorites_empty_image)
		else:
			text_note_display_favorite_button.configure(image = favorites_filled_image)

	def check_if_note_fav(status):
		if status:
			text_note_display_favorite_button.configure(image = favorites_filled_image)
		else:
			text_note_display_favorite_button.configure(image = favorites_empty_image)

	def note_display_is_fav():
		return text_note_display_favorite_button.cget("image") == favorites_filled_image		

	def light_up_text_note_tags(tags):
		if tags is None:
			return
		if 'Personal' in tags:
			text_note_display_tag_personal_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'School' in tags:
			text_note_display_tag_school_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'Work' in tags:
			text_note_display_tag_work_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'Other' in tags:
			text_note_display_tag_other_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)

	def display_note_tags():
		tags = []
		if text_note_display_tag_personal_button.cget('fg_color') == user_button_color:
			tags.append('Personal')
		if text_note_display_tag_work_button.cget('fg_color') == user_button_color:
			tags.append('Work')
		if text_note_display_tag_school_button.cget('fg_color') == user_button_color:
			tags.append('School')
		if text_note_display_tag_other_button.cget('fg_color') == user_button_color:
			tags.append('Other')
		return tags

	def text_note_display(note_id):

		text_note_display_tag_personal_button.configure(fg_color = grey, hover_color = '#474747')
		text_note_display_tag_school_button.configure(fg_color = grey, hover_color = '#474747')
		text_note_display_tag_work_button.configure(fg_color = grey, hover_color = '#474747')
		text_note_display_tag_other_button.configure(fg_color = grey, hover_color = '#474747')

		note = peko_database.get_text_note(current_user.user_id, note_id)
		tags = [item[0] for item in peko_database.get_text_note_tags(note_id)]

		switch_screen(text_note_display_screen)
		text_note_display_title_tb.delete(0, "end")
		text_note_display_title_tb.insert(0, note[2])
		text_note_display_content_tb.delete("0.0", "end")
		text_note_display_content_tb.insert("0.0", note[3])
		check_if_note_fav(note[6])
		light_up_text_note_tags(tags)
		text_note_display_title_tb.place(x=20,y=20)
		text_note_display_content_tb.place(x=20, y=60)

		def edit_note_submit():
			new_tags = display_note_tags()
			peko_database.edit_note_submit(current_user.user_id,
			note_id,
			text_note_display_title_tb.get(),
			text_note_display_content_tb.get("0.0", "end"),
			note_display_is_fav(),
			display_note_tags()
			)
			switch_screen(add_content_screen)
			show_all_notes()

		text_note_display_submit_button = customtkinter.CTkButton(
			master = text_note_display_screen,
			command = edit_note_submit,
			text = 'Submit',
			font=('Segoe', 16, 'bold'),
			width = 110,
			height = 36,
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		text_note_display_submit_button.place(x=365, y=580)

		def edit_note_m2t():
			peko_database.note_m2t(current_user.user_id, note_id)
			switch_frame(all_notes_frame)
			show_all_notes()
			switch_screen(add_content_screen)

		trash_image = customtkinter.CTkImage(Image.open(current_path + "/gui/trash_icon.png"), size=(20, 20))
		text_note_display_trash_button = customtkinter.CTkButton(
			master = text_note_display_screen,
			command = edit_note_m2t,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		text_note_display_trash_button.place(x=25, y=580)	
	
	def show_all_whiteboards():
		# self-explanatory
		lights_out(whiteboards_button)
		whiteboards_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Whiteboards')
		switch_frame(only_whiteboards_frame)
		forget_buttons(only_whiteboards_frame)
		update_wawla_text()

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
				font = font,
				height = 50,
				text = f"{short(elem[2])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = user_button_color,
				hover_color = '#323232',
				border_width = 1,
				)
			whiteboard.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(whiteboard)

	def whiteboard_display_tags_light_up(tags):
		if tags is None:
			return
		if 'Personal' in tags:
			whiteboard_display_screen_tag_personal_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'School' in tags:
			whiteboard_display_screen_tag_school_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'Work' in tags:
			whiteboard_display_screen_tag_work_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'Other' in tags:
			whiteboard_display_screen_tag_other_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)

	def display_whiteboard_tags():
		tags = []
		if whiteboard_display_screen_tag_personal_button.cget('fg_color') == user_button_color:
			tags.append('Personal')
		if whiteboard_display_screen_tag_work_button.cget('fg_color') == user_button_color:
			tags.append('Work')
		if whiteboard_display_screen_tag_school_button.cget('fg_color') == user_button_color:
			tags.append('School')
		if whiteboard_display_screen_tag_other_button.cget('fg_color') == user_button_color:
			tags.append('Other')
		return tags

	def display_whiteboard_favorite():
		if whiteboard_display_favorite_button.cget("image") == favorites_filled_image:
			whiteboard_display_favorite_button.configure(image = favorites_empty_image)
		else:
			whiteboard_display_favorite_button.configure(image = favorites_filled_image)

	def check_if_whiteboard_fav(status):
		if status:
			whiteboard_display_favorite_button.configure(image = favorites_filled_image)
		else:
			whiteboard_display_favorite_button.configure(image = favorites_empty_image)

	def whiteboard_display_is_fav():
		return whiteboard_display_favorite_button.cget("image") == favorites_filled_image

	def whiteboard_display(whiteboard_id):

		whiteboard_display_screen_tag_personal_button.configure(fg_color = grey, hover_color = '#474747')
		whiteboard_display_screen_tag_school_button.configure(fg_color = grey, hover_color = '#474747')
		whiteboard_display_screen_tag_work_button.configure(fg_color = grey, hover_color = '#474747')
		whiteboard_display_screen_tag_other_button.configure(fg_color = grey, hover_color = '#474747')

		whiteboard = peko_database.get_whiteboard(current_user.user_id, whiteboard_id)

		switch_screen(whiteboard_display_screen)

		whiteboard_display_title_tb.delete(0, "end")
		whiteboard_display_title_tb.insert(0, whiteboard[2])
		whiteboard_display_title_tb.place(x=20, y=20)
		img = Image.open(whiteboard[3])
		img_photo = ImageTk.PhotoImage(img)

		label = tkinter.Label(whiteboard_display_screen, image=img_photo)
		label.image = img_photo
		label.place(x=0, y=80)
		tags = [item[0] for item in peko_database.get_whiteboard_tags(whiteboard_id)]
		whiteboard_display_tags_light_up(tags)
		check_if_whiteboard_fav(whiteboard[6])

		def edit_whiteboard_submit():

			peko_database.edit_whiteboard_submit(current_user.user_id, 
			whiteboard_id,
			whiteboard_display_title_tb.get(),
			whiteboard_display_is_fav(), 
			display_whiteboard_tags() 
			)
			switch_screen(add_content_screen)
			switch_frame(all_notes_frame)
			show_all_notes()

		whiteboard_display_submit_button = customtkinter.CTkButton(
			master = whiteboard_display_screen,
			command = edit_whiteboard_submit,
			text = 'Submit',
			font=('Segoe', 16, 'bold'),
			width = 110,
			height = 36,
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		whiteboard_display_submit_button.place(x=365, y=600)

		def edit_whiteboard_m2t():

			peko_database.whiteboard_m2t(current_user.user_id, whiteboard_id)
			switch_frame(all_notes_frame)
			show_all_notes()
			switch_screen(add_content_screen)

		trash_image = customtkinter.CTkImage(Image.open(current_path + "/gui/trash_icon.png"), size=(20, 20))
		whiteboard_display_screen_trash_button = customtkinter.CTkButton(
			master = whiteboard_display_screen,
			command = edit_whiteboard_m2t,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		whiteboard_display_screen_trash_button.place(x=25, y=600)	

	def show_all_recordings():
		# self-explanatory
		lights_out(recordings_button)
		recordings_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Recordings')
		switch_frame(only_recordings_frame)
		forget_buttons(only_recordings_frame)
		update_wawla_text()

		recordings = current_user.get_recordings()

		row = 0
		buttons = []
		newline = '\n'
		for elem in recordings:

			recording = customtkinter.CTkButton(
				master = only_recordings_frame,
				command = lambda x=elem[0]: recording_display(x),
				image = recordings_image,
				width = 250,
				height = 50,
				font = font,
				text = f"{short(elem[2])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = user_button_color,
				hover_color = '#323232',
				border_width = 1,
				)
			recording.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(recording)	

	def recording_display_tags_light_up(tags):
		if tags is None:
			return
		if 'Personal' in tags:
			recording_display_screen_tag_personal_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'School' in tags:
			recording_display_screen_tag_school_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'Work' in tags:
			recording_display_screen_tag_work_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		if 'Other' in tags:
			recording_display_screen_tag_other_button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)

	def display_recording_tags():
		tags = []
		if recording_display_screen_tag_personal_button.cget('fg_color') == user_button_color:
			tags.append('Personal')
		if recording_display_screen_tag_work_button.cget('fg_color') == user_button_color:
			tags.append('Work')
		if recording_display_screen_tag_school_button.cget('fg_color') == user_button_color:
			tags.append('School')
		if recording_display_screen_tag_other_button.cget('fg_color') == user_button_color:
			tags.append('Other')
		return tags

	def display_recording_favorite():
		if recording_display_favorite_button.cget("image") == favorites_filled_image:
			recording_display_favorite_button.configure(image = favorites_empty_image)
		else:
			recording_display_favorite_button.configure(image = favorites_filled_image)

	def check_if_recording_fav(status):
		if status:
			recording_display_favorite_button.configure(image = favorites_filled_image)
		else:
			recording_display_favorite_button.configure(image = favorites_empty_image)

	def recording_display_is_fav():
		return recording_display_favorite_button.cget("image") == favorites_filled_image

	def recording_display(recording_id):
		global is_playing, stream, audio_thread

		recording = peko_database.get_recording(current_user.user_id, recording_id)

		is_playing = False
		stream = None
		audio_thread = None
		#wf = wave.open(recording[3], 'rb')
		total_duration = float(recording[4])
		#wf.close()

		recording_display_screen_tag_personal_button.configure(fg_color = grey, hover_color = '#474747')
		recording_display_screen_tag_school_button.configure(fg_color = grey, hover_color = '#474747')
		recording_display_screen_tag_work_button.configure(fg_color = grey, hover_color = '#474747')
		recording_display_screen_tag_other_button.configure(fg_color = grey, hover_color = '#474747')

		switch_screen(recording_display_screen)

		recording_display_title_tb.delete(0, "end")
		recording_display_title_tb.insert(0, recording[2])
		recording_display_title_tb.place(x=20, y=20)

		def play_audio(volume_slider, duration_label):
			global stream, is_playing

			wf = wave.open(recording[3], 'rb')
			#total_duration = wf.getnframes() / wf.getframerate()

			# Create a PyAudio object
			p = pyaudio.PyAudio()

			# Open a stream
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)
			chunk_size = 1024
			data = wf.readframes(chunk_size)
			while data and is_playing:
				remaining_duration = total_duration - (wf.tell() / wf.getframerate())
				recording_display_duration_label.configure(text=f"{remaining_duration:.2f}")
				samples = struct.unpack(f"{len(data)//wf.getsampwidth()}h", data)
				volume = volume_slider.get()
				samples = [int(sample * volume / 100) for sample in samples]
				data = struct.pack(f"{len(samples)}h", *samples)
				stream.write(data)
				data = wf.readframes(chunk_size)

			# Cleanup
			stream.stop_stream()
			stream.close()
			p.terminate()
			wf.close()

			recording_display_play_button.configure(state = 'normal', fg_color = user_button_color)
			recording_display_stop_button.configure(state = 'disabled', fg_color = dgrey)
			duration_label.configure(text="0.00")

		def on_play():
			global is_playing, audio_thread
			is_playing = False  # Reset is_playing to allow replaying
			if audio_thread and audio_thread.is_alive():
				# If there's an existing audio thread, wait for it to finish before starting a new one
				audio_thread.join()
			is_playing = True
			recording_display_play_button.configure(state = 'disabled', fg_color = dgrey)
			recording_display_stop_button.configure(state = 'normal', fg_color = user_button_color)
			audio_thread = threading.Thread(target=play_audio, args=(recording_display_volume_slider, recording_display_duration_label))
			audio_thread.start()

		def on_stop():
			global is_playing
			is_playing = False
			recording_display_play_button.configure(state = 'normal', fg_color = user_button_color)
			recording_display_stop_button.configure(state = 'disabled', fg_color = dgrey)

		tags = [item[0] for item in peko_database.get_recording_tags(recording_id)]
		recording_display_tags_light_up(tags)
		check_if_recording_fav(recording[7])

		def edit_recording_submit():

			peko_database.edit_recording_submit(current_user.user_id, 
			recording_id,
			recording_display_title_tb.get(),
			recording_display_is_fav(), 
			display_recording_tags() 
			)
			switch_screen(add_content_screen)
			switch_frame(all_notes_frame)
			show_all_notes()

		recording_display_submit_button = customtkinter.CTkButton(
			master = recording_display_screen,
			command = edit_recording_submit,
			text = 'Submit',
			font=('Segoe', 16, 'bold'),
			width = 110,
			height = 36,
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		recording_display_submit_button.place(x=365, y=600)

		def edit_recording_m2t():

			peko_database.recording_m2t(current_user.user_id, recording_id)
			switch_frame(all_notes_frame)
			show_all_notes()
			switch_screen(add_content_screen)

		trash_image = customtkinter.CTkImage(Image.open(current_path + "/gui/trash_icon.png"), size=(20, 20))
		recording_display_screen_trash_button = customtkinter.CTkButton(
			master = recording_display_screen,
			command = edit_recording_m2t,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		recording_display_screen_trash_button.place(x=25, y=600)	

		play_image = customtkinter.CTkImage(Image.open(current_path + '/gui/play_icon.png'), size = (32,32))
		recording_display_play_button = customtkinter.CTkButton(
			master = recording_display_screen,
			text = '',
			image = play_image,
			command = on_play,
			width = 80,
			height = 80,
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			state = 'normal'
			)
		recording_display_play_button.place(x=20, y=120)	

		stop_image_bigger = customtkinter.CTkImage(Image.open(current_path + "/gui/stop_icon.png"), size=(32, 32))
		recording_display_stop_button = customtkinter.CTkButton(
			master = recording_display_screen,
			text = '',
			image = stop_image_bigger,
			command = on_stop,
			width = 80,
			height = 80,
			#fg_color = user_button_color,
			hover_color = user_button_color_hover,
			state = 'disabled',
			fg_color = dgrey
			)
		recording_display_stop_button.place(x=120, y=120)

		recording_display_volume_slider = customtkinter.CTkSlider(
			master = recording_display_screen,
			from_ = 0,
			to = 100,
			number_of_steps = 101,
			button_color = user_button_color,
			button_hover_color = user_button_color_hover,
			progress_color = 'white'
			)
		recording_display_volume_slider.place(x=220, y=170)

		recording_display_duration_label = customtkinter.CTkLabel(
			master = recording_display_screen,
			text = f'{total_duration:.2f}',
			font = ('Segoe', 15),
			bg_color = lgrey
			)
		recording_display_duration_label.place(x=305, y=120)

	def show_all_contacts():
		# self-explanatory
		lights_out(contacts_button)
		contacts_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Contacts')
		switch_frame(contacts_frame)
		forget_buttons(contacts_frame)
		update_wawla_text()

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
			bg_color = grey
		)
		add_new_contact_button.grid(row=0, column=0, padx=10, pady=(0, 20))

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
				text = f'{short(elem[3])}',
				font=('Segoe', 15, 'bold'),
				anchor = 'w',
				fg_color = '#1f1f1f',
				bg_color = '#282828',
				background_corner_colors = ['#282828','#282828','#282828','#282828'],
				border_color = user_button_color,
				hover_color = '#323232',
				border_width=1
				)
			contact.grid(row=row, column=0, padx=10, pady=(0, 20))
			row += 1
			buttons.append(contact)

	def contact_display(contact_id):

		contact = peko_database.get_contact(current_user.user_id, contact_id)
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

		def delete_contact_forever():
			peko_database.delete_contact(current_user.user_id, contact_id)
			show_all_contacts()
			switch_screen(add_content_screen)

		contact_delete_button = customtkinter.CTkButton(
			master = contact_display_screen,
			command = delete_contact_forever,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		contact_delete_button.place(x=335, y=280)	

	def show_history():
		# self-explanatory
		lights_out(history_button)
		history_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('History')
		forget_buttons(history_frame)
		switch_frame(history_frame)
		update_wawla_text()

		row = 0
		history_data = current_user.get_current_history()
		newline = '\n'

		# Organize data by date
		history_by_date = defaultdict(list)
		for record in history_data:
			date, time, item_type, item_name, action_type = record
			if action_type == 'Edit':	
				history_by_date[date].append(f"* [{time}] {item_type} \"{item_name}\" has been {action_type.lower()}ed.{newline}")
			else:
				history_by_date[date].append(f"* [{time}] {item_type} \"{item_name}\" has been {action_type.lower()}d.{newline}")

		# Display the history in the frame, grouped by date
		for date, actions in history_by_date.items():
			date_label = customtkinter.CTkLabel(
				master = history_frame,
				text=f"\n{date} {newline}",
				font=('Segoe', 22, 'bold'),
				text_color = '#999999',
				justify = 'left',
				wraplength = 281
					)
			date_label.grid(row = row, column = 0)
			row += 1

			for action in actions:
				action_label = customtkinter.CTkLabel(
					master = history_frame,
					text = action,
					font = ('Segoe', 15),
					text_color = 'white',
					anchor = 'w',
					wraplength = 281
						)
				action_label.grid(row = row, column = 0, sticky = 'w')
				#action_label.pack(side = 'bottom', in_=history_frame)
				row += 1

	def show_settings():
		# self-explanatory
		lights_out(settings_button)
		settings_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		switch_screen(settings_screen)

	def show_add_content_screen():
		switch_screen(add_content_screen)

	def add_new_text_note():
		switch_screen(add_text_note_screen)

	def	add_new_whiteboard_note():
		switch_screen(add_whiteboard_screen)

	def add_new_recording_note():
		switch_screen(add_recording_screen)

	def new_note_cancel():
		switch_screen(add_content_screen)

	def note_tags():
		tags = []
		if note_tag_personal_button.cget('fg_color') == user_button_color:
			tags.append('Personal')
		if note_tag_work_button.cget('fg_color') == user_button_color:
			tags.append('Work')
		if note_tag_school_button.cget('fg_color') == user_button_color:
			tags.append('School')
		if note_tag_other_button.cget('fg_color') == user_button_color:
			tags.append('Other')
		return tags

	def whiteboard_tags():
		tags = []
		if whiteboard_tag_personal_button.cget('fg_color') == user_button_color:
			tags.append('Personal')
		if whiteboard_tag_work_button.cget('fg_color') == user_button_color:
			tags.append('Work')
		if whiteboard_tag_school_button.cget('fg_color') == user_button_color:
			tags.append('School')
		if whiteboard_tag_other_button.cget('fg_color') == user_button_color:
			tags.append('Other')
		return tags

	def recording_tags():
		tags = []
		if recording_tag_personal_button.cget('fg_color') == user_button_color:
			tags.append('Personal')
		if recording_tag_work_button.cget('fg_color') == user_button_color:
			tags.append('Work')
		if recording_tag_school_button.cget('fg_color') == user_button_color:
			tags.append('School')
		if recording_tag_other_button.cget('fg_color') == user_button_color:
			tags.append('Other')
		return tags

	def new_note_submit():
		title = new_note_title_tb.get().strip()
		favorite = check_if_fav_button()
		content = new_note_content_tb.get('0.0', 'end').strip()

		tags = note_tags()

		peko_database.insert_text_note(current_user.user_id, title, content, favorite, tags)
		switch_screen(add_content_screen)
		show_all_notes()

	def check_if_fav_button():
		return new_note_favorite_button.cget("image") == favorites_filled_image

	def check_if_fav_button2():
		return new_whiteboard_favorite_button.cget("image") == favorites_filled_image

	def check_if_fav_button3():
		return new_recording_favorite_button.cget("image") == favorites_filled_image

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

	def new_recording_fav():
		if new_recording_favorite_button.cget("image") == favorites_empty_image:
			new_recording_favorite_button.configure(image = favorites_filled_image)
		else:
			new_recording_favorite_button.configure(image = favorites_empty_image)

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
		favorite = check_if_fav_button2()
		tags = whiteboard_tags()
		peko_database.insert_whiteboard(current_user.user_id, title, content, favorite, tags)
		switch_screen(add_content_screen)
		show_all_notes()

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
		uid = current_user.user_id
		title = new_reminder_title_tb.get().strip()
		desc = new_reminder_content_tb.get('0.0', 'end').strip()
		rem_date = cal.get_date()

		peko_database.insert_reminder(uid, title, desc, rem_date)

		show_all_reminders()
		switch_screen(add_content_screen)

	def show_all_personal():
		# self-explanatory
		lights_out(personal_button)
		personal_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Personal')
		switch_frame(only_personal_frame)
		forget_buttons(only_personal_frame)
		update_wawla_text()

		all_personal = current_user.get_all_tag(tag_name = 'Personal')

		row = 0
		buttons = []
		newline = '\n'

		for elem in all_personal:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: recording_display(x)

			note_button = customtkinter.CTkButton(
				master= only_personal_frame,
				command=note_display_command,
				image=note_image,
				width=250,
				height=50,
				font = font,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)

	def show_all_work():
		# self-explanatory
		lights_out(work_button)
		work_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Work')
		switch_frame(only_work_frame)
		forget_buttons(only_work_frame)
		update_wawla_text()

		all_work = current_user.get_all_tag(tag_name = 'Work')		

		row = 0
		buttons = []
		newline = '\n'

		for elem in all_work:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: recording_display(x)

			note_button = customtkinter.CTkButton(
				master= only_work_frame,
				command=note_display_command,
				image=note_image,
				font = font,
				width=250,
				height=50,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)		

	def show_all_school():
		# self-explanatory
		lights_out(school_button)
		school_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('School')
		switch_frame(only_school_frame)
		forget_buttons(only_school_frame)
		update_wawla_text()

		all_school = current_user.get_all_tag(tag_name = 'School')

		row = 0
		buttons = []
		newline = '\n'

		for elem in all_school:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: recording_display(x)

			note_button = customtkinter.CTkButton(
				master= only_school_frame,
				command=note_display_command,
				image=note_image,
				font = font,
				width=250,
				height=50,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)	

	def show_all_other():
		# self-explanatory
		lights_out(other_button)
		other_button.configure(fg_color=user_button_color, hover_color = user_button_color_hover)
		set_wawla('Other')
		switch_frame(only_other_frame)
		forget_buttons(only_other_frame)
		update_wawla_text()

		all_other = current_user.get_all_tag(tag_name = 'Other')
	
		row = 0
		buttons = []
		newline = '\n'

		for elem in all_other:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: recording_display(x)

			note_button = customtkinter.CTkButton(
				master= only_other_frame,
				command=note_display_command,
				image=note_image,
				font = font,
				width=250,
				height=50,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)	

	def show_search_results():
			# self-explanatory
			search_results_frame.place(x=220, y=100)
			set_wawla('Search results')
			update_wawla_text()
			switch_frame(search_results_frame)
			forget_buttons(search_results_frame)

			global sr
			title, favorite, types, tags, last_edit_limit = sr
			print(sr)
			uid = current_user.user_id
			search_results = peko_database.search_results(uid, title, favorite, types, tags, last_edit_limit)

			row = 0
			buttons = []
			newline = '\n'

			for elem in search_results:

				note_image = None
				note_display_command = None

				if elem[0] == 'Notes':
					note_image = text_image
					note_display_command = lambda x=elem[1]: text_note_display(x)
				elif elem[0] == 'WhiteboardNotes':
					note_image = whiteboards_image
					note_display_command = lambda x=elem[1]: whiteboard_display(x)
				elif elem[0] == 'Recordings':
					note_image = recordings_image
					note_display_command = lambda x=elem[1]: recording_display(x)

				note_button = customtkinter.CTkButton(
					master = search_results_frame,
					command = note_display_command,
					image=note_image,
					width=250,
					height=50,
					text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
					font = font,
					anchor='w',
					fg_color='#1f1f1f',
					bg_color='#282828',
					background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
					border_color=user_button_color,
					hover_color='#323232',
					border_width=1,)
				note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
				row += 1
				buttons.append(note_button)

	def show_search_window():

		global search_window

		if search_window is None or not search_window.winfo_exists():
			search_window = customtkinter.CTkToplevel(
				master = app,
				fg_color = grey
				)
			search_window.geometry('480x260')
			search_window.resizable(0,0)
			search_window.title('Search')
			search_window.focus()
			search_window.after(100, search_window.lift)
		else:
			search_window.focus()
			search_window.after(100, search_window.lift)
			# everything dissapears from text boxes when else: is executed. (why?)

		if sys.platform.startswith("win"):
			search_window.after(200, lambda: search_window.iconbitmap(current_path + '/gui/icon.ico'))

		title_search_label = customtkinter.CTkLabel(
			master = search_window,
			text = 'TITLE',
			bg_color = grey,
			font=('Segoe', 10, 'bold'),
			text_color = 'white'
			)
		title_search_label.place(x=10, y=2)

		title_search_tb = customtkinter.CTkEntry(
			master = search_window,
			width = 315,
			height = 30,
			fg_color = '#282828',
			border_color = user_button_color,
			border_width = 3,
			placeholder_text = ''
			)
		title_search_tb.place(x=10, y=25)

		favorite_search_label = customtkinter.CTkLabel(
			master = search_window,
			text = 'FAVORITE',
			bg_color = grey,
			font=('Segoe', 10, 'bold'),
			text_color = 'white'
			)
		favorite_search_label.place(x=335, y=2)

		hc = get_hover_color(lgrey)

		favorite_search_menu = customtkinter.CTkOptionMenu(
			master = search_window,
			width = 140,
			values=['', 'Yes', 'No'],
			fg_color = lgrey,
			button_color = user_button_color,
			button_hover_color = user_button_color_hover,
			dropdown_fg_color = lgrey,
			dropdown_hover_color = hc
			)
		favorite_search_menu.place(x=335, y=25)

		type_search_label = customtkinter.CTkLabel(
			master = search_window,
			text = 'TYPE',
			bg_color = grey,
			font=('Segoe', 10, 'bold'),
			text_color = 'white'
			)
		type_search_label.place(x=10, y=55)

		def type_checkboxes_func():
			#print("checkbox toggled, current value:", text_note_checkbox_var.get())
			pass

		text_note_checkbox_var = customtkinter.StringVar(value="on")
		text_note_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "Text Note",
			font = ('Segoe', 12, 'bold'),		 	
			command = type_checkboxes_func,
			variable = text_note_checkbox_var,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		text_note_checkbox.place(x=10, y=78)

		whiteboard_checkbox_var = customtkinter.StringVar(value="on")
		whiteboard_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "Whiteboard",
			font = ('Segoe', 12, 'bold'),
			command = type_checkboxes_func,
			variable = whiteboard_checkbox_var,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		whiteboard_checkbox.place(x=120, y=78)

		recording_checkbox_var = customtkinter.StringVar(value="on")
		recording_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "Recording",
			font = ('Segoe', 12, 'bold'),
			command = type_checkboxes_func,
			variable = recording_checkbox_var,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		recording_checkbox.place(x=230, y=78)

		tags_search_label = customtkinter.CTkLabel(
			master = search_window,
			text = 'TAGS',
			bg_color = grey,
			font=('Segoe', 10, 'bold'),
			text_color = 'white'
			)
		tags_search_label.place(x=10, y=104)

		def tags_checkboxes_func():
			pass

		personal_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "Personal",
			font = ('Segoe', 12, 'bold'),		 	
			command = tags_checkboxes_func,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		personal_checkbox.place(x=10, y=127)

		school_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "School",
			font = ('Segoe', 12, 'bold'),		 	
			command = tags_checkboxes_func,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		school_checkbox.place(x=120, y=127)

		work_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "Work",
			font = ('Segoe', 12, 'bold'),		 	
			command = tags_checkboxes_func,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		work_checkbox.place(x=230, y=127)

		other_checkbox = customtkinter.CTkCheckBox(
			master = search_window,
			text = "Other",
			font = ('Segoe', 12, 'bold'),		 	
			command = tags_checkboxes_func,
			onvalue = "on",
			offvalue = "off",
			fg_color = user_button_color,
			hover_color = hc,
			border_color = user_button_color
			)
		other_checkbox.place(x=340, y=127)

		last_edited_search_label = customtkinter.CTkLabel(
			master = search_window,
			text = 'LAST EDITED',
			bg_color = grey,
			font=('Segoe', 10, 'bold'),
			text_color = 'white'
			)
		last_edited_search_label.place(x=10, y=180)

		last_edited_search_menu = customtkinter.CTkOptionMenu(
			master = search_window,
			width = 140,
			values=['Today', 'Yesterday', 'Last week', 'Last month', 'Last year'],
			fg_color = lgrey,
			button_color = user_button_color,
			button_hover_color = user_button_color_hover,
			dropdown_fg_color = lgrey,
			dropdown_hover_color = hc
			)
		last_edited_search_menu.place(x=80, y=180)

		or_later_search_label = customtkinter.CTkLabel(
			master = search_window,
			text = 'OR LATER',
			bg_color = grey,
			font=('Segoe', 10, 'bold'),
			text_color = 'white'
			)
		or_later_search_label.place(x=230, y=180)

		def search_submit():

			global sr
			sr = []

			title = title_search_tb.get().strip()
			favorite = favorite_search_menu.get() if favorite_search_menu.get() else None # 'Yes', 'No', None
			fav_bool = True if favorite == 'Yes' else False if favorite is not None else None

			types = []
			if text_note_checkbox.get() == 'on':
				types.append('Text Note')
			if whiteboard_checkbox.get() == 'on':
				types.append('Whiteboard')
			if recording_checkbox.get() == 'on':
				types.append('Recording')

			tags = []
			if personal_checkbox.get() == 'on':
				tags.append('Personal')
			if school_checkbox.get() == 'on':
				tags.append('School')
			if work_checkbox.get() == 'on':
				tags.append('Work')
			if other_checkbox.get() == 'on':
				tags.append('Other')
			
			last_edit_limit = last_edited_search_menu.get()

			sr = [title, fav_bool, types, tags, last_edit_limit]
			search_window.destroy()
			show_search_results()
			return sr

		search_submit_button = customtkinter.CTkButton(
			master = search_window,
			command = search_submit,
			text = 'Search',
			font=('Segoe', 16, 'bold'),
			width = 110,
			height = 36,
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
			 )
		search_submit_button.place(x=325, y=200)

	def tags_light_up(button):
		if button.cget('fg_color') == grey:
			button.configure(fg_color = user_button_color, hover_color = user_button_color_hover)
		else:
			button.configure(fg_color = grey, hover_color = '#474747')

	def new_recording_submit():
		global frames, audio
		filename = asksaveasfilename(defaultextension=".wav",
		 filetypes=[("WAV files", "*.wav")])
		if filename:
			wf = wave.open(filename, 'wb')
			wf.setnchannels(1)
			wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
			wf.setframerate(44100)
			wf.writeframes(b''.join(frames))
			duration =  round(float(wf.getnframes() / wf.getframerate()),2)
			wf.close()
			frames = []

			# add to database
			title = new_recording_title_tb.get().strip()
			content = filename
			favorite = check_if_fav_button3()
			tags = recording_tags()

			peko_database.insert_recording(current_user.user_id, title, content, duration, favorite, tags)

		audio = pyaudio.PyAudio()
		switch_screen(add_content_screen)
		switch_frame(all_notes_frame)
		show_all_notes()

	def start_recording():

		recording_button.configure(state = 'disabled', fg_color = dgrey)
		new_recording_submit_button.configure(state = 'disabled', fg_color = dgrey)
		stop_recording_button.configure(state = 'normal', fg_color = user_button_color, hover_color = user_button_color_hover)
		threading.Thread(target=record).start()

	def record():
		global is_recording, frames, audio
		is_recording = True

		audio = pyaudio.PyAudio()
		stream = audio.open(format = pyaudio.paInt16, channels = 1, rate = 44100,
		input = True, frames_per_buffer = 1024)
		frames = []
		while is_recording:
			data = stream.read(1024)
			frames.append(data)
		stream.stop_stream()
		stream.close()
		audio.terminate()

	def stop_recording():
		global is_recording

		recording_button.configure(state = 'normal', fg_color = user_button_color, hover_color = user_button_color_hover)
		new_recording_submit_button.configure(state = 'normal', fg_color = user_button_color, hover_color = user_button_color_hover)
		stop_recording_button.configure(state = 'disabled', fg_color = dgrey)

		is_recording = False

	def settings_cancel():
		switch_screen(add_content_screen)
		settings_button.configure(fg_color = dgrey)

	def change_user_avatar():
		file_path = askopenfilename()
		if file_path:
			avatar_file_path = file_path
			avatar = customtkinter.CTkImage(Image.open(avatar_file_path), size=(64, 64))
			avatar_check_out = customtkinter.CTkImage(Image.open(avatar_file_path), size=(128, 128))
			user_avatar_change_button.configure(image = avatar_check_out)
			user_avatar_button.configure(image = avatar)

			peko_database.update_avatar(current_user.user_id, avatar_file_path)

	def pick_theme_color():

		color_code = colorchooser.askcolor(title="Choose a color")
		if color_code[1]:

			color_hex = color_code[1]
			peko_database.update_color_scheme(current_user.user_id, color_hex)
			theme_color_button.configure(fg_color = color_hex, hover_color = get_hover_color(color_hex))

	def settings_submit():
		display_name = change_user_display_name_tb.get().strip()
		if display_name != '':
			username_text.configure(text = display_name)
			peko_database.update_display_name(current_user.user_id, display_name)

	def show_all_trash():
		# self-explanatory
		set_wawla('Trash')
		switch_frame(trash_frame)
		forget_buttons(trash_frame)
		update_wawla_text()

		all_trash = current_user.get_trash()

		row = 0
		buttons = []
		newline = '\n'

		if all_trash == []:
			trash_frame_label = customtkinter.CTkLabel(
				master = trash_frame,
				font = ('Segoe', 14, 'bold'),
				text = 'Trash is empty.',
				fg_color = grey
				)
			trash_frame_label.grid(row=0, column=0, padx=90, pady=180)

		for elem in all_trash:

			note_image = None
			note_display_command = None

			if elem[0] == 'Notes':
				note_image = text_image
				note_display_command = lambda x=elem[1]: trash_text_note_display(x)
			elif elem[0] == 'WhiteboardNotes':
				note_image = whiteboards_image
				note_display_command = lambda x=elem[1]: trash_whiteboard_display(x)
			elif elem[0] == 'Recordings':
				note_image = recordings_image
				note_display_command = lambda x=elem[1]: trash_recording_display(x)

			note_button = customtkinter.CTkButton(
				master= trash_frame,
				command=note_display_command,
				image=note_image,
				width=250,
				height=50,
				text=f"{short(elem[3])} {newline} {elem[5].strftime('%Y-%m-%d %H:%M')}",
				anchor='w',
				fg_color='#1f1f1f',
				bg_color='#282828',
				background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
				border_color=user_button_color,
				hover_color='#323232',
				border_width=1,)
			note_button.grid(row=row, column=0, padx=10, pady=(10, 10))
			row += 1
			buttons.append(note_button)

	def trash_text_note_display(note_id):

		note = peko_database.get_text_note(current_user.user_id, note_id)
		tags = peko_database.get_text_note_tags(note_id)

		switch_screen(text_note_trash_display_screen)
		text_note_trash_title_label.configure(text = note[2])
		text_note_trash_date_create_label.configure(text = f"Created on {note[4].strftime('%Y-%m-%d %H:%M')}")
		text_note_trash_date_edit_label.configure(text = f"Last edited on {note[5].strftime('%Y-%m-%d %H:%M')}")
		if note[6]:
			text_note_trash_favorite_label.configure(text = f"Favorite: YES")
		else:
			text_note_trash_favorite_label.configure(text = f"Favorite: NO")
		text_note_trash_tags_label.configure(text = f"Tags: {tags}")

		def restore_text_note_from_trash():
			peko_database.restore_text_note(current_user.user_id, note_id)
			switch_screen(settings_screen)
			show_all_trash()

		def delete_text_note_forever():
			peko_database.delete_text_note(current_user.user_id, note_id)
			show_all_trash()
			switch_screen(settings_screen)

		text_note_delete_button = customtkinter.CTkButton(
			master = text_note_trash_display_screen,
			command = delete_text_note_forever,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		text_note_delete_button.place(x=150, y=330)	

		restore_image = customtkinter.CTkImage(Image.open(current_path + '/gui/restore_icon.png'), size = (20,20))
		text_note_restore_button = customtkinter.CTkButton(
			master = text_note_trash_display_screen,
			command = restore_text_note_from_trash,
			text = 'Restore',
			image = restore_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		text_note_restore_button.place(x=25, y=330)	

	def trash_whiteboard_display(whiteboard_id):

		whiteboard = peko_database.get_whiteboard(current_user.user_id, whiteboard_id)
		tags = [item[0] for item in peko_database.get_whiteboard_tags(whiteboard_id)]

		switch_screen(whiteboard_trash_display_screen)
		whiteboard_trash_title_label.configure(text = whiteboard[2])
		whiteboard_trash_date_create_label.configure(text = f"Created on {whiteboard[4].strftime('%Y-%m-%d %H:%M')}")
		whiteboard_trash_date_edit_label.configure(text = f"Last edited on {whiteboard[5].strftime('%Y-%m-%d %H:%M')}")
		if whiteboard[6]:
			whiteboard_trash_favorite_label.configure(text = f"Favorite: YES")
		else:
			whiteboard_trash_favorite_label.configure(text = f"Favorite: NO")
		whiteboard_trash_tags_label.configure(text = f"Tags: {tags}")

		def restore_whiteboard_from_trash():
			peko_database.restore_whiteboard(current_user.user_id, whiteboard_id)
			switch_screen(settings_screen)
			show_all_trash()

		def delete_whiteboard_forever():
			peko_database.delete_whiteboard(current_user.user_id, whiteboard_id)
			switch_screen(settings_screen)
			show_all_trash()

		whiteboard_delete_button = customtkinter.CTkButton(
			master = whiteboard_trash_display_screen,
			command = delete_whiteboard_forever,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		whiteboard_delete_button.place(x=150, y=330)	

		restore_image = customtkinter.CTkImage(Image.open(current_path + '/gui/restore_icon.png'), size = (20,20))
		whiteboard_restore_button = customtkinter.CTkButton(
			master = whiteboard_trash_display_screen,
			command = restore_whiteboard_from_trash,
			text = 'Restore',
			image = restore_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		whiteboard_restore_button.place(x=25, y=330)	

	def trash_recording_display(recording_id):

		recording = peko_database.get_recording(current_user.user_id, recording_id)
		tags = [item[0] for item in peko_database.get_recording_tags(recording_id)]

		switch_screen(recording_trash_display_screen)
		recording_trash_title_label.configure(text = recording[2])
		recording_trash_date_create_label.configure(text = f"Created on {recording[5].strftime('%Y-%m-%d %H:%M')}")
		recording_trash_duration_label.configure(text = f"Duration {recording[4]} seconds")
		if recording[7]:
			recording_trash_favorite_label.configure(text = f"Favorite: YES")
		else:
			recording_trash_favorite_label.configure(text = f"Favorite: NO")
		recording_trash_tags_label.configure(text = f"Tags: {tags}")

		def restore_recording_from_trash():
			peko_database.restore_recording(current_user.user_id, recording_id)
			switch_screen(settings_screen)
			show_all_trash()

		def delete_recording_forever():
			peko_database.delete_recording(current_user.user_id, recording_id)
			switch_screen(settings_screen)
			show_all_trash()

		recording_delete_button = customtkinter.CTkButton(
			master = recording_trash_display_screen,
			command = delete_recording_forever,
			text = 'Delete',
			image = trash_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		recording_delete_button.place(x=150, y=330)	

		restore_image = customtkinter.CTkImage(Image.open(current_path + '/gui/restore_icon.png'), size = (20,20))
		recording_restore_button = customtkinter.CTkButton(
			master = recording_trash_display_screen,
			command = restore_recording_from_trash,
			text = 'Restore',
			image = restore_image,
			font = ('Segoe', 16, 'bold'),
			width = 100,
			height = 36,
			compound = 'left',
			anchor = 'w',
			fg_color = user_button_color,
			hover_color = user_button_color_hover,
			background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
			bg_color = '#323232'
		 )
		recording_restore_button.place(x=25, y=330)	


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
	text_button.place(x=20, y=245)

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
	whiteboards_button.place(x=20, y=275)

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
	recordings_button.place(x=20, y=305)

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
	personal_button.place(x=20, y=380)

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
	work_button.place(x=20, y=410)

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
	school_button.place(x=20, y=440)

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
	other_button.place(x=20, y=470)

	# History Button
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
	history_button.place(x=20, y=545)

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
	settings_button.place(x=20, y=575)

	# User Avatar Button
	user_avatar_button = customtkinter.CTkButton(
		master = app,
		image = current_user_avatar64,
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

	default_frame = customtkinter.CTkFrame(
		master = app,
		width = 305,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3
		)
	default_frame.place(x=220, y=100)

	default_frame_label = customtkinter.CTkLabel(
		master = default_frame,
		font = ('Segoe', 14, 'bold'),
		text = 'Use buttons on the left to navigate.',
		fg_color = grey
		)
	default_frame_label.place(x=30, y=190)

	search_results_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3
		)

	all_notes_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3
		)

	reminders_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3,
		)

	favorites_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3,
		)

	contacts_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3,
		)

	trash_frame = customtkinter.CTkScrollableFrame(
		master = app,
		width = 281,
		height = 583,
		bg_color = '#282828',
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3,
		)

	only_text_notes_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	only_whiteboards_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	only_recordings_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	only_personal_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	only_work_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	only_school_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	only_other_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	)

	history_frame = customtkinter.CTkScrollableFrame(
	master = app,
	width = 281,
	height = 583,
	bg_color = '#282828',
	fg_color = '#282828',
	border_color = user_button_color,
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
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
	background_corner_colors=['#282828', '#282828', '#282828', '#282828'],
	bg_color = '#282828'
			 )
	add_button.place(x=490, y=10)

	# Search Button
	search_image = customtkinter.CTkImage(Image.open(current_path + "/gui/search_icon.png"), size=(20, 20))
	search_button = customtkinter.CTkButton(
	master = app,
	command = show_search_window,
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
	categories_text.place(x=28, y=215)

	# Tags Text
	tags_text = customtkinter.CTkLabel(
	master = app,
	text = 'Tags',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	tags_text.place(x=28, y=350)

	# Account Text
	account_text = customtkinter.CTkLabel(
	master = app,
	text = 'Account',
	bg_color = '#1f1f1f',
	font=('Segoe', 13, 'bold'),
	text_color = '#999999'
		)
	account_text.place(x=28, y=515)

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
	text = current_user_display_name, 
	bg_color = '#1f1f1f',
	font=('Segoe', 15, 'bold'),
	text_color = 'White'
		)
	username_text.place(x=95, y=655) # 28

	# Text Elements - Middle Panel

	# What are we looking at Text
	wawla_text = customtkinter.CTkLabel(
	master = app,
	text = 'Welcome!',
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
		border_color = user_button_color,
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
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
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
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
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
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
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
		command = lambda: tags_light_up(note_tag_personal_button),
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
		command = lambda: tags_light_up(note_tag_work_button),
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
		command = lambda: tags_light_up(note_tag_school_button),
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
		command = lambda: tags_light_up(note_tag_other_button),
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
		hover_color = user_button_color_hover,
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
		fg_color = user_button_color,
		hover_color = user_button_color_hover,
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
			 )
	new_note_submit_button.place(x=365, y=580)


# =======================================================================================================================

	text_note_display_screen = customtkinter.CTkFrame(
	master = app,
	width = 500,
	height = 650,
	bg_color = '#323232',
	fg_color = '#323232',
	border_color = user_button_color,
	border_width = 3
	)

	text_note_display_title_tb = customtkinter.CTkEntry(
		master = text_note_display_screen,
		width = 400,
		height = 30,
		font = ('Segoe', 16, 'bold'),
		border_width = 1,
		fg_color = '#474747'
		)

	text_note_display_favorite_button = customtkinter.CTkButton(
		master = text_note_display_screen,
		width = 32,
		height = 32,
		command = display_text_note_favorite,
		text = "",
		image = favorites_empty_image,
		fg_color = '#323232',
		bg_color = '#323232',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		hover_color = '#323232'
		)
	text_note_display_favorite_button.place(x=434, y=13)

	text_note_display_content_tb = customtkinter.CTkTextbox(
		master = text_note_display_screen,
		width = 458,
		height = 420,
		wrap = 'word',
		font = ('Segoe', 16),
		border_width = 1,
		fg_color = '#474747'
		)

	text_note_display_tag_text = customtkinter.CTkLabel(
		master = text_note_display_screen,
		text = 'Tags',
		font = ('Segoe', 14, 'bold')
		)
	text_note_display_tag_text.place(x=25, y=487)

	# Personal Tag
	text_note_display_tag_personal_button = customtkinter.CTkButton(
		master = text_note_display_screen,
		command = lambda: tags_light_up(text_note_display_tag_personal_button),
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
	text_note_display_tag_personal_button.place(x=24, y=517)

	# Work Tag
	text_note_display_tag_work_button = customtkinter.CTkButton(
		master = text_note_display_screen,
		command = lambda: tags_light_up(text_note_display_tag_work_button),
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
	text_note_display_tag_work_button.place(x=139, y=517)

	# School Tag
	text_note_display_tag_school_button = customtkinter.CTkButton(
		master = text_note_display_screen,
		command = lambda: tags_light_up(text_note_display_tag_school_button),
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
	text_note_display_tag_school_button.place(x=254, y=517)

	# Other Tag
	text_note_display_tag_other_button = customtkinter.CTkButton(
		master = text_note_display_screen,
		command = lambda: tags_light_up(text_note_display_tag_other_button),
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
	text_note_display_tag_other_button.place(x=369, y=517)

	text_note_display_cancel_button = customtkinter.CTkButton(
		master = text_note_display_screen,
		command = new_note_cancel,
		text = 'Cancel',
		font=('Segoe', 16),
		width = 110,
		height = 36,
		fg_color = '#474747',
		hover_color = user_button_color_hover,
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
			 )
	text_note_display_cancel_button.place(x=250, y=580)


# ========================================== CONTACTS ============================================

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

	new_contact_submit_button = customtkinter.CTkButton(
		master = add_contact_screen,
		command = new_contact_submit,
		text = 'Submit',
		font=('Segoe', 16, 'bold'),
		width = 110,
		height = 36,
		fg_color = dgrey,
		hover_color = user_button_color_hover,
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232',
		state = 'disabled'
			 )
	new_contact_submit_button.place(x=375, y=330)

	def on_entry_change(*args):
		value = display_name_tb.get()
		if value:
			new_contact_submit_button.configure(state = 'normal', fg_color = user_button_color)
		else:
			new_contact_submit_button.configure(state = 'disabled', fg_color = dgrey)

	entry_text = tkinter.StringVar()		

	# Display Name TextBox
	display_name_tb = customtkinter.CTkEntry(
		master = add_contact_screen,
		textvariable = entry_text,
		width = 315,
		height = 30,
		fg_color = '#282828',
		border_color = user_button_color,
		border_width = 3,
		placeholder_text = ''
		)
	display_name_tb.place(x=170, y=130)

	entry_text.trace("w", on_entry_change)

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
	display_name_text.place(x=170, y=102)

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
	border_color = user_button_color,
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
	border_color = user_button_color,
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
	border_color = user_button_color,
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
	border_color = user_button_color,
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
		border_color = user_button_color
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

	canvas = tkinter.Canvas(add_whiteboard_screen, bg="white", width=612, height=560)
	canvas.place(x=4, y=90)

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
		fg_color = user_button_color,
		hover_color = user_button_color_hover,
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
		hover_color = user_button_color_hover,
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
	hover_color = user_button_color_hover,
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
	command = lambda: tags_light_up(whiteboard_tag_personal_button),
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
	command = lambda: tags_light_up(whiteboard_tag_work_button),
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
	command = lambda: tags_light_up(whiteboard_tag_school_button),
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
	command = lambda: tags_light_up(whiteboard_tag_other_button),
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

# ======================================= WHITEBOARD DISPLAY =================================================

	whiteboard_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_color = user_button_color,
		border_width = 3
	)

	whiteboard_display_title_tb = customtkinter.CTkEntry(
		master = whiteboard_display_screen,
		width = 400,
		height = 30,
		font = ('Segoe', 16, 'bold'),
		border_width = 1,
		fg_color = '#474747'
		)

	whiteboard_display_favorite_button = customtkinter.CTkButton(
		master = whiteboard_display_screen,
		width = 32,
		height = 32,
		command = display_whiteboard_favorite,
		text = "",
		image = favorites_empty_image,
		fg_color = '#323232',
		bg_color = '#323232',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		hover_color = '#323232'
		)
	whiteboard_display_favorite_button.place(x=434, y=13)

	whiteboard_display_screen_tag_text = customtkinter.CTkLabel(
		master = whiteboard_display_screen,
		text = 'Tags',
		font = ('Segoe', 14, 'bold')
		)
	whiteboard_display_screen_tag_text.place(x=25, y=520)

	# Personal Tag
	whiteboard_display_screen_tag_personal_button = customtkinter.CTkButton(
		master = whiteboard_display_screen,
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
		font = font,
		command = lambda: tags_light_up(whiteboard_display_screen_tag_personal_button)
			 )
	whiteboard_display_screen_tag_personal_button.place(x=24, y=550)

	# Work Tag
	whiteboard_display_screen_tag_work_button = customtkinter.CTkButton(
		master = whiteboard_display_screen,
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
		font = font,
		command = lambda: tags_light_up(whiteboard_display_screen_tag_work_button)
			 )
	whiteboard_display_screen_tag_work_button.place(x=139, y=550)

	# School Tag
	whiteboard_display_screen_tag_school_button = customtkinter.CTkButton(
		master = whiteboard_display_screen,
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
		font = font,
		command = lambda: tags_light_up(whiteboard_display_screen_tag_school_button)
			 )
	whiteboard_display_screen_tag_school_button.place(x=254, y=550)

	# Other Tag
	whiteboard_display_screen_tag_other_button = customtkinter.CTkButton(
		master = whiteboard_display_screen,
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
		font = font,
		command = lambda: tags_light_up(whiteboard_display_screen_tag_other_button)
			 )
	whiteboard_display_screen_tag_other_button.place(x=369, y=550)

	whiteboard_display_screen_cancel_button = customtkinter.CTkButton(
		master = whiteboard_display_screen,
		command = new_note_cancel,
		text = 'Cancel',
		font=('Segoe', 16),
		width = 110,
		height = 36,
		fg_color = '#474747',
		hover_color = user_button_color_hover,
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
			 )
	whiteboard_display_screen_cancel_button.place(x=250, y=600)

# ==================================== REMINDERS ==========================================

	add_reminder_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3,
		border_color = user_button_color
		)

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
		#border_color = user_button_color_hover,
		fg_color = '#474747'
		)
	new_reminder_title_tb.place(x=25, y=60)

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
		#border_color = user_button_color_hover,
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

	cal = tkcalendar.DateEntry(add_reminder_screen, width=12, background=user_button_color, foreground='#323232',
		borderwidth=2, year=2024, state='readonly')
	cal.place(x=32,y=436)

	#dt = cal.get_date()
	#str_dt = dt.strftime("%Y-%m-%d")

	new_reminder_cancel_button = customtkinter.CTkButton(
		master = add_reminder_screen,
		command = new_note_cancel,
		text = 'Cancel',
		font=('Segoe', 16),
		width = 110,
		height = 36,
		fg_color = '#474747',
		hover_color = user_button_color_hover,
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
		fg_color = user_button_color,
		hover_color = user_button_color_hover,
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
		)
	new_reminder_submit_button.place(x=365, y=335)


# =========	               REMINDER DISPLAY                  ==============

	reminder_display_screen = customtkinter.CTkFrame(
	master = app,
	width = 480,
	height = 600,
	bg_color = '#323232',
	fg_color = '#323232'
	)

	reminder_display_title_label = customtkinter.CTkLabel(
		master = reminder_display_screen,
		text = '',
		font = ('Segoe', 34, 'bold'),
		text_color = 'white'
	)

	reminder_display_description_label = customtkinter.CTkLabel(
		master = reminder_display_screen,
		text = '',
		font = ('Segoe', 15),
		text_color = 'white'
	)

	reminder_display_due_date_label = customtkinter.CTkLabel(
		master = reminder_display_screen,
		text = '',
		font = ('Segoe', 18, 'bold'),
		text_color = 'white'
	)

# ====================================== RECORDINGS =====================================

	add_recording_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3
		)

	new_recording_title_tb = customtkinter.CTkEntry(
		master = add_recording_screen,
		width = 400,
		height = 30,
		font = ('Segoe', 16, 'bold'),
		placeholder_text = 'Title...',
		border_width = 1,
		fg_color = '#474747'
		)
	new_recording_title_tb.place(x=25, y=25)

	new_recording_favorite_button = customtkinter.CTkButton(
		master = add_recording_screen,
		width = 32,
		height = 32,
		command = new_recording_fav,
		text = "",
		image = favorites_empty_image,
		fg_color = '#323232',
		bg_color = '#323232',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		hover_color = '#323232'
		)
	new_recording_favorite_button.place(x=437, y=18)

	#waves_animation = AudioWaves(add_recording_screen)

	# Recording Button
	recording_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = start_recording,
	image = recordings_image,
	text = '',
	width = 100,
	height = 100,
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	corner_radius = 20
			 )
	recording_button.place(x=139, y=300)

	# Stop Recording Button
	stop_image = customtkinter.CTkImage(Image.open(current_path + "/gui/stop_icon.png"), size=(20, 20))
	stop_recording_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = stop_recording,
	image = stop_image,
	text = '',
	width = 100,
	height = 100,
	fg_color = grey,
	hover_color = '#474747',
	background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey,
	corner_radius = 20,
	state = 'disabled'
			 )
	stop_recording_button.place(x=250, y=300)

	new_recording_tag_text = customtkinter.CTkLabel(
		master = add_recording_screen,
		text = 'Tags',
		font = ('Segoe', 14, 'bold')
		)
	new_recording_tag_text.place(x=25, y=490)

	# Personal Tag
	recording_tag_personal_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = lambda: tags_light_up(recording_tag_personal_button),
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
	recording_tag_personal_button.place(x=24, y=520)

	# Work Tag
	recording_tag_work_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = lambda: tags_light_up(recording_tag_work_button),
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
	recording_tag_work_button.place(x=139, y=520)

	# School Tag
	recording_tag_school_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = lambda: tags_light_up(recording_tag_school_button),
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
	recording_tag_school_button.place(x=254, y=520)

	# Other Tag
	recording_tag_other_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = lambda: tags_light_up(recording_tag_other_button),
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
	recording_tag_other_button.place(x=369, y=520)

	new_recording_cancel_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = new_note_cancel,
	text = 'Cancel',
	font=('Segoe', 16),
	width = 110,
	height = 36,
	fg_color = '#474747',
	hover_color = user_button_color_hover,
	background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
			 )
	new_recording_cancel_button.place(x=250, y=580)

	new_recording_submit_button = customtkinter.CTkButton(
	master = add_recording_screen,
	command = new_recording_submit,
	text = 'Submit',
	font=('Segoe', 16, 'bold'),
	width = 110,
	height = 36,
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
	background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
			 )
	new_recording_submit_button.place(x=365, y=580)

# ========================== 	RECORDNIG DISPLAY ===================================

	recording_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_color = user_button_color,
		border_width = 3
	)

	recording_display_title_tb = customtkinter.CTkEntry(
		master = recording_display_screen,
		width = 400,
		height = 30,
		font = ('Segoe', 16, 'bold'),
		border_width = 1,
		fg_color = '#474747'
		)
	recording_display_title_tb.place(x=20, y=20)

	recording_display_favorite_button = customtkinter.CTkButton(
		master = recording_display_screen,
		width = 32,
		height = 32,
		command = display_recording_favorite,
		text = "",
		image = favorites_empty_image,
		fg_color = '#323232',
		bg_color = '#323232',
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		hover_color = '#323232'
		)
	recording_display_favorite_button.place(x=434, y=13)

	whiteboard_display_screen_tag_text = customtkinter.CTkLabel(
		master = recording_display_screen,
		text = 'Tags',
		font = ('Segoe', 14, 'bold')
		)
	whiteboard_display_screen_tag_text.place(x=25, y=520)

	# Personal Tag
	recording_display_screen_tag_personal_button = customtkinter.CTkButton(
		master = recording_display_screen,
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
		font = font,
		command = lambda: tags_light_up(recording_display_screen_tag_personal_button)
			 )
	recording_display_screen_tag_personal_button.place(x=24, y=550)

	# Work Tag
	recording_display_screen_tag_work_button = customtkinter.CTkButton(
		master = recording_display_screen,
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
		font = font,
		command = lambda: tags_light_up(recording_display_screen_tag_work_button)
			 )
	recording_display_screen_tag_work_button.place(x=139, y=550)

	# School Tag
	recording_display_screen_tag_school_button = customtkinter.CTkButton(
		master = recording_display_screen,
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
		font = font,
		command = lambda: tags_light_up(recording_display_screen_tag_school_button)
			 )
	recording_display_screen_tag_school_button.place(x=254, y=550)

	# Other Tag
	recording_display_screen_tag_other_button = customtkinter.CTkButton(
		master = recording_display_screen,
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
		font = font,
		command = lambda: tags_light_up(recording_display_screen_tag_other_button)
			 )
	recording_display_screen_tag_other_button.place(x=369, y=550)

	recording_display_screen_cancel_button = customtkinter.CTkButton(
		master = recording_display_screen,
		command = new_note_cancel,
		text = 'Cancel',
		font=('Segoe', 16),
		width = 110,
		height = 36,
		fg_color = '#474747',
		hover_color = user_button_color_hover,
		background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
			 )
	recording_display_screen_cancel_button.place(x=250, y=600)


# =================================== SETTINGS ==========================================

	settings_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3
		)

	# Settings Text
	settings_text_label = customtkinter.CTkLabel(
		master = settings_screen,
		text = 'Settings',
		bg_color = lgrey,
		font = ('Segoe', 32, 'bold'),
		text_color = '#999999'
		)
	settings_text_label.place(x=20, y=30)

	# User Avatar Change Button
	try:
		current_user_avatar_128 = customtkinter.CTkImage(Image.open(current_user_avatar_path), size=(128, 128))
	except Exception as e:
		current_user_avatar_128 = customtkinter.CTkImage(Image.open(current_path + current_user_avatar_path), size=(128, 128))

	user_avatar_change_button = customtkinter.CTkButton(
		master = settings_screen,
		command = change_user_avatar,
		image = current_user_avatar_128,
		text = '',
		width = 128,
		height = 128,
		fg_color = grey,
		hover_color = '#474747',
		background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
		bg_color = lgrey,
		border_width = 0
			 )
	user_avatar_change_button.place(x=20, y=110)

	# Change Avatar (text)
	change_avatar_text = customtkinter.CTkLabel(
		master = settings_screen,
		text = 'CHANGE AVATAR',
		bg_color = '#323232',
		font=('Segoe', 10, 'bold'),
		text_color = 'white'
		)
	change_avatar_text.place(x=55, y=247)

	# Display Name (text)
	change_user_display_name_label = customtkinter.CTkLabel(
		master = settings_screen,
		text = 'DISPLAY NAME',
		bg_color = '#323232',
		font=('Segoe', 10, 'bold'),
		text_color = 'white'
		)
	change_user_display_name_label.place(x=175, y=105)

	# Display Name TextBox
	change_user_display_name_tb = customtkinter.CTkEntry(
	master = settings_screen,
	width = 200,
	height = 30,
	fg_color = '#282828',
	border_color = user_button_color,
	border_width = 3,
	placeholder_text = current_user_display_name
			)
	change_user_display_name_tb.place(x=175, y=130)

	# Theme color (text)
	theme_color_label = customtkinter.CTkLabel(
	master = settings_screen,
	text = 'THEME COLOR',
	bg_color = '#323232',
	font=('Segoe', 10, 'bold'),
	text_color = 'white'
		)
	theme_color_label.place(x=175, y=159)

	theme_color_button = customtkinter.CTkButton(
	master = settings_screen,
	command = pick_theme_color,
	text = 'Choose...',
	font=('Segoe', 16, 'bold'),
	width = 110,
	height = 36,
	fg_color = user_button_color,
	hover_color = user_button_color_hover,
	background_corner_colors = [lgrey, lgrey, lgrey, lgrey],
	bg_color = lgrey
			 )
	theme_color_button.place(x=175, y=190)

	# (Restart required) (text)
	restart_required_label = customtkinter.CTkLabel(
	master = settings_screen,
	text = '(Restart required)',
	bg_color = '#323232',
	font=('Segoe', 15,),
	text_color = 'white'
		)
	restart_required_label.place(x=300, y=192)

	settings_cancel_button = customtkinter.CTkButton(
	master = settings_screen,
	command = settings_cancel,
	text = 'Back',
	font=('Segoe', 16),
	width = 110,
	height = 36,
	fg_color = '#474747',
	hover_color = '#585858',
	background_corner_colors = ['#323232', '#323232', '#323232', '#323232'],
	bg_color = '#323232'
			 )
	settings_cancel_button.place(x=245, y=330)

	settings_submit_button = customtkinter.CTkButton(
		master = settings_screen,
		command = settings_submit,
		text = 'Submit',
		font=('Segoe', 16, 'bold'),
		width = 110,
		height = 36,
		fg_color = user_button_color,
		hover_color = user_button_color_hover,
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
			 )
	settings_submit_button.place(x=375, y=330)

	trash_image = customtkinter.CTkImage(Image.open(current_path + "/gui/trash_icon.png"), size=(20, 20))
	settings_trash_button = customtkinter.CTkButton(
		master = settings_screen,
		command = show_all_trash,
		text = 'Show Trash',
		image = trash_image,
		font = ('Segoe', 16, 'bold'),
		width = 140,
		height = 36,
		compound = 'left',
		anchor = 'w',
		fg_color = user_button_color,
		hover_color = user_button_color_hover,
		background_corner_colors=['#323232', '#323232', '#323232', '#323232'],
		bg_color = '#323232'
		 )
	settings_trash_button.place(x=25, y=330)	

# ============================================== TRASH =========================================================

	text_note_trash_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3
		)

	# Title Text
	text_note_trash_title_label = customtkinter.CTkLabel(
		master = text_note_trash_display_screen,
		text = 'title',
		bg_color = lgrey,
		font = ('Segoe', 32, 'bold'),
		text_color = 'white'
		)
	text_note_trash_title_label.place(x=20, y=30)

	# Date create Text
	text_note_trash_date_create_label = customtkinter.CTkLabel(
		master = text_note_trash_display_screen,
		text = 'date:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	text_note_trash_date_create_label.place(x=20, y=80)

	# Date edit Text
	text_note_trash_date_edit_label = customtkinter.CTkLabel(
		master = text_note_trash_display_screen,
		text = 'date:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	text_note_trash_date_edit_label.place(x=20, y=130)

	# Favorite Text
	text_note_trash_favorite_label = customtkinter.CTkLabel(
		master = text_note_trash_display_screen,
		text = 'label:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	text_note_trash_favorite_label.place(x=20, y=180)

	# Tags Text
	text_note_trash_tags_label = customtkinter.CTkLabel(
		master = text_note_trash_display_screen,
		text = 'tags:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	text_note_trash_tags_label.place(x=20, y=230)

#  ==================================== trash for whiteboards ========================================

	whiteboard_trash_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3
		)

	# Title Text
	whiteboard_trash_title_label = customtkinter.CTkLabel(
		master = whiteboard_trash_display_screen,
		text = 'title',
		bg_color = lgrey,
		font = ('Segoe', 32, 'bold'),
		text_color = 'white'
		)
	whiteboard_trash_title_label.place(x=20, y=30)

	# Date create Text
	whiteboard_trash_date_create_label = customtkinter.CTkLabel(
		master = whiteboard_trash_display_screen,
		text = 'date:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	whiteboard_trash_date_create_label.place(x=20, y=80)

	# Date edit Text
	whiteboard_trash_date_edit_label = customtkinter.CTkLabel(
		master = whiteboard_trash_display_screen,
		text = 'date:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	whiteboard_trash_date_edit_label.place(x=20, y=130)

	# Favorite Text
	whiteboard_trash_favorite_label = customtkinter.CTkLabel(
		master = whiteboard_trash_display_screen,
		text = 'label:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	whiteboard_trash_favorite_label.place(x=20, y=180)

	# Tags Text
	whiteboard_trash_tags_label = customtkinter.CTkLabel(
		master = whiteboard_trash_display_screen,
		text = 'tags:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	whiteboard_trash_tags_label.place(x=20, y=230)

#  ==================================== trash for recordings ========================================

	recording_trash_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_width = 3
		)

	# Title Text
	recording_trash_title_label = customtkinter.CTkLabel(
		master = recording_trash_display_screen,
		text = 'title',
		bg_color = lgrey,
		font = ('Segoe', 32, 'bold'),
		text_color = 'white'
		)
	recording_trash_title_label.place(x=20, y=30)

	# Date create Text
	recording_trash_date_create_label = customtkinter.CTkLabel(
		master = recording_trash_display_screen,
		text = 'date:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	recording_trash_date_create_label.place(x=20, y=80)

	# Duration Text
	recording_trash_duration_label = customtkinter.CTkLabel(
		master = recording_trash_display_screen,
		text = 'dur:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	recording_trash_duration_label.place(x=20, y=130)

	# Favorite Text
	recording_trash_favorite_label = customtkinter.CTkLabel(
		master = recording_trash_display_screen,
		text = 'label:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	recording_trash_favorite_label.place(x=20, y=180)

	# Tags Text
	recording_trash_tags_label = customtkinter.CTkLabel(
		master = recording_trash_display_screen,
		text = 'tags:',
		bg_color = lgrey,
		font = ('Segoe', 16),
		text_color = 'white'
		)
	recording_trash_tags_label.place(x=20, y=230)

# =================================== STATISTICS SCREEN =================================

	statistics_display_screen = customtkinter.CTkFrame(
		master = app,
		width = 500,
		height = 650,
		bg_color = '#323232',
		fg_color = '#323232',
		border_color = user_button_color,
		border_width = 3
	)

	statistics_display_screen_text_icon = customtkinter.CTkButton(
		master = statistics_display_screen,
		text = '',
		image = text_image,
		fg_color = lgrey,
		background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
		bg_color = lgrey,
		border_width = 0,
		border_spacing = 0,
		width = 20,
		height = 20,
		hover_color = lgrey
		 )
	statistics_display_screen_text_icon.place(x=338, y=182)	

	statistics_display_screen_whiteboard_icon = customtkinter.CTkButton(
		master = statistics_display_screen,
		text = '',
		image = whiteboards_image,
		fg_color = lgrey,
		background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
		bg_color = lgrey,
		border_width = 0,
		border_spacing = 0,
		width = 20,
		height = 20,
		hover_color = lgrey
		 )
	statistics_display_screen_whiteboard_icon.place(x=383, y=182)	

	statistics_display_screen_recording_icon = customtkinter.CTkButton(
		master = statistics_display_screen,
		text = '',
		image = recordings_image,
		fg_color = lgrey,
		background_corner_colors=[lgrey, lgrey, lgrey, lgrey],
		bg_color = lgrey,
		border_width = 0,
		border_spacing = 0,
		width = 20,
		height = 20,
		hover_color = lgrey
		 )
	statistics_display_screen_recording_icon.place(x=428, y=182)

	# Statistics Text
	statistics_display_screen_text_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Statistics',
		bg_color = lgrey,
		font = ('Segoe', 32, 'bold'),
		text_color = '#999999'
		)
	statistics_display_screen_text_label.place(x=20, y=30)

	# total # of notes Text
	statistics_display_screen_total_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Total number of notes: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = '#474747',
		width = 300,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_total_label.place(x=3, y=90)

	# total of text Text
	statistics_display_screen_total_text_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Text notes: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 300,
		anchor = 'w',
		padx = 50
		)
	statistics_display_screen_total_text_label.place(x=3, y=120)

	# total of whiteboard Text
	statistics_display_screen_total_whiteboard_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Whiteboards: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 300,
		anchor = 'w',
		padx = 50
		)
	statistics_display_screen_total_whiteboard_label.place(x=3, y=150)

	# total of recording Text
	statistics_display_screen_total_recording_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Recordings: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 300,
		anchor = 'w',
		padx = 50
		)
	statistics_display_screen_total_recording_label.place(x=3, y=180)

	# shortest Text
	statistics_display_screen_shortest_text_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Shortest text note: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_shortest_text_label.place(x=3, y=230)

	# longest Text
	statistics_display_screen_longest_text_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Longest text note: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_longest_text_label.place(x=3, y=260)

	# avg Text
	statistics_display_screen_average_text_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Average length: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_average_text_label.place(x=3, y=290)

	# shortest rec
	statistics_display_screen_shortest_rec_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Shortest recording: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_shortest_rec_label.place(x=3, y=340)

	# longest rec
	statistics_display_screen_longest_rec_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Longest recording: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_longest_rec_label.place(x=3, y=370)

	# avg rec
	statistics_display_screen_average_rec_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Average length: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_average_rec_label.place(x=3, y=400)

	# total rem
	statistics_display_screen_total_reminder_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Total number of reminders: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_total_reminder_label.place(x=3, y=450)

	# total contacts
	statistics_display_screen_total_contact_label = customtkinter.CTkLabel(
		master = statistics_display_screen,
		text = 'Total number of contacts: ',
		font = ('Segoe', 15, 'bold'),
		text_color = 'white',
		bg_color = get_hover_color('#474747'),
		width = 493,
		anchor = 'w',
		padx = 20
		)
	statistics_display_screen_total_contact_label.place(x=3, y=500)


# =======================================================================================

	# List of All Buttons
	button_list = [all_notes_button, reminders_button, favorites_button, statistics_button,
	text_button, recordings_button, whiteboards_button, contacts_button, history_button, settings_button,
	personal_button, work_button, school_button, other_button]

	# List of All Frames
	frame_list = [default_frame, all_notes_frame, reminders_frame, contacts_frame, favorites_frame, 
	only_text_notes_frame, history_frame, only_work_frame, only_personal_frame, only_recordings_frame,
	only_whiteboards_frame, only_school_frame, only_other_frame, trash_frame, search_results_frame]

	# List of ShowScreens
	screen_list = [add_content_screen, add_text_note_screen, text_note_display_screen, add_contact_screen,
	contact_display_screen, add_whiteboard_screen, add_reminder_screen, whiteboard_display_screen, add_recording_screen,
	reminder_display_screen, recording_display_screen, settings_screen, text_note_trash_display_screen,
	whiteboard_trash_display_screen, recording_trash_display_screen, statistics_display_screen]

	#run app
	app.mainloop()

run_login_page()