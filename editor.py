import os
import ui
import dialogs
import console
from objc_util import *
from editor.app_single_launch import AppSingleLaunch
from editor.syntax_highlighter import SyntaxHighlighter
from editor.auto_completer import AutoCompleter
from editor.text_view_delegate import TextViewDelegate
from editor.layout import layout
from editor.base_editor_theme import base_editor_theme
from editor.syntax_empty import EmptySyntax
from editor.themes.theme_example import theme_light

class BaseEditor(ui.View):

	layout = layout
	base_editor_theme = base_editor_theme
	name = "Base Editor"

	def __init__(self):

		self.app = AppSingleLaunch(self.name)
		if not self.app.is_active():
			self.current_open_file = None
			self.current_open_file_hash = None
			self.saved = None
			self.width, self.height = ui.get_screen_size()
			self.frame = (0, self.layout['distance_from_top'], self.width,self.height)
			self.init_text_view()
			self.setup_obj_instances()
			self.setup_autocomplete()
			self.setup_syntax_highlighter(EmptySyntax, theme_light)

	def show(self):
		self.present('fullscreen', hide_title_bar=True)
		self.tv.begin_editing()
		self.app.will_present(self)

	def setup_syntax_highlighter(self, syntax, theme):
		self.syntax_highlighter = SyntaxHighlighter(syntax, theme)

	def setup_buttons(self, buttons):
		if not buttons:
			buttons= {
				'Open' : self.open_file,
				'S' : self.manual_save,
				'↓' : self.hide_keyboard,
			}
		self._build_button_line(buttons)

	def setup_autocomplete(self):
		self.autoCompleter = AutoCompleter(
			self.width, self.height, self.layout, self.base_editor_theme)
		self.add_subview(self.autoCompleter.search)
		self.add_subview(self.autoCompleter.dropDown)

	def open_file(self, sender):
		open_file = dialogs.pick_document()
		if open_file:
			with open(open_file, 'r', encoding='utf-8') as d:
				contents = d.read()
			self.tv.text=contents
			self.current_open_file = open_file
			self.current_open_file_hash = hash(contents)

	def init_text_view(self):
		self.tv = ui.TextView()
		self.tv.frame=(
			0, 
			self.layout['distance_from_top'], 
			self.width, 
			self.height)
		self.tv.auto_content_inset = True
		self.tv.background_color = self.base_editor_theme['background_color']
		self.tv.width = self.width
		self.tv.delegate = TextViewDelegate(self)
		self.add_subview(self.tv)

	def _build_button_line(self, buttons):
		button_x_position = 0
		button_y_position = 10
		button_line = ui.View()
		button_line.name = 'buttonLine'
		button_line.background_color = self.base_editor_theme['button_line_background_color']

		for button_character in buttons:
			new_button = ui.Button(title=button_character)
			new_button.action = buttons[button_character]

			new_button.corner_radius = self.layout['button_corner_radius']
			if button_x_position >= self.width :
				button_y_position += self.layout['button_container_height']
				button_x_position = 0
			new_button.frame = (button_x_position, 
				button_y_position, 
				self.layout['button_width'], 
				self.layout['button_height'])
			button_line.add_subview(new_button)
			button_x_position += self.layout['button_width'] + 3
			new_button.border_width = self.layout['button_border_width']
			new_button.border_color = self.base_editor_theme['button_border_color']
			new_button.background_color = self.base_editor_theme['button_background_color']

		self.button_line = button_line
		self.button_line.height = button_line.height + 5 # add margin
		self.add_subview(self.button_line)
		btn_ln = ObjCInstance(self.button_line)
		self.tvo.setInputAccessoryView_(btn_ln)

	def setup_obj_instances(self):
		self.tvo = ObjCInstance(self.tv)
		self.tvo.setAllowsEditingTextAttributes_(True)	

	def hide_keyboard(self, sender):
		self.tv.end_editing()

	def manual_save(self, sender):
		self.save(None)
		console.hud_alert('Saved','success',0.5)

	def save(self, sender):
		if self.saved:
			return
		if self.current_open_file:
			contents = self.tv.text 
			with open(self.current_open_file,'w', encoding='utf-8') as d:
				d.write(contents)
			self.current_open_file_hash = hash(contents)
			self.saved = True
				
	def refresh_syntax_highlighting(self, text=''):   
		self.syntax_highlighter.setAttribs(self.tv, self.tvo, self.theme)
	