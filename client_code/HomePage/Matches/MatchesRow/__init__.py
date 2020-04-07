from ._anvil_designer import MatchesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ConfirmMatch import ConfirmMatch

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
      self.volunteers.foreground = '#ff8080' if self.volunteers.text.startswith("0 ") else '#0080c0'

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
    # Green: #5eb348
    # Blue: #0080c0
    # Red: #ff8080
    if self.item['request']['user'] == user:
        self.label_1.text  = "My Request"
        self.label_1.foreground = '#5eb348'
        self.label_4.foreground = '#5eb348'
        self.dropoff.foreground = '#5eb348'
        self.dropoff.icon = 'fa:home'
        self.request.foreground = '#5eb348'
        self.request_notes.foreground = '#5eb348'
        

    if self.item['offer']['user'] == user:
        self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
        self.label_2.text  = "My Offer"
        self.label_2.foreground = '#5eb348'
        self.label_3.foreground = '#5eb348'        
        self.pickup.foreground = '#5eb348'
        self.pickup.icon = 'fa:home'
        self.offer.foreground = '#5eb348'
        self.offer_notes.foreground = '#5eb348'
        self.confirm_match.visible = True
        self.volunteer_toggle.visible = False

  def confirm_match_click(self, **event_args):
      """This method is called when the Select Volunteer button is clicked"""
      self.confirm_match.visible = False
#       self.confirm_match_container.visible = True
      new_form = ConfirmMatch()
      self.add_component(new_form, column=0)
#       self.flow_panel_1.visible = True
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






