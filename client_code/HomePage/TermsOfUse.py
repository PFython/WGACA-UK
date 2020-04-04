from ._anvil_designer import TermsOfUseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TermsOfUse(TermsOfUseTemplate):
    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.

    def accept_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      if self.accept:
          self.accept.enabled = False
          anvil.server.call('terms_accepted', True)








