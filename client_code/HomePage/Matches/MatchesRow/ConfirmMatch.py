from ._anvil_designer import ConfirmMatchTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

from ....Globals import LOCALE, ADDRESSES, green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class ConfirmMatch(ConfirmMatchTemplate):

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.message_to_requester.tag = "Optional"
        self.message_to_runner.tag = "Optional"

#     def confirm_match(self, **event_args):
#       """This method is called when the button is clicked"""
#       self.clear()
#       self.parent.visible = False
#       alert("""Message sent.  Thanks for taking the time to reach out to us!""")
      
    def dropdown_change(self, **event_args):
        """ Colour codes dropdown box """
        runner = event_args['sender'].selected_value
        if runner not in event_args['sender'].items:
            event_args['sender'].background = pink
        else:
            event_args['sender'].background = white
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
        self.parent.parent.visible = False
        self.clear()
        self.visible = False

    def confirm_match_button_click(self, **event_args):
        """This method is called when the Confirm Match button is clicked"""
        user = anvil.users.get_user()
        runner = anvil.server.call("get_user_from_display_name", self.runner_dropdown.selected_value.replace(" (myself)",""))
        self.update_shared_with_fields(user, runner)
        messages = self.create_messages_dict(user)
        print(messages)
        self.update_databases(runner, messages)
        self.exit()
        
    def update_shared_with_fields(self, user, runner):
        """ Update 'shared_with' for Requester """
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
        for field, checked in runner_dict.items():
            users = list(set((user[field] or []) + [runner]))
            if not checked:
                users = users.remove(runner)
            anvil.server.call('save_user_setup', field, users)
        
    def create_messages_dict(self, user):    
        """ Add messages and Telephone/Email/Postcode if granted"""
        messages = {}
        messages['offerer_to_runner'] = self.message_to_runner.text +"\n"
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
        return messages
      
    def update_databases(self, runner, messages):
        """ Sets Approved Runner, updates Matches/Offers/Requests, and refreshes the view """
        anvil.server.call("save_to_matches_database", self.parent.parent.parent.item, runner, messages, "Awaiting Pickup")
        anvil.server.call("update_offers_status", self.parent.parent.parent.item['offer'], "Awaiting Pickup")
        anvil.server.call("update_requests_status", self.parent.parent.parent.item['request'], "Awaiting Pickup")
        anvil.server.call('generate_matches')
        self.parent.parent.parent.refresh_data_bindings()      
      




























