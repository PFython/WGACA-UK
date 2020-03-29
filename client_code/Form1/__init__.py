from ._anvil_designer import Form1Template
from anvil import *



class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.choices = ('Food|Vegetables|Tomatoes',
                  'Food|Vegetables|Potatoes',
                  'Food|Vegetables|Carrots',
                  'Medical|Tablets|Ibuprofen',
                  'Medical|Tablets|Paracetamol')

    # Any code you write here will run when the form opens.
    

  def offer_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    pass

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def offered_item_list_show(self, **event_args):
    """This method is called when the data row panel is shown on the screen"""
    pass



