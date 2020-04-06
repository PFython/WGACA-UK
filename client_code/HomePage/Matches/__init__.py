from ._anvil_designer import MatchesTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class Matches(MatchesTemplate):

    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        anvil.server.call('generate_matches')
        self.repeating_panel_1.items = anvil.server.call("get_my_matches")     
    
    def request_data_access_click(self, **event_args):
        """This method is called when the Request Data Access button is clicked"""
        alert("This feature is still being worked on...\nPlease check back later.")
        

