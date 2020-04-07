from ._anvil_designer import MyRequestsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

ITEM_HEIRARCHY = anvil.server.call("get_product_hierarchy")
UNITS_OF_MEASURE = anvil.server.call("get_units_of_measure")

class MyRequests(MyRequestsTemplate):
    item_choices = ITEM_HEIRARCHY
    units_of_measure = UNITS_OF_MEASURE

    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.check_request_status()
        self.repeating_panel_1.items = anvil.server.call("get_my_requests")  
    
    def add_to_my_requests(self,product_category, urgent, notes):
        """ Add request item to Requests database """          
        result = anvil.server.call("save_to_requests_database", product_category, urgent, notes)
        if result == "Duplicate":
              self.debug_console.text = "ⓘ Unable to create new entry because a request for this category already exists."
        else:
              self.debug_console.text = "✓ Request added."
              anvil.server.call('generate_matches')
        self.check_request_status()
        self.repeating_panel_1.items = anvil.server.call('get_my_requests')    

    def check_request_status(self, **properties):
        requests = anvil.server.call('get_my_requests')
        matches = anvil.server.call('get_my_matches')
        for request in requests:
            match_count = 0
            for match in matches:
                if match['request'] == request:
                    match_count += 1
            if match_count > 0 and request['status'] not in anvil.server.call("STATUSES"):
                request['status'] = f"Matched with {match_count} offers"
        self.refresh_data_bindings()
        
    def add_request_click(self, **event_args):
        """This method is called when the Add Request button is clicked"""
        product_category = (self.product_category.selected_value)
        urgent = self.urgent.selected
        notes = self.notes.text or "(No notes attached)"
        if not product_category:
            self.debug_console.text = "⚠ Please select a product category."
        else:
            self.add_to_my_requests(product_category, urgent, notes)

    def drop_down_change(self, **event_args):
        """Clears old Notes when a Drop Down list is selected"""
        self.notes.text = ""



