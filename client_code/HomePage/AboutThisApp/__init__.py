from ._anvil_designer import AboutThisAppTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ContactUs import ContactUs

class AboutThisApp(AboutThisAppTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.

  def contact_us_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.contact_us_container.visible = True
      self.contact_us_container.add_component(ContactUs())
      
  def log_out(self, **event_args):
      """This method is called when the Log Out button is clicked"""
      anvil.users.logout()
      anvil.users.login_with_form()
      self.parent.parent.__init__()
      self.parent.parent.menu_my_details_click()


