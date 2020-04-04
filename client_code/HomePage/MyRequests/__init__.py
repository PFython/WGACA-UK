from ._anvil_designer import MyRequestsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

ITEM_HEIRARCHY = anvil.server.call("get_product_heirarchy").split("\n")
UNITS_OF_MEASURE = anvil.server.call("get_units_of_measure").split("\n")

class MyRequests(MyRequestsTemplate):
    item_choices = ITEM_HEIRARCHY
    units_of_measure = UNITS_OF_MEASURE

    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.repeating_panel_1.items = anvil.server.call("get_my_requests")     
    
    def add_to_my_requests(self,product_category, urgent, notes):
#         user = anvil.users.get_user()['email']
        result = anvil.server.call("save_to_requests_database", product_category, urgent, notes)
        if result == "Duplicate":
              self.debug_console.text = "ⓘ Unable to create new entry because a request for this category already exists."
        else:
              self.debug_console.text = "✓ Request added."   
        self.repeating_panel_1.items = anvil.server.call('get_my_requests')    

    def add_request_click(self, **event_args):
        """This method is called when the button is clicked"""
        product_category = (self.product_category.selected_value)
        urgent = self.urgent.selected
        notes = self.notes.text or "(No notes attached)"
        if not product_category:
            self.debug_console.text = "⚠ Please select a product category."
        else:
            self.add_to_my_requests(product_category, urgent, notes)

