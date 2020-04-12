from ._anvil_designer import MatchesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ConfirmMatch import ConfirmMatch

from .Globals import green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class MatchesRow(MatchesRowTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.users.get_user()
    # Any code you write here will run when the form opens.

  def volunteer_toggle_status(self, **event_args):
      """This method is called when the Volunteer Toggle CheckBox is shown on the screen"""
      if self.user in self.item['available_runners']:
          event_args['sender'].checked = True
          event_args['sender'].text = "You volunteered.\nUntick to cancel."
      else:
          event_args['sender'].checked = False
          event_args['sender'].text = "Tick to volunteer"
      self.volunteers.foreground = red if self.volunteers.text.startswith("0 ") else blue

  def volunteer_toggle_change(self, **event_args):
    """This method is called when this Volunteer Toggle checkbox is checked or unchecked"""
    if event_args['sender'].checked:
        anvil.server.call("volunteer_as_runner", self.item, True)
    else:
        anvil.server.call("volunteer_as_runner", self.item, False)
    self.refresh_data_bindings()
    self.volunteer_toggle_status(**event_args)
        

  def show_myself(self, **event_args):
      """This method is called when the data row panel is shown on the screen"""
      user = anvil.users.get_user()

      if self.item['request']['user'] == user:
          self.label_1.text  = "My Request"
          self.label_1.foreground = green
          self.label_4.foreground = green
          self.dropoff.foreground = green
          self.dropoff.icon = 'fa:home'
          self.request.foreground = green
          self.request_notes.foreground = green        

      if self.item['offer']['user'] == user:
          self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
          self.label_2.text  = "My Offer"
          self.label_2.foreground = green
          self.label_3.foreground = green        
          self.pickup.foreground = green
          self.pickup.icon = 'fa:home'
          self.offer.foreground = green
          self.offer_notes.foreground = green
          self.confirm_match.visible = True
          self.volunteer_toggle.visible = False

  def confirm_match_click(self, **event_args):
      """This method is called when the Select Volunteer button is clicked"""
      self.confirm_match.visible = False
      new_form = ConfirmMatch()
      self.flow_panel_1.add_component(new_form, column=None)
      self.flow_panel_1.visible = True
      user = anvil.users.get_user()
      requester = self.item['request']['user']
      new_form.requester = requester
      new_form.telephone_to_requester.checked = requester in (user['telephone_shared_with'] or [])
      new_form.telephone_to_requester.text = requester['display_name'] + " (Requester)"
      new_form.email_to_requester.checked = requester in (user['email_shared_with'] or [])
      new_form.email_to_requester.text = requester['display_name'] + " (Requester)"
      new_form.postcode_to_requester.checked = requester in (user['postcode_shared_with'] or [])
      new_form.postcode_to_requester.text = requester['display_name'] + " (Requester)"
      new_form.runner_dropdown.items = [f"{user['display_name']} (myself)"] + [x['display_name'] for x in self.item['available_runners']]





