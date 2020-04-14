from ._anvil_designer import MyOffersRowTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....Globals import STATUSES

class MyOffersRow(MyOffersRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        try:
            self.status.text = STATUSES[self.item['status_code']]
        except KeyError:
            self.visible = False
            check_request_status()     

    def check_request_status(self, **properties):
        matches = anvil.server.call('get_my_matches')
        match_count = 0
        for match in matches:
            if match['request'] == self.item:
                match_count += 1
        if match_count > 0 and int(match['status_code']) in [1,2,3]:                
            self.status.text = f"Matched with {match_count} requests"
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



