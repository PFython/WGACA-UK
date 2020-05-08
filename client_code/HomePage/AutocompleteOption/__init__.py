from ._anvil_designer import AutocompleteOptionTemplate
from anvil import *
import anvil.server

class AutocompleteOption(AutocompleteOptionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    # Any code you write here will run when the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.parent.raise_event('x-option_clicked',option=self.link_1.text)
    pass
