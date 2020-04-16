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
    self.is_offerer.checked = self.user == self.match['offer']['user']
    self.is_runner.checked = self.user == self.match['approved_runner']
    self.is_requester.checked = self.user == self.match['request']['user']
    if self.match['approved_runner']:
        self.runner_selected.checked = True
    self.layout_rules()
    self.initial_canvas() 
    self.dynamic_canvas()    

    
  def initial_canvas(self):
    self.offer_matched.checked = True
    for component in self.card_1.get_components():
        component.background = bright_blue
        component.foreground = white
        component.enabled = False
        component.bold = True
        component.spacing_above = 'none'
        component.spacing_below = 'none'
    self.card_1.background = light_blue
    self.complete.background = red
    self.offerer.background = dark_blue
    self.runner.background = dark_blue
    self.requester.background = dark_blue
    self.offerer.text = "Offerer: " + self.match['offer']['user']['display_name']
    self.runner.text = "Runner: " + self.match['approved_runner']['display_name']
    self.requester.text = "Requester: " + self.match['request']['user']['display_name']
    components = set()
    if self.is_runner.checked:
        components.update({self.runner_confirms_pickup, self.runner_confirms_dropoff, self.dropoff_agreed, self.pickup_agreed})
    if self.is_offerer.checked:
        components.update({self.offerer_confirms_pickup, self.pickup_agreed})
    if self.is_requester.checked:
        components.update({self.requester_confirms_dropoff, self.dropoff_agreed})
    for component in components:
        component.
        
  def dynamic_canvas(self, **event_args):
    """This method is called when the column panel is shown on the screen"""

    # Run Layout Rules
    for component in self.card_1.get_components():
      if hasattr(component, "_action"):
        component._action(sender=component)
        print(component._action)
    self.rules_for_style()
    
  def layout_rules(self):
      ARROWS = self.rule_for_arrows
      TICK = self.rule_for_checkbox_tick
      ENABLE = self.rule_for_enabling
      rules = [
               (self.offer_matched, ARROWS, [self.arrow1]),
               (self.runner_selected, ARROWS, [self.arrow2]),
               (self.pickup_agreed, ARROWS, [self.arrow3]),
               (self.dropoff_agreed, ARROWS, [self.arrow4,self.arrow5]),
               (self.runner_confirms_pickup, ENABLE, [self.feedback_on_offerer_by_runner]),
               (self.offerer_confirms_pickup, ENABLE, [self.feedback_on_runner_by_offerer]),
               (self.runner_confirms_dropoff, ENABLE, [self.feedback_on_requester_by_runner]),]     
      for component, action, target_list in rules:
          component._target_list = target_list
          component._action = action
          component.set_event_handler("change", action)

          
  def rule_for_checkbox_tick(self, **event_args):
        component = event_args['sender']
        if component.checked:
          for item in component._target_list:
            item.checked = True
          
  def rule_for_arrows(self, **event_args):
        component = event_args['sender']
        if component.checked:
          for arrow in component._target_list:
            arrow.foreground = black
            
  def rule_for_enabling(self, **event_args):
        component = event_args['sender']
        print("Enabling",component.__name__)
        if component.checked:
          for item in component._target_list:
                  item.enabled = True
  
  def rules_for_style(self):            
    for component in self.card_1.get_components():
        if hasattr(component, "enabled"):
            if not component.enabled and component not in (self.offerer, self.runner, self.requester):
                component.foreground = light_blue
                component.italic = True
        if hasattr(component, "checked"):
            if component.checked:
                component.foreground = black
                component.bold = True
          





              

