from ._anvil_designer import DeliveriesTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class Deliveries(DeliveriesTemplate):
    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        deliveries = []
        user = anvil.users.get_user()
        for delivery in anvil.server.call("get_my_deliveries"):
            if delivery['approved_runner'] == user:
                deliveries += [delivery]
                continue
            if delivery['offer']['user'] == user:
                deliveries += [delivery]
                continue
            if delivery['request']['user'] == user:
                deliveries += [delivery]
                continue
        if deliveries:
            self.repeating_panel_1.items = deliveries
        else:
            self.input_description_1.text = "There are no current deliveries where you're the Requester, Runner, or person making an Offer."
        
    