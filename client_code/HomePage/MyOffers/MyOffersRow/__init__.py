from ._anvil_designer import MyOffersRowTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....Globals import STATUSES, red

class MyOffersRow(MyOffersRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        try:
            self.status.text = STATUSES[self.item['status_code']]
        except KeyError:
            pass
        if self.item['matches']:
            self.check_offer_status()     

    def check_offer_status(self, **properties):
        match_count = len(self.item['matches'])
        print ("Matches:",match_count)
        if match_count > 0 and self.item['status_code'] in ['1','2']:                
            self.status.text = f"Matched with {match_count} requests.  Please check My Matches."
        self.refresh_data_bindings()
        
    def delete_row_click(self, **event_args):
        """This method is called when a Delete Row icon is clicked"""
        anvil.server.call("remove_orphan_matches", self.item)
        self.item.delete()
        self.remove_from_parent()
        
    def show_notes_click(self, **event_args):
        """This method is called when a Show Notes icon is clicked"""
        text = "\nNOTES:\n\n" + self.item['notes']
        alert(text)

    def show_row(self, **event_args):
      """This method is called when the data row panel is shown on the screen"""
      self.status.text = STATUSES[self.item['status_code']]
      self.status.foreground = '#0080c0' if self.status.text.startswith("New") else '#5eb348'
      self.check_offer_status()






