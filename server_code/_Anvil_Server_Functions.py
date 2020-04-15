import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import datetime

# Change imports for other countries' data:
from .Product_Data_UK import products
from .Unit_Data_UK import units
from .Address_Data_UK import hierarchy

LOCALE = "United Kingdom"

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.

@anvil.server.callable
def add_karma_row(**kwargs):
    print(kwargs)
    app_tables.karma.add_row(**kwargs)

@anvil.server.callable
def check_for_display_name(display_name):
    """ Returns boolean check for whether display name already exists in Users database, or is simply invalid"""
    if display_name.startswith(" "):
      return True
    if display_name != None and display_name != "":
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
    statuses = anvil.server.call("STATUSES").values()
    for request in (x for x in requests if x['status_code'] in ['1','2']):
        for offer in (x for x in offers if x['status_code'] in ['1','2']):
            if request['product_category'] in offer['product_key']:
                if request['user']['display_name'] != offer['user']['display_name']:
                    # check if new or existing match
                    if not app_tables.matches.get(request=request, offer=offer):
                        print("new match!")
                        new_match =  app_tables.matches.add_row(available_runners = [], request = request, offer=offer, status_code="2")
                        request.update(status_code = "2")
                        offer.update(status_code = "2")
                        new_match['route_url'] = generate_route_url(new_match)
                        # 'or []' added to address possible database corruption i.e. value = None rather than value = []
                        if new_match not in (offer['matches'] or []):
                            offer['matches'] = (offer['matches'] or []) + [new_match]
                        if new_match not in (request['matches'] or []):
                            request['matches'] = (request['matches'] or []) + [new_match]

def generate_route_url(new_match):
    """Creates an Open Street Map url for pickup to dropoff route"""
    user = new_match['offer']['user']
    pickup = [user['street'], user['town'], user['county']]
    user = new_match['request']['user']
    dropoff = [user['street'], user['town'], user['county']]
    pickup = nominatim_scrape(pickup)[0]
    pickup = pickup['lat'] + "%2C" + pickup['lon']
    dropoff = nominatim_scrape(dropoff)[0]
    dropoff = dropoff['lat'] + "%2C" + dropoff['lon']
    osm = "https://www.openstreetmap.org/directions?engine=graphhopper_foot&route="
    osm += pickup + "%3B" + dropoff
#     print(osm)
    return osm
    
@anvil.server.callable
def _generate_route_url_for_all_matches():
  """This is a developer function to create OSM route urls for all Matches"""
  matches = app_tables.matches.search(tables.order_by("request"))
  count = 0
  for match in matches:
#     if match['route_url'] == None:
    match['route_url'] = generate_route_url(match)
    count += 1
  print(f"Populated {count} Matches with a route_url")
  return

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
        return [x for x in app_tables.matches.search(tables.order_by("status")) if x['approved_runner'] != None]

@anvil.server.callable
def get_my_matches():
    """ Returns rows from the Matches database """
    user = anvil.users.get_user()
    if user is not None:
        return app_tables.matches.search(tables.order_by("status_code"),approved_runner=None)
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

def nominatim_scrape(address_list):
    """Returns location & address data for supplied address list"""
    nominatim = 'https://nominatim.openstreetmap.org/search?q='
    nominatim += f"{','.join(address_list).replace(', ',',').replace('&','%26')},{LOCALE},&format=json".replace(" ","%20")
    return  anvil.http.request(nominatim, json=True)
  
@anvil.server.callable
def remove_orphan_matches(request_or_offer):
    """
    Deletes a Match where the child Request or Offer has just been deleted
    and deletes the Match from the corresponding Request or Offer
    """
    try:
        for match in app_tables.matches.search(request=request_or_offer):
            match.delete()
    except anvil.tables.TableError:
        pass
    try:
        for match in app_tables.matches.search(offer=request_or_offer):
            match.delete()
            offer = app_tables.matches.search()
    except anvil.tables.TableError:
        pass

@anvil.server.callable
def save_to_matches_database(match, runner, messages, status_code):
    """ Returns 'Duplicate' if product_category request already exists"""
    user = anvil.users.get_user()
    if user is None:
        return
    match.update(approved_runner = runner, messages_dict = messages, status = STATUSES()[status_code])
    
@anvil.server.callable
def save_to_offers_database(product_key, units, expiry_date, notes, status_code="1"):
    """ Returns 'Duplicate' if product_key/expiry date row already exists"""
    product_key = " … ".join(product_key)
    user = anvil.users.get_user()
    if user is None:
        return
    existing_entry = app_tables.offers.get(product_key=product_key, expiry_date=expiry_date, user = user)
    if existing_entry:
        return "Duplicate"    
    app_tables.offers.add_row(product_key=product_key, notes = str(notes), expiry_date = expiry_date, units=units, user=user, date_posted=datetime.datetime.today().date(), matches = [], status_code = status_code)
 
@anvil.server.callable
def save_to_requests_database(product_category, urgent, notes, status_code="1"):
    """ Returns 'Duplicate' if product_category request already exists"""
    user = anvil.users.get_user()
    if user is None:
        return
    existing_entry = app_tables.requests.get(product_category=product_category, user = user)
    if existing_entry:
        return "Duplicate"    
    app_tables.requests.add_row(product_category=product_category, urgent = urgent, user = user, notes = str(notes), date_posted=datetime.datetime.today().date(), matches = [], status_code = status_code)    

@anvil.server.callable
def save_user_setup(field, value):
    """ General purpose save to the User database """
    user = anvil.users.get_user()
    user[field] = value
  
@anvil.server.callable
def STATUSES():
    """ Returns allowable status descriptions other than 'New' or 'X matches found' """
    return {'1':  "New",
            '2':  "Matched with...",
            '3':  "Runner confirmed; Agree Pickup Time",
            '4':  "Offerer: Pickup complete",
            '5':  "Runner: Pickup complete", 
            '6':  "Pickup complete; Agree Dropoff Time",
            '7':  "Requester: Dropoff complete",
            '8':  "Runner: Dropoff complete",
            '9': "Delivery complete"}
    # NB If Requester confirms Dropoff complete, this must force: Delivery complete.
    # If Runner confirms Dropoff complete, this must force Runner: Pickup complete

@anvil.server.callable
def string_to_datetime(string, format = "%d %b %Y"):
    """Converts a date-like string to a datetime object"""
    return datetime.datetime.strptime(string, format)
  
@anvil.server.callable
def terms_accepted(boolean_value):
    """ Records today's date (or None) in the User database for Terms Accepted"""
    user = anvil.users.get_user()
    user['terms_accepted'] = datetime.datetime.today().date() if boolean_value else None

@anvil.server.callable
def update_offers_status(offer, status_code):
    user = anvil.users.get_user()
    if user is None:
        return
    offer.update(status = STATUSES()[status_code])
    
@anvil.server.callable
def update_requests_status(request, status_code):
    user = anvil.users.get_user()
    if user is None:
        return
    request.update(status = STATUSES()[status_code])
    
@anvil.server.callable
def volunteer_as_runner(match, boolean_value):
    """ Volunteer/unvolunteer as available_runner in Matches"""
    user = anvil.users.get_user()
    if boolean_value:
        match['available_runners'] += [user]
    else:
        match["available_runners"] = [x for x in match["available_runners"] if x != user]