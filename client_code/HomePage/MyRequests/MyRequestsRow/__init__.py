from ._anvil_designer import MyRequestsRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class MyRequestsRow(MyRequestsRowTemplate):
  
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      # Any code you write here will run when the form opens.

    def delete_row_click(self, **event_args):
        """This method is called when the link is clicked"""
        anvil.server.call("remove_orphan_matches", self.item)
        self.item.delete()
        self.remove_from_parent()

    def check_request_status(self, **properties):
      match_count = len(self.item['matches'])
      if match_count > 0 and self.item['status_code'] in ['1','2']:                 
          self.status.text = f"Matched with {match_count} requests.  Please check My Matches."
      self.refresh_data_bindings()

    def show_row(self, **event_args):
        """This method is called when the data row panel is shown on the screen"""
        self.status.text = anvil.server.call("get_status_message_from_status_dict", self.item)
        self.status.foreground = '#0080c0' if self.status.text.startswith("New") else '#5eb348'
        self.urgent.visible = self.item['urgent']
        self.date_posted.text = self.item['date_posted'].strftime('%d %b %Y')
        if self.item['matches']:
            self.check_request_status()


