from ._anvil_designer import ConfirmMatchTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

from ....Globals import LOCALE, ADDRESSES
from ....Globals import green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class ConfirmMatch(ConfirmMatchTemplate):

    def __init__(self, requester, runners, row_id, CHAT_BLURB, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.requester = requester
        self.runner_dropdown.items = runners
        self.user = anvil.users.get_user()
        self.row_id = row_id
        self.chat_blurb = CHAT_BLURB
        self.telephone.enabled = True if self.user['telephone'] else False
        self.postcode.enabled = True if self.user['postcode'] else False

    def dropdown_change(self, **event_args):
        """ Colour codes dropdown box """
        runner = event_args['sender'].selected_value
        if runner not in event_args['sender'].items:
            event_args['sender'].background = pink
        else:
            event_args['sender'].background = white
        self.confirm_match_button.enabled = self.runner_dropdown.selected_value in self.runner_dropdown.items
        self.refresh_data_bindings()

    def exit(self, **event_args):
        """This method is called when the button is clicked"""
        self.parent.parent.parent.show_myself()
#         self.parent.parent.visible = False
        self.clear()
        self.visible = False

    def confirm_match_button_click(self, **event_args):
        """This method is called when the Confirm Match button is clicked"""      
        runner = anvil.server.call("get_user_from_display_name", self.runner_dropdown.selected_value.replace(" (myself)",""))
        self.update_shared_with_fields(self.user, runner)
        self.update_databases(runner)
        self.parent.parent.parent.show_myself()
        self.parent.parent.visible = False
        self.clear()
        self.visible = False
        
    def add_remove_sharing(self, user, dictionary, recipient):
        """ Adds or Removes a user in the shared_with column """
        for field, checked in dictionary.items():
            users = list(set((self.user[field] or []) + [recipient]))
            if not checked:
                users = users.remove(recipient)
            anvil.server.call('save_user_setup', field, users)
        

      
            
    def update_shared_with_fields(self, user, runner):
        """ Update 'shared_with' for Runner """
        # Update 'shared_with' for Runner and Requester
        sharing_dict = {'telephone_shared_with': self.telephone.checked,
                      'email_shared_with': self.email.checked,
                      'postcode_shared_with': self.postcode.checked,}
        self.add_remove_sharing(self.user, sharing_dict, runner)
        self.add_remove_sharing(self.user, sharing_dict, self.requester)
        
    def create_message(self):
        message = ""
        message += "\n> " + self.user['telephone'] if self.telephone.checked else ""
        message += "\n> " + self.user['email'] if self.email.checked else ""
        message += "> You can contact me on:" + message if message != "" else ""
        message += f"\n({self.user['display_name']} at " if message !="" else ""
        message += datetime.datetime.now().strftime("%d %b %Y on %H:%M)\n\n") if message !="" else ""      
        message += self.chat_blurb
        print(message)
        anvil.server.call('save_to_chat', self.row_id, message)   
        
             
    def update_databases(self, runner):
        """ Sets Approved Runner, updates Matches/Offers/Requests, and refreshes the view """
        status_dict = self.parent.parent.parent.item['status_dict']
        status_dict['runner_selected'] = True
        # TODO: Change parent.parent etc. to passing in match as 
        anvil.server.call("save_to_matches_database", self.parent.parent.parent.item, runner, status_dict)
        anvil.server.call('update_status_codes', self.parent.parent.parent.item, "Match Confirmed")
        anvil.server.call('generate_matches')
        self.create_message()
        self.parent.parent.parent.refresh_data_bindings()     

      




























