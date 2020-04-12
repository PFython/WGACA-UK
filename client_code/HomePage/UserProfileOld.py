from ._anvil_designer import UserProfileOldTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .TermsOfUse import TermsOfUse
from . import green

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)

class UserProfileOld(UserProfileOldTemplate):
    addresses = ADDRESSES
    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.privacy_notice.text = TermsOfUse().privacy_notice.text
        self.terms_accepted.text = "You accepted this Privacy Notice & Terms of Use on "
        self.terms_accepted.text += anvil.users.get_user()['terms_accepted'].strftime('%d %b %Y')
        self.show_my_details()
        
    def show_my_details(self, **event_args):
        """ Populates User Profile page from User database """
        user = anvil.users.get_user()
        self.id.text = user.get_id()
        self.display_name.text = user['display_name']
        self.email.text = user['email']
        self.house_number.text = user['house_number']
        self.street.text = user['street']
        self.town.text = user['town']
        self.county.text = user['county']
        self.country.text = user['country']
        self.postcode.text = user['postcode']
        self.postcode.tag = "Optional"
        self.telephone.text = user['telephone']
        self.telephone.tag = "Optional"

    def view_history_click(self, **event_args):
        """This method is called when the View Transaction History button is clicked"""
        alert("This feature is still being worked on...\nPlease check back later.")

    def delete_account_click(self, **event_args):
        """This method is called when the Delete Account button is clicked"""
        alert("This feature is still being worked on...\nPlease check back later.")

    def log_out(self, **event_args):
        """This method is called when the Log Out button is clicked"""
        anvil.users.logout()
        anvil.users.login_with_form()
        self.parent.parent.__init__()
        self.parent.parent.menu_my_data_click()
         
    def field_change(self, **event_args):
        """ Highlights empty input boxes"""
        if event_args['sender'].text == "":
            if event_args['sender'].tag == "Optional":
                event_args['sender'].background = '#fefdc7'
            else:
                event_args['sender'].background = '#ffe6e6'
        else:
            event_args['sender'].background = white

    def deselect_all_icons(self):
        """ Set all icons to unselected """
        components = [self.help0, self.help1, self.help2, self.help3,
                      self.help4, self.help5, self.help6,
                      self.help7, self.help8, self.help9]
        for component in components:
            setattr(component, 'icon', 'fa:question')
            
    def show_help_tag(self, **event_args):
        """This method is called when the link is clicked"""
        self.help_text.text = event_args['sender'].tag
        self.deselect_all_icons()
        # Set clicked icon to selected
        event_args['sender'].icon = 'fa:question-circle'            

    def save_optional_field(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.deselect_all_icons()
        value = event_args['sender'].text
        field = {self.postcode: "postcode", self.telephone: 'telephone'}[event_args['sender']]
        anvil.server.call("save_user_setup", field, value)
        self.help_text.text = f"Your new {field.title()} details are: {value or '<empty>'}"

    def expand_privacy_notice(self, **event_args):
      """This method is called when the link is clicked"""
      if self.label_privacy.icon == "fa:caret-down":
          self.privacy_notice.visible = True
          self.label_privacy.icon = "fa:caret-up"
      else:
          self.privacy_notice.visible = False
          self.label_privacy.icon = "fa:caret-down"




