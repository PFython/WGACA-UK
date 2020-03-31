import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def save_to_database(product_key, units, expiry_date, notes, USER):
    """ Returns 'Duplicate' if product_key/expiry date row already exists"""
    product_key = " … ".join(product_key)
    existing_entry = app_tables.offers.get(product_key=product_key, expiry_date=expiry_date)
    if existing_entry:
        return "Duplicate"
    app_tables.offers.add_row(status='New',product_key=product_key, notes = str(notes), expiry_date = expiry_date, units=units, user=USER, date_posted=datetime.datetime.today().date())
    

