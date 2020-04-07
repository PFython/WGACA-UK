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
def check_for_display_name(display_name):
    """ Returns boolean check for whether display name already exists in Users database"""
    return True if app_tables.users.get(display_name = display_name) else False

@anvil.server.callable
def generate_matches():
    """
    Compares Offers and Requests and saves matches (by product and area) to Matches database.
    Current version matches by Town.  TODO: Match by actual distance,
    as for some addresses the other side of the road is a different Town!
    """
    requests = app_tables.requests.search(tables.order_by("product_category"))
    offers = app_tables.offers.search(tables.order_by("product_key"))
    matches = 0
#     print("Generating Matches...")
    statuses = "Awaiting Pickup, Pickup Failed, Awaiting Delivery, Delivery Failed, Delivery Complete".split(", ")
    for request in (x for x in requests if x['status'] not in statuses):
        for offer in (x for x in offers if x['status'] not in statuses):
            if request['product_category'] in offer['product_key']:
                if request['user']['display_name'] != offer['user']['display_name']:
                    # check if new or existing match
                    new_match = app_tables.matches.get(request=request, offer=offer) or app_tables.matches.add_row(available_runners = [], request = request, offer=offer, status="New")
                    if new_match not in offer['matches']:
                        offer['matches'] += [new_match]
#                     offer['matches'] = list(set(offer['matches']))
                    if new_match not in request['matches']:
                        request['matches'] += [new_match]
#                     request['matches'] = list(set(request['matches']))

@anvil.server.callable
def get_address_hierarchy(country = "United Kingdom"):
    """ Returns an address hierarchy for the given Country """
    global hierarchy
    return hierarchy[country]    
  
@anvil.server.callable
def get_my_deliveries():
    """ Returns rows from the Matches database where runner = user """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("status"), approved_runner = user)

@anvil.server.callable
def get_my_matches():
    """ Returns rows from the Matches database """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("status"),approved_runner=None)
        # When approved_runner != None, the Match effectively becomes a Delivery
        # TODO: Filter results by proximity

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
def get_product_hierarchy():
    """ Returns a product hierarchy """
    global products
    return sorted(products.split("\n"))

@anvil.server.callable
def get_units_of_measure():
    """ Returns a list of valid units of measure """
    global units
    return units.split("\n")
  
@anvil.server.callable
def get_user_from_display_name(display_name):
    """ Returns a User (row) object based on display_name string """
    return app_tables.users.get(display_name=display_name)

@anvil.server.callable
def remove_orphan_matches(request_or_offer):
    """ Deletes a Match where the child Request or Offer has just been deleted """
    try:
        for match in app_tables.matches.search(request=request_or_offer):
            match.delete()
    except anvil.tables.TableError:
        pass
    try:
        for match in app_tables.matches.search(offer=request_or_offer):
            match.delete()
    except anvil.tables.TableError:
        pass

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
    app_tables.offers.add_row(status='New',product_key=product_key, notes = str(notes), expiry_date = expiry_date, units=units, user=user, date_posted=datetime.datetime.today().date(), matches = [])

 
@anvil.server.callable
def save_to_requests_database(product_category, urgent, notes):
    """ Returns 'Duplicate' if product_category request already exists"""
    user = anvil.users.get_user()
    if user is None:
        return
    existing_entry = app_tables.requests.get(product_category=product_category, user = user)
    if existing_entry:
        return "Duplicate"    
    app_tables.requests.add_row(status='New', product_category=product_category, urgent = urgent, user = user, notes = str(notes), date_posted=datetime.datetime.today().date(), matches = [])    
    
@anvil.server.callable
def save_user_setup(field, value):
    """ General purpose save to the User database """
    user = anvil.users.get_user()
    user[field] = value
  
@anvil.server.callable
def terms_accepted(boolean_value):
    """ Records today's date (or None) in the User database for Terms Accepted"""
    user = anvil.users.get_user()
    user['terms_accepted'] = datetime.datetime.today().date() if boolean_value else None

@anvil.server.callable
def volunteer_as_runner(match, boolean_value):
    """ Volunteer/unvolunteer as available_runner in Matches"""
    user = anvil.users.get_user()
    if boolean_value:
        match['available_runners'] += [user]
    else:
        match["available_runners"] = [x for x in match["available_runners"] if x != user]