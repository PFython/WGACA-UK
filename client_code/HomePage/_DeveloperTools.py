from ._anvil_designer import _DeveloperToolsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class _DeveloperTools(_DeveloperToolsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def click_OSM_route_generator(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call("_generate_route_url_for_all_matches")

