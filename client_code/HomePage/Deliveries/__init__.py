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
        self.filters = {self.all: ["all",False],
           self.needs_action: ["needs_action",False],
           self.expiring: ["expiring",False],
           self.complete: ["complete",False],}
        self.checkbox_change(sender=self.all)
        
    def get_deliveries(self):
        deliveries = anvil.server.call("get_my_deliveries", self.filters.values())
        if deliveries:
            self.repeating_panel_1.items = deliveries
        else:
            self.input_description_1.text = "There are no current deliveries where you're the Requester, Runner, or person making an Offer."

    def checkbox_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      sender = event_args['sender']
      if sender == self.all:
          print("if")
          for checkbox in self.filters:
             checkbox.checked = True if self.all.checked else False
      elif self.all.checked:
          print("elif")
          self.all.checked = False
      for checkbox in self.filters:
          self.filters[checkbox] = [self.filters[checkbox][0], True if checkbox.checked else False]
      
      print(self.filters)
#       self.get_deliveries()
              
                

    