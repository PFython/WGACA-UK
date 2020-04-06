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


