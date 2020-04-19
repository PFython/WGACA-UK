from ._anvil_designer import TitleButtonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TitleButton(TitleButtonTemplate):
  def __init__(self, title, background, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.title_button.background = background
    user = anvil.users.get_user()
    username = user['display_name'] if user else ""
    self.title_button.text = title + " > " + username

    # Any code you write here will run when the form opens.