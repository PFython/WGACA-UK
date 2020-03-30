from ._anvil_designer import Home_PageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

USER = 'peter_5_Pullman_Gardens'

ITEM_HEIRARCHY = ('Food | Vegetables | Tomatoes',
              'Food | Vegetables | Potatoes',
              'Food | Vegetables | Carrots',
              'Medical | Tablets | Ibuprofen',
              'Medical | Tablets | Paracetamol')

UNITS_OF_MEASURE = ('grammes', 'kilogrammes', 'centilitres', 'litres', 'cans (regular)', 'cans (large)',
                    'bottles (regular)', 'bottles (large)', 'packets', 'items (small)', 'items (medium)', 'items (large)')

MY_OFFER_LIST = {}
# key: (product description, unit of measure)
# value: units

class Home_Page(Home_PageTemplate):
    item_choices = ITEM_HEIRARCHY
    units_of_measure = UNITS_OF_MEASURE

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.repeating_panel_1.items = app_tables.offers.search()
      
    
    def add_to_my_offer_list(self,product_key, units):
        output = "Added: " + str((product_key, units))
        try:
            existing_units = MY_OFFER_LIST[product_key]
        except KeyError: 
            existing_units = None
        if not existing_units:
            MY_OFFER_LIST[product_key] = units
            self.save_to_database(product_key, units)
        else:
            units += existing_units
            MY_OFFER_LIST[product_key] = units
        # save to database        
        output += "\n\n" + str(MY_OFFER_LIST)
        self.debug_console.text = output
        
    def save_to_database(self, product_key, units):
      product_key = " … ".join(product_key)
      app_tables.offers.add_row(status='New',product_key=product_key, units=units, user=USER, date_posted=datetime.datetime.today().date())
      self.repeating_panel_1.items = app_tables.offers.search()

    def add_item_click(self, **event_args):
      """This method is called when the button is clicked"""
      unit_of_measure = self.unit_of_measure.selected_value or self.unit_of_measure.placeholder
      product_key = (self.product_description.selected_value, unit_of_measure)
      units = int(self.number_of_units.text or self.number_of_units.placeholder)
      if not product_key[0] and product_key[1]:
          self.debug_console.text = "⚠ Please select a product and/or unit of measure."
      else:
          self.add_to_my_offer_list(product_key, units)

