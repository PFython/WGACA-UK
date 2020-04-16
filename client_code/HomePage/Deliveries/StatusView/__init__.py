from ._anvil_designer import StatusViewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....Globals import green, grey, red, black, dark_green, dark_blue,blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class StatusView(StatusViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    self.match = anvil.server.call('_get_all_matches')[0] # Test data
    self.user = anvil.users.get_user()
    self.is_offerer = self.user == self.match['offer']['user']
    self.is_runner = self.user == self.match['approved_runner']
    self.is_requester = self.user == self.match['request']['user']
    self.build_status_view()

    
  def setup_static_view(self):
    self.offer_matched.checked = True
    for component in self.card_1.get_components():
        component.background = bright_blue
        component.foreground = white
        component.enabled = False
        component.spacing_above = 'none'
        component.spacing_below = 'none'
    self.card_1.background = light_blue
    self.successful.background = green
    self.unsuccessful.background = red
    self.offerer.background = dark_blue
    self.runner.background = dark_blue
    self.requester.background = dark_blue
    self.offerer.bold = True
    self.runner.bold = True
    self.requester.bold = True
    self.offerer.text = "Offerer: " + self.match['offer']['user']['display_name']
    self.runner.text = "Runner: " + self.match['approved_runner']['display_name']
    self.requester.text = "Requester: " + self.match['request']['user']['display_name']

  def build_status_view(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.setup_static_view()
    if self.match['approved_runner']:
        self.runner_selected.checked = True
    if self.is_runner:
        self.runner_confirms_pickup.enabled = True
        self.runner_confirms_dropoff.enabled = True
        self.feedback_on_offerer_by_runner.enabled = True
        self.feedback_on_requester_by_runner.enabled = True
        self.dropoff_agreed.enabled
    for component in self.card_1.get_components():
        if hasattr(component, "enabled"):
            if not component.enabled:
                component.foreground = grey
                component.italic = True
        if hasattr(component, "checked"):
            if component.checked:
                component.foreground = black
                component.bold = True


              

