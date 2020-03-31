from ._anvil_designer import Home_PageTemplate
from anvil import *
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime



ITEM_HEIRARCHY = ('Food | Vegetables | Tomatoes',
              'Food | Vegetables | Potatoes',
              'Food | Vegetables | Carrots',
              'Medical | Tablets | Ibuprofen',
              'Medical | Tablets | Paracetamol')

UNITS_OF_MEASURE = ('grammes', 'kilogrammes', 'centilitres', 'litres', 'cans (regular)', 'cans (large)',
                    'bottles (regular)', 'bottles (large)', 'packets', 'items (small)', 'items (medium)', 'items (large)')


class Home_Page(Home_PageTemplate):
    item_choices = ITEM_HEIRARCHY
    units_of_measure = UNITS_OF_MEASURE

    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.repeating_panel_1.items = app_tables.offers.search(tables.order_by("product_key"))      
    
    def add_to_my_offer_list(self,product_key, units, expiry_date, notes):
        user = anvil.users.get_user()['email']
        result = anvil.server.call("save_to_database", product_key, units, expiry_date, notes)
        if result == "Duplicate":
              self.debug_console.text = "ⓘ Unable to create new entry because this combination of Product, Unit of Measure, and Expiry Date already exists.  Please consider deleting old entry and creating a new one?"
        else:
              self.debug_console.text = "✓ Item added."   
        self.repeating_panel_1.items = app_tables.offers.search(tables.order_by("product_key"))
    

    def add_item_click(self, **event_args):
      """This method is called when the button is clicked"""
      unit_of_measure = self.unit_of_measure.selected_value or self.unit_of_measure.placeholder
      product_key = (self.product_description.selected_value, unit_of_measure)
      units = int(self.number_of_units.text or self.number_of_units.placeholder)
      expiry_date = self.expiry_date.date or datetime.datetime.today().date()
      notes = self.notes.text or "(No notes attached)"
      if not product_key[0] and product_key[1]:
          self.debug_console.text = "⚠ Please select a product and/or unit of measure."
      else:
          self.add_to_my_offer_list(product_key, units, expiry_date, notes)

    def text_area_1_change(self, **event_args):
      """This method is called when the text in this text area is edited"""
      pass


