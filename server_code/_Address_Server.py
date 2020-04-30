import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import datetime
import time

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.


address_media = [x for x in app_tables.uploads.search(tables.order_by("datetime"), name="Address_Data_UK") if 'OS' in x['media'].name]
address_lines = address_media[0]['media'].get_bytes().decode('utf-8')
data = address_lines.split()
print("address_lines",len(data))

@anvil.server.callable
def get_initial_address_matches(text, max_options):
    new_options = []
    text = text.lower()
    for option in data:
      if option.lower().startswith(text):
          new_options.append(option)
          if len(new_options) == max_options:
              break
    return sorted(new_options)
