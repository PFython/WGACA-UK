from ._anvil_designer import _DeveloperToolsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..OS import address_list
from ..Globals import LOCALE

class _DeveloperTools(_DeveloperToolsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.address_lines = address_list.split("\n")

    def backfill_approx_lat_lon(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.server.call('_backfill_approx_lon_lat')

    def upload_address_lines(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        file = self.file_loader_1.file
        file = anvil.server.call('_store_uploaded_media', file, "Address_Data_UK")
        self.file_loader_1.clear()
        
        
    def download_media(self):
        blob = anvil.BlobMedia("text/plain",self.merged_srts.encode('utf-8'), filename)
        anvil.download(blob, "D:")
        
    def text_box_1_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        text = self.text_box_1.text
        if text.endswith(" ") or len(text) > 8:
            self.text_area_1.text = self.autofill_address(text)

            
    def autofill_address(self, user_input):
        matches = []
        for line in self.address_lines:
            if user_input in line:
                matches += [line]
                if len(matches) > 5:
                      break
        return matches
      


