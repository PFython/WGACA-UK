from ._anvil_designer import ContactUsTemplate
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class ContactUs(ContactUsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.


    def send_message(self, **event_args):
      """This method is called when the button is clicked"""
      app_tables.feedback.add_row(from_user = anvil.users.get_user(),
                                  date_time = datetime.datetime.now(),
                                  category = self.category.selected_value,
                                  title = self.title.text,
                                  description = self.description.text,
                                  telephone_ok = self.telephone_ok.checked,
                                  email_ok = self.email_ok.checked,)
      self.clear()
      self.parent.visible = False
      alert("""Message sent.  Thanks for taking the time to reach out to us!""")

    def cancel_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.clear()
      self.parent.visible = False




















