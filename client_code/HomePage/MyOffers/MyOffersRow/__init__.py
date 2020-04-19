from ._anvil_designer import MyOffersRowTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

from ....Globals import red

class MyOffersRow(MyOffersRowTemplate):
  
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        
    def delete_row_click(self, **event_args):
        """This method is called when a Delete Row icon is clicked"""
        anvil.server.call("remove_orphan_matches", self.item)
        self.item.delete()
        self.remove_from_parent()        

    def check_offer_status(self, **properties):
        self.status.text = anvil.server.call('get_status_message_from_status_dict', self.item)
        self.refresh_data_bindings()

    def show_row(self, **event_args):
      """This method is called when the data row panel is shown on the screen"""
      self.status.text = anvil.server.call("get_status_message_from_status_dict", self.item)
      self.status.foreground = '#0080c0' if self.status.text.startswith("New") else '#5eb348'
      self.info.visible = self.item['notes'] != "(No notes attached)"
      expiry = self.item['expiry_date']
      self.expiry_date.text = expiry.strftime('%d %b %Y')
      if expiry <= datetime.datetime.today():
            self.expiry_date.foreground = red
      if self.item['matches']:
          self.check_offer_status()

    def show_notes_click(self, **event_args):
        """This method is called when a Show Notes icon is clicked"""
        text = "\nNOTES:\n\n" + self.item['notes']
        alert(text)