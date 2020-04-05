from ._anvil_designer import MatchesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

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
      self.volunteers.foreground = '#ff8080' if self.volunteers.text.startswith("0 ") else '#5eb348'

  def volunteer_toggle_change(self, **event_args):
    """This method is called when this Volunteer Toggle checkbox is checked or unchecked"""
    if event_args['sender'].checked:
        anvil.server.call("volunteer_as_runner", self.item,True)
    else:
        anvil.server.call("volunteer_as_runner", self.item, False)
    self.refresh_data_bindings()
    self.volunteer_toggle_status(**event_args)
        


