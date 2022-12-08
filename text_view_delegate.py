import time

class TextViewDelegate(object):

	def __init__(self, main_view):
		self.last_time = time.time()
		# self.time = time.time()
		self.main_view = main_view

	def textview_did_change(self, textview):
		self.main_view.saved = False
		# now = time.time()
		# if now - self.time > .5:
		self.main_view.refresh_syntax_highlighting()   
		# self.time = time.time()
		
	def textview_did_change_selection(self, textview):
		self.main_view.autoCompleter.hide()

	def textview_did_begin_editing(self, textview):
		self.main_view.autoCompleter.hide()