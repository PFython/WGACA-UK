from ._anvil_designer import UserSetupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)

class UserSetup(UserSetupTemplate):
    addresses = ADDRESSES
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        user = anvil.users.get_user()
        self.display_name.text = user['display_name']
        self.email.text = user['email']
        if user['house_number']:
            self.house_number.text = user['house_number']
        # Create list of valid counties
        self.county.items = sorted(self.addresses.keys())
        if user['county']:
            self.county.selected_value = user['county']
        else:
            self.county.selected_value = sorted(list(self.addresses.keys()))[0]
            self.county_change()
        # Create list of valid streets
        self.street.items = self.get_streets_from_county()
        if user['street']:           
            self.street.selected_value = user['street']
        else:
            self.street_change()
        # Create list of valid towns
        towns = list(self.get_towns_from_county().keys())
        self.town.items = towns
        if user['town']:
           self.town.selected_value = user['town']
        self.country.text = LOCALE
        self.postcode.text = user['postcode']
        self.postcode.tag = "Optional"
        self.telephone.text = user['telephone']
        self.telephone.tag = "Optional"
        
    def get_streets_from_county(self):
        """ Returns a list of streets derived from County selection """
        towns = UserSetup.addresses[self.county.selected_value]
        streets = []
        for town in towns:
            streets.extend(UserSetup.addresses[self.county.selected_value][town])
        streets.sort()
        return streets
    
    def get_towns_from_county(self):
        """ Returns a dictionary of towns (key) and a list of streets (value)"""
        return UserSetup.addresses[self.county.selected_value]
  
    def county_change(self, **event_args):
        """This method is called when the County drop-down is changed """
        streets = self.get_streets_from_county()
        self.street.items = streets
        self.street.selected_value = streets[0]
        self.street_change()

    def street_change(self, **event_args):
        """This method is called when the Street drop-down is changed"""
        towns = self.get_towns_from_county()
        for town, street_list in towns.items():
            if self.street.selected_value in street_list:
                break
        # Create single item list of valid towns        
        self.town.items = [town]
        self.town.selected_value = town
        
    def get_input_fields(self):
        """ Returns a dictionary of database column headings and corresponding components/attributes """
        return {'display_name' : (self.display_name, 'text'),
               'house_number' : (self.house_number, 'text'),
               'street' : (self.street, 'selected_value'),
               'town' : (self.town, 'selected_value'),
               'county' : (self.county, 'selected_value'),
               'country' : (self.country, 'text'),
               'postcode' : (self.postcode, 'text'),
               'telephone' : (self.telephone, 'text'),}
      
    def save_input(self, **event_args):
        """This method is called when the .my_details container is finally closed (after clicking OK) """
        input_fields = self.get_input_fields()
        for field, _values in input_fields.items():
            component, attribute = _values
            anvil.server.call("save_user_setup", field, getattr(component, attribute))

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
        """This method is called when a Help icon is clicked"""
        self.help_text.text = event_args['sender'].tag
        # Set all icons to unselected
        components = [self.help1, self.help2, self.help3,
                      self.help4, self.help5, self.help6,
                      self.help7, self.help8, self.help9]
        for component in components:
            setattr(component, 'icon', 'fa:question')
        # Set clicked icon to selected
        event_args['sender'].icon = 'fa:question-circle'



















