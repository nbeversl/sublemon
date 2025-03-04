import ui
from objc_util import *
from thefuzz import fuzz

class AutoCompleter:

	def __init__(self, view_width, view_height, layout, theme):
		self.view_height = view_height
		self.search = ui.TextField()
		self.search.text_color = theme['autocompleter']['foreground_color']
		self.search.hidden = True
		self.search.delegate = SearchFieldDelegate()
		self.search.delegate.textfield_did_change = self.textfield_did_change
		self.dropDown = ui.TableView()
		self.dropDown.separator_color = theme['autocompleter']['separator_color']
		tfo = ObjCInstance(self.search).textField()
		tfo.backgroundColor = theme['autocompleter']['search_field_background_color']
		self.search.border_color = theme['autocompleter']['search_field_border_color']
		self.search.border_width = 1
		self.dropDown.delegate = SearchFieldDelegate()
		self.dropDown.delegate.tableview_did_select = self.tableview_did_select
		self.dropDown.hidden = True
		self.size_fields(view_width, view_height, layout)
		self.dropDown.data_source = ListDataSourceCustom([])
		self.dropDown.data_source.theme = theme
		self.reset()

	def textfield_did_change(self, textfield):
		self.update_and_sort_options(textfield)

	def update_and_sort_options(self,
		textfield,
		all_items_updated=False,
		allow_new=False):

		new_entry = textfield.text.lower()
		characters_typed = len(new_entry)
		words_typed = new_entry.split(' ')
		if characters_typed > len(self.current_entry) and not all_items_updated:
			items = list(self.current_items)
		else:
			items = list(self.all_items)

		if len(items) and isinstance(items[0],list):
			items = [i[0] for i in items] # for now no secondaray feautre
		lowered_items = {}

		for i in items:
			lowered_items[i] = {}
			lowered_items[i]['lower'] = i.lower()
			lowered_items[i]['words'] = lowered_items[i]['lower'].split(' ')
		
		first_char_matching_items = [
			i for i in items if len(i) >= characters_typed - 1 and (
				lowered_items[i]['lower'][:characters_typed] == new_entry[:characters_typed])
			]

		partial_matching_items = [
			i for i in items if 
			new_entry in lowered_items[i]['lower'] and i not in first_char_matching_items
			]
		
		word_matching_items = [
			i for i in items if [
				word for word in words_typed if word in lowered_items[i]['words']]
			]

		remaining_items = [
			i for i in items if i not in partial_matching_items and (
				i not in first_char_matching_items ) and (
				i not in word_matching_items )
			]

		fuzzy_options = sorted(
			remaining_items,
			key = lambda option: fuzz.ratio(
				new_entry,
				self.items_comparision[option]) if option in self.items_comparision else 0, 
			reverse=True)
		total_options=[]
		total_options.extend(first_char_matching_items)
		total_options.extend(partial_matching_items)
		total_options.extend(fuzzy_options[:20])
		if len(total_options) > 1 and total_options[0] == total_options[1]:
			total_options = total_options[1:]
		self.current_entry = new_entry
		self._set_current_items(total_options)

	def hide(self):
		self.dropDown.hidden = True
		self.search.hidden = True
		self.reset()

	def reset(self):
		self.search.text=''
		self.all_items = []
		self.current_items = []
		self.items_comparision = {}
		self.allowing_new = False
		self.current_entry = ''
		self.showing = None

	def tableview_did_select(self, tableview, section, selected_row):
		self.search.text = self.dropDown.data_source.items[selected_row]
		original_row = self.all_items.index(self.dropDown.data_source.items[selected_row])
		self.hide()
		return self.action(original_row)

	def _set_current_items(self, items):
		self.current_items = list(items)
		if self.allowing_new and self.current_entry.strip() and (
			self.current_entry.strip() != self.current_items[0]):
			items.insert(0, self.current_entry.strip())
		self.items_comparision = {}
		for item in items:
			self.items_comparision[item] = item.lower()
		self.dropDown.data_source.items = items		
		if len(items):
			max_items_showing = (
				self.view_height - self.search.height 
				) / len(items)
		else:
			max_items_showing = 5
		if len(items) > max_items_showing:
			self.dropDown.height = self.view_height
		else:
			self.dropDown.height = self.search.height * len(items)

	def set_items(self, items, name, allow_new=False):
		self.all_items = items
		if len(items) and isinstance(items[0],list):
			self.all_items = [i[0] for i in items] # for now no secondaray feautre
		self.allowing_new = allow_new
		self.showing = name
		self.update_and_sort_options(self.search, all_items_updated=True)

	def show(self):
		self.search.hidden = False
		self.search.bring_to_front()
		self.search.text=''
		self.dropDown.hidden = False
		self.dropDown.bring_to_front()
		self.dropDown.x = self.search.x
		self.dropDown.y = self.search.y + self.search.height
		self.dropDown.width = self.search.width
		self.dropDown.row_height = self.search.height
		self.search.begin_editing()

	def set_action(self, action):
		self.action = action

	def size_fields(self, view_width, view_height, layout):
		self.search.height = layout['search_box_height']
		self.search.width = view_width * 0.8
		self.search.x = view_width / 10
		self.search.y = layout['text_view_distance_from_top'] + layout['padding']['md']
		self.search.border_width = layout['button_border_width']
		self.dropDown.height = view_height

class SearchFieldDelegate:
	
	def __init__(self):
		pass

class ListDataSourceCustom(ui.ListDataSource):

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]
		cell.text_label.text_color = self.theme['autocompleter']['foreground_color']
		cell.text_label.background_color = self.theme['autocompleter']['background_color']
		cell.background_color = self.theme['autocompleter']['background_color']
		return cell


