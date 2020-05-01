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
        self.filters = {self.all: {"all": False},
           self.needs_action: {"needs_action": False},
           self.expiring: {"expiring": False},
           self.complete: {"complete": False},}
        self.checkbox_change(sender=self.all)
        
    def get_deliveries(self):
        filters_dict = {k: v for d in self.filters.values() for k, v in d.items()}
        print(filters_dict)        
        deliveries = anvil.server.call("get_my_deliveries", filters_dict)
        print(len(deliveries))
        if deliveries:
            self.repeating_panel_1.items = deliveries
        else:
            self.repeating_panel_1.items = []
            self.input_description_1.text = "There are no current deliveries where you're the Requester, Runner, or person making an Offer."

    def checkbox_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      sender = event_args['sender']
      if sender == self.all:
          for checkbox in self.filters:
             checkbox.checked = True if self.all.checked else False
      elif self.all.checked:
          self.all.checked = False
      for checkbox in self.filters:
          name = self.filters[checkbox].keys()[0]
          self.filters[checkbox][name] = True if checkbox.checked else False
      self.get_deliveries()
              
                

    