from ._anvil_designer import MyOffersTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

ITEM_HEIRARCHY = anvil.server.call("get_product_heirarchy").split("\n")
UNITS_OF_MEASURE = anvil.server.call("get_units_of_measure").split("\n")

class MyOffers(MyOffersTemplate):
    item_choices = ITEM_HEIRARCHY
    units_of_measure = UNITS_OF_MEASURE

    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.repeating_panel_1.items = anvil.server.call("get_my_offers")     
    
    def add_to_my_offer_list(self,product_key, units, expiry_date, notes):
        user = anvil.users.get_user()['email']
        result = anvil.server.call("save_to_database", product_key, units, expiry_date, notes)
        if result == "Duplicate":
              self.debug_console.text = "ⓘ Unable to create new entry because this combination of Product, Unit of Measure, and Expiry Date already exists.  Please consider deleting old entry and creating a new one?"
        else:
              self.debug_console.text = "✓ Item added."   
        self.repeating_panel_1.items = anvil.server.call("get_my_offers")    

    def add_item_click(self, **event_args):
        """This method is called when the button is clicked"""
        unit_of_measure = self.unit_of_measure.selected_value or self.unit_of_measure.placeholder
        product_key = (self.product_description.selected_value, unit_of_measure)
        units = int(self.number_of_units.text or self.number_of_units.placeholder)
        expiry_date = self.expiry_date.date or datetime.datetime.today().date()
        notes = self.notes.text or "(No notes attached)"
        if not product_key[0] and product_key[1]:
            self.debug_console.text = "⚠ Please select a product and/or unit of measure."
        else:
            self.add_to_my_offer_list(product_key, units, expiry_date, notes)

