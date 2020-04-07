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
        self.message_to_requester.tag = "Optional"
        self.message_to_runner.tag = "Optional"

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
      
    def dropdown_change(self, **event_args):
        """ Colour codes dropdown box """
        runner = event_args['sender'].selected_value
        if runner not in event_args['sender'].items:
            event_args['sender'].background = '#ffe6e6'
        else:
            event_args['sender'].background = '#ffffff'
            user = anvil.users.get_user()
            if runner.replace(" (myself)","") != user['display_name']:
                self.telephone_to_runner.checked = runner in [x['display_name'] for x in (user['telephone_shared_with'] or [])]
                self.telephone_to_runner.text = runner + " (Runner)"
                self.email_to_runner.checked = runner in [x['display_name'] for x in (user['email_shared_with'] or [])]
                self.email_to_runner.text = runner + " (Runner)"
                self.postcode_to_runner.checked = runner in [x['display_name'] for x in (user['postcode_shared_with'] or [])]
                self.postcode_to_runner.text = runner + " (Runner)"
                self.message_to_runner.visible = True
                self.telephone_to_runner.visible = True
                self.email_to_runner.visible = True
                self.postcode_to_runner.visible = True                
        self.refresh_data_bindings()

    def exit(self, **event_args):
      """This method is called when the button is clicked"""
      self.parent.parent.parent.show_myself()
      self.clear()
      self.visible = False

    def confirm_match_button_click(self, **event_args):
      """This method is called when the Confirm Match button is clicked"""
      user = anvil.users.get_user()
      # Update 'shared_with' for Requester
      requester_dict = {'telephone_shared_with': self.telephone_to_requester.checked,
                    'email_shared_with': self.email_to_requester.checked,
                    'postcode_shared_with': self.postcode_to_requester.checked,
                   }
      for field, checked in requester_dict.items():          
          users = list(set((user[field] or []) + [self.requester]))
          if not checked:
              users = users.remove(self.requester)
          anvil.server.call('save_user_setup', field, users)
      # Update 'shared_with' for Requester
      runner_dict = {'telephone_shared_with': self.telephone_to_runner.checked,
                    'email_shared_with': self.email_to_runner.checked,
                    'postcode_shared_with': self.postcode_to_runner.checked,
                   }
      runner = anvil.server.call("get_user_from_display_name", self.runner_dropdown.selected_value)
      for field, checked in runner_dict.items():
          users = list(set((user[field] or []) + [runner]))
          if not checked:
              users = users.remove(self.runner)
          anvil.server.call('save_user_setup', field, users)
      # Add messages and Telephone/Email/Postcode if granted
      messages = {}
      messages['offerer_to_runner'] = self.message_to_runner.text +"\n\n"
      if self.telephone_to_runner.checked and user['telephone']:
          messages['offerer_to_runner'] += f"\nMy telephone number is: {user['telephone']}"
      if self.email_to_runner.checked:
          messages['offerer_to_runner'] += f"\nMy Email is: {user['email']}"
      if self.postcode_to_runner.checked and user['postcode']:
                messages['offerer_to_runner'] += f"\nMy Postcode is {user['postcode']}"               
      messages['offerer_to_requester'] = self.message_to_requester.text +"\n\n"
      if self.telephone_to_requester.checked and user['telephone']:
          messages['offerer_to_requester'] += f"\nMy telephone number is: {user['telephone']}"
      if self.email_to_requester.checked:
          messages['offerer_to_requester'] += f"\nMy Email is: {user['email']}"
      if self.postcode_to_requester.checked and user['postcode']:
                messages['offerer_to_requester'] += f"\nMy Postcode is {user['postcode']}"          
      print(messages)
      # Confirm Runner, update Matches/Offers/Requests, and refresh view
      anvil.server.call("save_to_matches_database", self.parent.parent.parent.item, runner, messages, "Awaiting Pickup")
      anvil.server.call("update_offers_status", self.parent.parent.parent.item['offer'], "Awaiting Pickup")
      anvil.server.call("update_requests_status", self.parent.parent.parent.item['request'], "Awaiting Pickup")
      anvil.server.call('generate_matches')
      self.parent.parent.parent.refresh_data_bindings()      
      self.exit()




























