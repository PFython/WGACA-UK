from ._anvil_designer import StatusViewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....Globals import green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class StatusView(StatusViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    self.setup_view()
    # Test data
    match = anvil.server.call('_get_all_matches')[0]
    print(match)
    
    
  def setup_view(self):
    for component in self.card_1.get_components():
        component.background = bright_blue
        component.foreground = white
        component.enabled = False
    self.card_1.background = light_blue
    self.successful.background = green
    self.unsuccessful.background = red

  def show_status_view(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    pass

