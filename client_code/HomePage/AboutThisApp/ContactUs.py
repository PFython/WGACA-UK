from ._anvil_designer import ContactUsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)

class ContactUs(ContactUsTemplate):
    addresses = ADDRESSES
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.


    def send_message(self, **event_args):
      """This method is called when the button is clicked"""
      app_tables.feedback.add_row(from_user = anvil.users.get_user(),
                                  date = datetime.datetime.today().date(),
                                  category = self.category.selected_value,
                                  title = self.title.text,
                                  description = self.description.text,
                                  telephone_ok = self.telephone_ok.checked,
                                  email_ok = self.email_ok.checked,)
      self.clear()
      self.parent.visible = False
      alert("""Message sent.  Thanks for taking the time to reach out to us!""")



















