from ._anvil_designer import DeliveriesTemplate
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

class Deliveries(DeliveriesTemplate):
    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.radio_buttons = {self.all: "all",
           self.needs_action: "needs_action",
           self.expiring: "expiring",
           self.complete: "complete",}
        self.radio_button_change(sender=self.all)
        
    def get_deliveries(self):
        deliveries = anvil.server.call("get_my_deliveries",self.radio_buttons[self.sender])
        print(len(deliveries),"deliveries found")
        if deliveries:
            self.repeating_panel_1.items = deliveries
        else:
            self.repeating_panel_1.items = []
            self.input_description_1.text = "There are no current deliveries where you're the Requester, Runner, or person making an Offer."

    def radio_button_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      self.sender = event_args['sender']
      for button in self.radio_buttons:
          button.bold = True if button.selected else False
      self.get_deliveries()
              
                

    