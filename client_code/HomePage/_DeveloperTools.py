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

    def backfill_approx_lat_lon(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.server.call('_backfill_approx_lon_lat')

