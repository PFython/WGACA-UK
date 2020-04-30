from ._anvil_designer import AutocompleteTemplate
from anvil import *
import anvil.server

class Autocomplete(AutocompleteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    self.repeating_panel_1.set_event_handler('x-option_clicked', self.option_clicked)
    # Initial number of autocomplete suggestions to show
    self.max_options = 10
    # Number of characters required before initial Server call
    self.min_length = 5    
    
# MODEL (Data)
    
  def initial_fetch(self, text):
    """Initial server call to get results matching the first word or N characters"""
    # max_options argument = 99999 to fetch all (realistically) possible matches
    self.options = anvil.server.call("get_initial_address_matches", text, 99999)
    self.match_count = len(self.options)
    return [{'text':option.title()} for option in self.options]
  
# CONTROL (Main Process Flow)

  def text_box_1_change(self, **event_args):
    """This method is called when the text in text_box_1 is edited"""
    self.repeating_panel_1.visible = True
    text = self.text_box_1.text.lower()
    # I wanted to use .casefold() here but not supported
    if len(text) < self.min_length and not text.endswith(" "):
        # Wait for first full word or N characters to be entered for a good match
        matching_rows = [{'text': f"Please enter at least {self.min_length} characters or a whole word, then select from the options..."}]
        self.match_count = 0
        self.show_all = True
        self.options = []
    elif not self.options:
        # Initial fetch hasn't happened yet
        matching_rows = self.initial_fetch(text)
        self.match_count = len(matching_rows)
        # This will also set self.options to all (realistically) possible matches
        self.show_all = False
    else:
        matching_rows = []
        for option in self.options:
          if option.lower().startswith(text):
            # Instead of .startswith() you could use Regex here or 'x in y'.
            matching_rows.append({'text':option.title()})
        self.match_count = len(matching_rows)
        if len(matching_rows) < self.max_options:
            matching_rows+=( [{'text':' '}] * (self.max_options-len(matching_rows)))            
    if self.show_all:
      self.repeating_panel_1.items = matching_rows
    else:
      self.repeating_panel_1.items = matching_rows[:self.max_options]
    self.results_summary()
    self.show_only_valid_components()
    
  # VIEW (Front End and Navigation)
  
  def text_box_1_show(self, **event_args):
    self.text_box_1_change()
    self.text_box_1.focus()    
    
  def show_only_valid_components(self):
      for row in self.repeating_panel_1.get_components():
          row.visible = False if row.item['text'] == " " else True
      if self.match_count == 1:
        self.button_1.enabled = True
    
  def results_summary(self):
    if self.match_count <= self.max_options:
      self.link_1.icon = "fa:empty"
      options = self.match_count
    if self.match_count > self.max_options:
      self.link_1.icon = "fa:caret-up" if self.show_all else "fa:caret-down"
      options = self.match_count if self.show_all else self.max_options
    self.link_1.text = f"{options} out of {self.match_count} result"
    self.link_1.text += "s" if self.match_count != 1 else ""
    
  def option_clicked(self,option,**event_args):
    self.text_box_1.text = option
    self.text_box_1_change()
    self.text_box_1.focus()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.button_1.enabled:
        last_option = self.repeating_panel_1.get_components()[0].item['text']
        self.text_box_1.text = last_option
        alert(f"Your final selection was:\n\n{self.text_box_1.text}")

  def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      self.show_all = True if not self.show_all else False
      self.text_box_1_change()