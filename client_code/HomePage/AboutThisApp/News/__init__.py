from ._anvil_designer import NewsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....Globals import blue, bright_blue

class News(NewsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.title.background = bright_blue
    self.card_2.background = bright_blue
    # Any code you write here will run when the form opens.
    

  def click_previous_updates(self, **event_args):
      """This method is called when the link is clicked"""
      if event_args['sender'].icon == 'fa:caret-down':
          self.previous_updates.visible = True
          event_args['sender'].icon = 'fa:caret-up'
      else:
          self.previous_updates.visible = False
          event_args['sender'].icon = 'fa:caret-down'

