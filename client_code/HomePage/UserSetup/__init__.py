from ._anvil_designer import UserSetupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...Globals import LOCALE, pink, yellow, white
from ..Autocomplete import Autocomplete

class UserSetup(UserSetupTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        user = anvil.users.get_user()
        self.display_name.text = user['display_name']
        if user['house_number']:
            self.house_number.text = user['house_number']
        self.country.text = LOCALE
        self.postcode.text = user['postcode']
        self.postcode.tag = "Optional"
        self.telephone.text = user['telephone']
        self.telephone.tag = "Optional"
        self.autocomplete = Autocomplete()
        self.column_panel_1.add_component(self.autocomplete)
        self.autocomplete.text_box_1.tag = "Optional"
        self.autocomplete.text_box_1.set_event_handler("show", self.field_change)

      
    def get_input_fields(self):
        """ Returns a dictionary of database column headings and corresponding components/attributes """
        return {'display_name' : (self.display_name, 'text'),
               'house_number' : (self.house_number, 'text'),
               'address' : (self.autocomplete.text_box_1, 'text'),
               'country': (self.country, 'text'),
               'telephone' : (self.telephone, 'text'),
               'postcode': (self.postcode, 'text'),
               }
      
    def save_input(self, **event_args):
        """This method is called when the .my_details container is finally closed (after clicking OK) """
        print("saving input")
        input_fields = self.get_input_fields()
        for field, _values in input_fields.items():
            component, attribute = _values
            anvil.server.call("save_user_setup", field, getattr(component, attribute))
        valid_address = True if "1 out of 1 result" in self.autocomplete.link_1.text else False
        print(valid_address)
        anvil.server.call("save_user_setup", "valid_address", valid_address)
        anvil.server.call('save_approx_lon_lat')
        
        
    def check_for_existing_display_name(self):
        user = anvil.users.get_user()
        if self.display_name.text != user['display_name']:
            existing_name = anvil.server.call("check_for_display_name", self.display_name.text)
            if existing_name:
                self.help_box.text = f"⚠ Sorry, the Display Name '{self.display_name.text}' has already been taken or is not allowed."
                self.deselect_all_icons()
                return True
            
    def field_change(self, **event_args):
        """ Highlights empty input boxes and checks for unique Display Name"""
        if event_args['sender'] is self.display_name:
            if self.check_for_existing_display_name():
                self.display_name.background = pink
                return
        if event_args['sender'].text == "":
            if event_args['sender'].tag == "Optional":
                event_args['sender'].background = yellow
            else:
                event_args['sender'].background = pink
        else:
            event_args['sender'].background = white
                   



















