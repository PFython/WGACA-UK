import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime
from .Product_Data import products
from .Unit_Data import units
# Change import for other countries' address data:
from .Address_Data_UK import hierarchy

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.

@anvil.server.callable
def save_to_offers_database(product_key, units, expiry_date, notes):
    """ Returns 'Duplicate' if product_key/expiry date row already exists"""
    product_key = " … ".join(product_key)
    user = anvil.users.get_user()
    if user is None:
        return
    existing_entry = app_tables.offers.get(product_key=product_key, expiry_date=expiry_date, user = user)
    if existing_entry:
        return "Duplicate"    
    app_tables.offers.add_row(status='New',product_key=product_key, notes = str(notes), expiry_date = expiry_date, units=units, user=user, date_posted=datetime.datetime.today().date())

@anvil.server.callable
def save_to_requests_database(product_category, urgent, notes):
    """ Returns 'Duplicate' if product_category request already exists"""
    user = anvil.users.get_user()
    if user is None:
        return
    existing_entry = app_tables.requests.get(product_category=product_category, user = user)
    if existing_entry:
        return "Duplicate"    
    app_tables.requests.add_row(status='New', product_category=product_category, urgent = urgent, user = user, notes = str(notes), date_posted=datetime.datetime.today().date())    
    
@anvil.server.callable
def save_user_setup(field, value):
    user = anvil.users.get_user()
    user[field] = value    

@anvil.server.callable
def get_my_matches():
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("accepted"))
      
@anvil.server.callable
def get_my_deliveries():
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("accepted"))
      
@anvil.server.callable
def get_my_offers():
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.offers.search(tables.order_by("product_key"), user = user)
      
@anvil.server.callable
def get_my_requests():
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.requests.search(tables.order_by("product_category"), user = user)
       
@anvil.server.callable
def terms_accepted(boolean_value):
    user = anvil.users.get_user()
    user['terms_accepted'] = datetime.datetime.today().date() if boolean_value else None

@anvil.server.callable
def get_address_hierarchy(country = "United Kingdom"):
    global hierarchy
    return hierarchy[country]    
  
@anvil.server.callable
def get_units_of_measure():
    global units
    return units.split("\n")
      
@anvil.server.callable
def get_product_heirarchy():
    global products
    return sorted(products.split("\n"))

@anvil.server.callable
def update_telephone(telephone):
    user_row = anvil.users.get_user()
    try:
        user_row.update(Telephone = telephone)
        result = True
    except:
        result = False
    return result