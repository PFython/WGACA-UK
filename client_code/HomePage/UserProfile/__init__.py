from ._anvil_designer import UserProfileTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..TermsOfUse import TermsOfUse

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)

class UserProfile(UserProfileTemplate):
    addresses = ADDRESSES
    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.privacy_notice.text = TermsOfUse().privacy_notice.text       
        self.terms_accepted.text = "You accepted the above Privacy Statement & Terms of Use on "
        self.terms_accepted.text += anvil.users.get_user()['terms_accepted'].strftime('%d %b %Y')
        self.show_my_details()
        
    def show_my_details(self, **event_args):
        user = anvil.users.get_user()
        self.display_name.text = user['display_name']
        self.email.text = user['email']
        self.house_number.text = user['house_number']
        self.street.text = user['street']
        self.town.text = user['town']
        self.county.text = user['county']
        self.country.text = user['country']
        self.postcode.text = user['postcode']
        self.telephone.text = user['telephone']

    def view_history_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert("This feature is still being worked on...\nPlease check back later.")

    def delete_account_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert("This feature is still being worked on...\nPlease check back later.")

    def change_password_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert("To change your password we first need to log you out, then log you back in again.\n\nPlease select the 'Forgot your password?' options from the next window.")
        anvil.users.logout()
        anvil.users.login_with_form()

    def telephone_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        if anvil.server.call("update_telephone", self.telephone.text):
            alert("Telephone successfully updated.")
        else:
            alert("Something went wrong while updating phone number.")
            
    def field_change(self, **event_args):
        """ Highlights empty input boxes"""
        if event_args['sender'].text == "":
            if event_args['sender'].tag == "Optional":
                event_args['sender'].background = '#fefdc7'
            else:
                event_args['sender'].background = '#ffe6e6'
        else:
            event_args['sender'].background = '#ffffff'

    def show_help_tag(self, **event_args):
        """This method is called when the link is clicked"""
        self.help_text.text = event_args['sender'].tag
        # Set all icons to unselected
        components = [self.help1, self.help2, self.help3,
                      self.help4, self.help5, self.help6,
                      self.help7, self.help8, self.help9]
        for component in components:
            setattr(component, 'icon', 'fa:question')
        # Set clicked icon to selected
        event_args['sender'].icon = 'fa:question-circle'            





