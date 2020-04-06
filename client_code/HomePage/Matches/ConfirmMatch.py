from ._anvil_designer import ConfirmMatchTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)

class ConfirmMatch(ConfirmMatchTemplate):
    addresses = ADDRESSES
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.


    def confirm_match(self, **event_args):
      """This method is called when the button is clicked"""
#       app_tables.feedback.add_row(from_user = anvil.users.get_user(),
#                                   date_time = datetime.datetime.now(),
#                                   category = self.category.selected_value,
#                                   title = self.title.text,
#                                   description = self.description.text,
#                                   telephone_ok = self.telephone_ok.checked,
#                                   email_ok = self.email_ok.checked,)
      self.clear()
      self.parent.visible = False
      alert("""Message sent.  Thanks for taking the time to reach out to us!""")

    def cancel_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.clear()
      self.parent.visible = False

    def confirm_match_button_click(self, **event_args):
      """This method is called when the Confirm Match button is clicked"""
      writeback_dict = {'telephone_shared_with': self.telephone_to_requester.checked,
                    'email_shared_with': self.email_to_requester.checked,
                    'postcode_shared_with': self.postcode_to_requester.checked,
                   }
      for field, checked in writeback_dict.items():
          user = anvil.users.get_user()
          users = list(set((user[field] or []) + [self.requester]))
          if not checked:
              users = users.remove(self.requester)
          anvil.server.call('save_user_setup', field, users)
      self.clear()
      # Clean up each Table as required and refresh Matches view


























