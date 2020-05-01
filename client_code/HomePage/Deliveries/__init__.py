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
        self.filters = {self.all: "all",
           self.needs_action: "needs_action",
           self.expiring: "expiring",
           self.complete: "complete"}

    def form_loaded(self, **event_args):
        self.checkbox_change(sender=self.all)
        
    def get_deliveries(self):

            self.repeating_panel_1.items = anvil.server.call("get_my_deliveries", self.filters.values())
        else:
            self.input_description_1.text = "There are no current deliveries where you're the Requester, Runner, or person making an Offer."

    def checkbox_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      sender = event_args['sender']
      if sender == self.all:
          for checkbox in self.filters:
             checkbox.checked = True if self.all.checked else False
      elif self.all.checked:
          self.all.checked = False
      self.get_deliveries()
              
                

    