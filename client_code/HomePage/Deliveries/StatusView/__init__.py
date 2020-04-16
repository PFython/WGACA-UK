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
        component.bold = True
        component.spacing_above = 'none'
        component.spacing_below = 'none'
#         try:
#           component.set_event_handler("change", self.build_status_view)
#         except:
#           pass
    self.card_1.background = light_blue
    self.complete.background = red
    self.offerer.background = dark_blue
    self.runner.background = dark_blue
    self.requester.background = dark_blue
    self.offerer.text = "Offerer: " + self.match['offer']['user']['display_name']
    self.runner.text = "Runner: " + self.match['approved_runner']['display_name']
    self.requester.text = "Requester: " + self.match['request']['user']['display_name']

  def build_status_view(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.setup_static_view()
    if self.match['approved_runner']:
        self.runner_selected.checked = True
#     self.update_offerer()
    self.update_runner()
#     self.update_requester()
    for component in self.card_1.get_components():
        if hasattr(component, "enabled"):
            if not component.enabled and component not in (self.offerer, self.runner, self.requester):
                component.foreground = light_blue
                component.italic = True
        if hasattr(component, "checked"):
            if component.checked:
                component.foreground = black
                component.bold = True
    self.update_arrows()
    
  def update_arrows(self):
    lookup = {self.offer_matched: [self.arrow1],
             self.runner_selected: [self.arrow2],
             self.pickup_agreed: [self.arrow3],
             self.dropoff_agreed: [self.arrow4,self.arrow5],
             }
    for component in lookup:
        if component.checked:
          for arrow in lookup[component]:
            arrow.foreground = black
          
  def update_runner(self):
        if self.is_runner:
          self.runner_confirms_pickup.enabled = True
          self.runner_confirms_dropoff.enabled = True
          self.dropoff_agreed.enabled = True
          self.pickup_agreed.enabled = True
        if self.runner_confirms_pickup.checked:
              self.feedback_on_offerer_by_runner.enabled = True
        if self.runner_confirms_dropoff.checked:
          self.feedback_on_requester_by_runner.enabled = True
          self.runner_confirms_pickup.checked = True
          
  def refresh_layout(self):
        triggers = []
        for component in self.get_components():
            if hasattr(component, "_action"):
                triggers += [component]
        lookup = {'enables': }
          
  def layout(self, trigger_list, action, target_list):
     """
     Pseudo-English method for creating dynamic dependencies between
     components in a form: 1...1, 1...n, n...1, and n...n.
     
     For example: layout(checkbox1, "enables", checkbox2)
     When checkbox1 is checked, checkbox2 will be updated too.
     
     This methods just setups up the event handler and additional
     attributes for each component, and works in conjunction with
     refresh_layout() which figures out what to refresh and how.     
     """
     for trigger in trigger_list:
          trigger.set_event_handler("change", self.refresh_layout)
          trigger._target_list = target_list
          trigger._action = action


              

