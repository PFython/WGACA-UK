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
    self.init_components(**properties)
    self.options = countries = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central Arfrican Republic","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cuba","Curacao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauro","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","North Korea","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
    self.repeating_panel_1.items = [{'text':' '}] * 7
    self.repeating_panel_1.set_event_handler('x-option_clicked',self.option_clicked)

    # Any code you write here will run when the form opens.

    def text_box_1_change(self, **event_args):
      """This method is called when the text in this text box is edited"""
      new_options = []
      for option in self.options:
        if option.lower().startswith(self.text_box_1.text.lower()):
          new_options.append({'text':option})
      # truncate to 7 max
      new_options = new_options[:7]
      # ensure a full 7 options
      if len(new_options) < 7:
        new_options+=( [{'text':' '}] * (7-len(new_options)))
      self.repeating_panel_1.items = new_options
      pass

    def option_clicked(self,option,**event_args):
      if option == ' ':
        return
      self.text_box_1.text = option
      self.repeating_panel_1.items = []

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
        if text.endswith(" ") or len(text) > 8 or len(text) > len(self.previous_entry):
            self.text_area_1.text = self.autofill_address(text)
        self.previous_entry = text

            
    def autofill_address(self, user_input):
        matches = anvil.server.call('get_address_matches', user_input)
        for line in self.address_lines:
            if user_input in line:
                matches += [line]
                if len(matches) > 5:
                      break
        return matches
      


