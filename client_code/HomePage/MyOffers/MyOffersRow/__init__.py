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
        self.status.text = STATUSES[self.item['status_code']]        

    def delete_row_click(self, **event_args):
        """This method is called when a Delete Row icon is clicked"""
        anvil.server.call("remove_orphan_matches", self.item)
        self.item.delete()
        self.remove_from_parent()
        
    def show_notes_click(self, **event_args):
        """This method is called when a Show Notes icon is clicked"""
        text = "\nNOTES:\n\n" + self.item['notes']
        alert(text)



