from ._anvil_designer import _DeveloperToolsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..OS import address_list
from ..Globals import LOCALE
import datetime

class _DeveloperTools(_DeveloperToolsTemplate):
    def __init__(self, **properties):
      
      
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.init_components(**properties)
        
    # Any code you write here will run when the form opens.

    def backfill_approx_lat_lon(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.server.call('_backfill_approx_lon_lat')
        
    def upload_via_returned_row(self, file, **event_args):
        upload_row, row_id = anvil.server.call("_get_upload_row", "Address_Data_UK")
        file = self.file_loader_1.file
        upload_row['media'] = file
        anvil.server.call("_write_upload_row", upload_row, row_id)
        self.file_loader_1.clear()

    def upload_address_lines_client_only(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        file = self.file_loader_1.file
        print(file, file.name)
        media_upload = app_tables.uploads.add_row(name=file.name, media = file, datetime = datetime.datetime.now())
        print(f"{file.name} saved to uploads databases.")
        self.file_loader_1.clear()
        
    def upload_address_lines(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        file = self.file_loader_1.file
        file = anvil.server.call('_store_uploaded_media', file, "Address_Data_UK")
        self.file_loader_1.clear()
              
    def download_media(self):
        blob = anvil.BlobMedia("text/plain",self.merged_srts.encode('utf-8'), filename)
        anvil.download(blob, "D:")        

    def button_1_copy_click(self, **event_args):
      """This method is called when the button is clicked"""
      anvil.server.call("_convert_old_addresses")      

    def button_1_copy_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      input("Are you sure")
      anvil.server.call("_scratch_offers_matches_requests")

    def click_user_emails(self, **event_args):
      """This method is called when the button is clicked"""
      areas = [x for x in self.get_components() if type(x) == TextArea]
      for area in areas:
          area.remove_from_parent()
      textarea = TextArea()
      self.add_component(textarea)
      textarea.text = anvil.server.call("_get_user_emails")
      textarea.select()








