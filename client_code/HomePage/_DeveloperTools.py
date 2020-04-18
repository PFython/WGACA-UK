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
        self.limit_amount.text = 3

        # Any code you write here will run when the form opens.

    def click_OSM_route_generator(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.server.call("_generate_route_url_for_all_matches")

    def click_limit_status_codes(self, **event_args):
        """This method is called when the button is clicked"""
        limit = self.limit_amount.text
        count = 0
        matches = anvil.server.call('_get_all_matches')
        for match in anvil.server.call('_get_all_matches'):
            match_value = match['status_code'] or limit
            if int(match_value) >= int(limit):
                anvil.server.call("update_status_codes", match, limit)
                count += 1
        print(f"{count} matches out of {len(matches)} limited to status code [{limit}]")
