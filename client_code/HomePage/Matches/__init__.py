from ._anvil_designer import MatchesTemplate
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
        self.user = anvil.users.get_user()
        self.radio_buttons = {self.radio_button_1: "all",
                      self.radio_button_2: 'street',
                      self.radio_button_3: 'town',
                      self.radio_button_4: 'county',}
        street, town, county = self.user['address'].split("; ")
        self.radio_button_2.text = f"Matches in {street or 'my Street'}"
        self.radio_button_3.text = f"Matches in {town or 'my Town'}"
        self.radio_button_4.text = f"Matches in {county or 'my County'}"
        if self.user['view_all']:
            self.radio_button_1.visible = True
        self.radio_button_clicked(sender=self.radio_button_3)
        
    
    def request_data_access_click(self, **event_args):
        """This method is called when the Request Data Access button is clicked"""
        alert("This feature is still being worked on...\nPlease check back later.")
        

    def radio_button_clicked(self, **event_args):
      """This method is called when this radio button is selected"""
      sender = event_args['sender']
      for button in self.radio_buttons:
          button.bold = True if button.selected else False
      self.repeating_panel_1.items = anvil.server.call("get_my_matches",self.radio_buttons[sender])



