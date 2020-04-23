from ._anvil_designer import NewsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Globals import blue, bright_blue

class News(NewsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.previous = [x for x in self.previous_updates.get_components() if type(x) != Link]
    for label in self.previous:
          label.visible = False
    

  def click_previous_updates(self, **event_args):
      """This method is called when the link is clicked"""
      if event_args['sender'].icon == 'fa:caret-down':
          for label in self.previous:
              label.visible = True
          event_args['sender'].icon = 'fa:caret-up'
      else:
          for label in self.previous:
              label.visible = False
          event_args['sender'].icon = 'fa:caret-down'


