from ._anvil_designer import UserSetupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class UserSetup(UserSetupTemplate):
    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
  
    def show_my_details(self, **event_args):
        """This method is called when the TextBox is shown on the screen"""
        self.email.text = anvil.users.get_user()['email']
        self.telephone.text = anvil.users.get_user()['telephone']
        self.display_name.text = anvil.users.get_user()['display_name']
        self.house_number.text = anvil.users.get_user()['house_number']
        self.street.text = anvil.users.get_user()['street']
        self.town.text = anvil.users.get_user()['town']
        self.county.text = anvil.users.get_user()['county']
        self.postcode.text = anvil.users.get_user()['postcode']








