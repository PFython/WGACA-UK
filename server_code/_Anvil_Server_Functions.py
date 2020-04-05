import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

# Change imports for other countries' data:
from .Product_Data_UK import products
from .Unit_Data_UK import units
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
    """ General purpose save to the User database """
    user = anvil.users.get_user()
    user[field] = value    

@anvil.server.callable
def get_my_matches():
    """ Returns rows from the Matches database """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("status"))
        # TODO: Filter results by proximity
      
@anvil.server.callable
def get_my_deliveries():
    """ Returns rows from the Matches database where runner = user """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("status"), runner = user)
      
@anvil.server.callable
def get_my_offers():
    """ Returns rows from the Offers database for a given user """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.offers.search(tables.order_by("product_key"), user = user)
      
@anvil.server.callable
def get_my_requests():
    """ Returns rows from the Requests database for a given user """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.requests.search(tables.order_by("product_category"), user = user)
       
@anvil.server.callable
def terms_accepted(boolean_value):
    """ Records today's date (or None) in the User database for Terms Accepted"""
    user = anvil.users.get_user()
    user['terms_accepted'] = datetime.datetime.today().date() if boolean_value else None

@anvil.server.callable
def get_address_hierarchy(country = "United Kingdom"):
    """ Returns an address hierarchy for the given Country """
    global hierarchy
    return hierarchy[country]    

@anvil.server.callable
def check_for_display_name(display_name):
    """ Returns boolean check for whether display name already exists in Users database"""
    return True if app_tables.users.get(display_name = display_name) else False
  
@anvil.server.callable
def get_units_of_measure():
    """ Returns a list of valid units of measure """
    global units
    return units.split("\n")
      
@anvil.server.callable
def get_product_hierarchy():
    """ Returns a product hierarchy """
    global products
    return sorted(products.split("\n"))

@anvil.server.callable
def generate_matches():
    """
    Compares Offers and Requests and saves matches (by product and area) to Matches database.
    Current version matches by Town.  TODO: Match by actual distance,
    as for some addresses the other side of the road is a different Town!
    """
    requests = app_tables.requests.search(tables.order_by("product_category"), status = "New")
    offers = app_tables.offers.search(tables.order_by("product_key"), status = "New")
    matches = 0
    for request in requests:
        for offer in offers:
            if request['product_category'] in offer['product_key']:
                if request['user']['display_name'] != offer['user']['display_name']:
                    print(f"Request by {request['user']['display_name']}:\n{request['product_category']} \nOffer from {offer['user']['display_name']}:\n{offer['product_key']}\n")
                    matches += 1
                    # check if new or existing match
                    new_match = app_tables.matches.add_row(request=request, offer=offer) or app_tables.matches.add_row(request=request, offer=offer, available_runners = [], status="New")
    print(f"{matches} new matches found.")
    # Assign Offer to earliest Requests first