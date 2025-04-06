from objc_util import *
import re
import time

class SyntaxHighlighter:

	def __init__(self, syntax, theme, text_view, tvo):

		self.syntax = syntax(theme)
		self.theme = theme
		self.tv = text_view
		self.tvo = tvo
		self.refresh_timer = None
		self.all_wrappers = []
		self.cached_strings = []
		self.updating = False
		self.wait = .5
		self.last_call_time = 0 

	def refresh(self, highlight_range, initial=False):
		if initial:
			self._refresh(highlight_range=highlight_range)
			return 
		current_time = time.time()
		if current_time - self.last_call_time >= self.wait:
			self.last_call_time = current_time
			self._refresh(highlight_range=highlight_range)

	def _refresh(self, highlight_range=None, initial=False):
		str_obj = self._get_cached_string(self.tv.text)
		font_attr = ObjCInstance(c_void_p.in_dll(c, 'NSFontAttributeName'))
		color_attr = ObjCInstance(c_void_p.in_dll(c, 'NSForegroundColorAttributeName'))

		str_obj.addAttribute_value_range_(
			font_attr, 
			self.theme['font']['regular'], 
			NSRange(0, len(self.tv.text)))

		str_obj.addAttribute_value_range_(
			color_attr, 
			self.theme['foreground_color'],
			NSRange(0, len(self.tv.text)))
		
		if self.refresh_timer is not None:
			self.refresh_timer.cancel()

		self._performRefresh(
			str_obj,
			self.tv.text,
			0,
			self.syntax.syntax,
			font_attr,
			color_attr,
			initial=True)

		self._updateView(str_obj, highlight_range=highlight_range)

	def _get_cached_string(self, text):
		if self.cached_strings:
			# Reuse the last cached string if it's the same length
			cached_str = self.cached_strings.pop()
			if cached_str.length() == len(text):
				cached_str.mutableString().setString_(text)
				return cached_str
		return ObjCClass('NSMutableAttributedString').alloc().initWithString_(text)

	def _performRefresh(self, str_obj, substring, offset, syntax_scope, font_attr, color_attr, initial=False, highlight_range=None):
	
		if initial: # block indentation
			font = self.theme['font']['regular']
			paragraph_style = ObjCClass('NSMutableParagraphStyle').new()
			for tab in re.finditer('(\t+)(.*?)\n', substring):
				text_obj = ObjCClass('NSMutableAttributedString').alloc().initWithString_(tab.group(1))
				text_obj.addAttribute_value_range_(
					ObjCInstance(c_void_p.in_dll(c,'NSFontAttributeName')), 
					font,
					NSRange(0,len(tab.group(1))))
				paragraph_style.setHeadIndent_(text_obj.size().width)
				str_obj.addAttribute_value_range_(
					ObjCInstance(c_void_p.in_dll(c,'NSParagraphStyleAttributeName')),
					paragraph_style,
					NSRange(tab.start(), tab.end() - tab.start()))
		for item in syntax_scope:
			scope = syntax_scope[item]
			matches = scope['pattern'].finditer(substring)
			for m in matches:
				start, end = m.span()
				length = end - start
				self_attr = scope['self'] 
				if 'font' in self_attr:
					str_obj.addAttribute_value_range_(font_attr, self_attr['font'], NSRange(start+offset, length))
				if 'color' in self_attr:
					str_obj.addAttribute_value_range_(color_attr, self_attr['color'], NSRange(start+offset, length))
				if 'groups' in self_attr:
					for group in self_attr['groups']:
						str_obj.addAttribute_value_range_(color_attr, self_attr['groups'][group],
							NSRange(m.start(group)+offset,
								m.end(group) - m.start(group)))
				if 'scoped' in scope:
					self._performRefresh(
						str_obj,
						substring[start:end],
						start + offset,
						scope['scoped'],
						font_attr,
						color_attr)

	@on_main_thread
	def _updateView(self, str_obj, highlight_range=None):
		current_position = self.tv.selected_range[0]
		self.tvo.setAllowsEditingTextAttributes_(True)
		self.tvo.setAttributedText_(str_obj)
		bg_color_attr = ObjCInstance(c_void_p.in_dll(c, 'NSBackgroundColorAttributeName'))

		if current_position < len(self.tv.text) - 1:			
			self.tvo.setSelectedRange_(NSRange(current_position, 0))
			self.tvo.scrollRangeToVisible(NSRange(current_position, 0))
		if highlight_range and 'highlight_color' in self.theme:
			length = highlight_range[1] - highlight_range[0]
			# workaround
			if length >= len(self.tv.text):
				length = len(self.tv.text) - 1
			str_obj.addAttribute_value_range_(
				bg_color_attr, 
				self.theme['highlight_color'],
				NSRange(highlight_range[0], length))
