import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import datetime
import time

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
    app_tables.karma.add_row(**kwargs)

@anvil.server.callable
def check_for_display_name(display_name):
    """ Returns boolean check for whether display name already exists in Users database, or is simply invalid"""
    if display_name.startswith(" "):
      return True
    if display_name != None and display_name != "":
      return True if app_tables.users.get(display_name = display_name) else False

# @anvil.tables.in_transaction
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
    for request in (x for x in requests if x['status_code'] in ['1','2']):
        for offer in (x for x in offers if x['status_code'] in ['1','2']):
            if request['product_category'] in offer['product_key']:
                if request['user']['display_name'] != offer['user']['display_name']:
                    # check if new or existing match
                    if not app_tables.matches.get(request=request, offer=offer):
                        new_match =  app_tables.matches.add_row(available_runners = [], request = request, offer=offer, status_dict=get_initial_status_dict())
                        request.update(status_code = "2")
                        offer.update(status_code = "2")
                        new_match['route_url'] = create_route_url(new_match)
                        # 'or []' added to address possible database corruption i.e. value = None rather than value = []
                        if new_match not in (offer['matches'] or []):
                            offer['matches'] = (offer['matches'] or []) + [new_match]
                        if new_match not in (request['matches'] or []):
                            request['matches'] = (request['matches'] or []) + [new_match]                    
                            
def get_initial_status_dict():
    return  {"offer_matched":True,
             "runner_selected":True,
             "pickup_agreed":False,
             "offerer_confirms_pickup":False,
             "dropoff_agreed":False,
             "feedback_REQ_on_RUN":False,
             "feedback_RUN_on_OFF":False,
             "delivery":False,
             "requester_confirms_dropoff":False,
             "feedback_RUN_on_REQ":False,
             "feedback_OFF_on_RUN":False,
             "runner_confirms_pickup":False,
             "runner_confirms_dropoff":False}

@anvil.server.callable  
def get_status_message_from_status_dict(match):
      try:
          status = match['status_dict']
          if status['delivery']:
              return "Delivery complete!  What goes around comes around..."    
          if status['dropoff_agreed'] and match['approved_runner'] != match['request']['user']:
              return "A Dropoff time has been agreed between the Requester and Runner."
          if status['offerer_confirms_pickup'] and status['runner_confirms_pickup']:
              return "Both the Offerer and Runner have confirmed Pickup is complete."
          if status['offerer_confirms_pickup'] and not status['runner_confirms_pickup']:
              return "The Offerer (only) has confirmed Pickup is complete."
          if not status['offerer_confirms_pickup'] and status['runner_confirms_pickup']:
              return "The Runner (only) has confirmed Pickup is complete."        
          if status['pickup_agreed'] and match['approved_runner'] != match['offer']['user']:
              return "A Pickup time has been agreed between the Offerer and Runner."
          if status['runner_selected']:
              return f"The offerer has confirmed {match['approved_runner']['display_name']} as the Runner."
          if status['offer_matched']:
              return f"This request has been... "
      except anvil.tables.TableError:
      # Match hasn't been created yet and isn't a match at all but an offer or request.
          try:
              x = match['product_category']
              row_type = "Request"
              alt_row_type = "Offer(s)"
          except KeyError:
              row_type = "Offer"
              alt_row_type = "Request(s)"
          match_count = len(self.item['matches'])
          if match['status_code'] == "Matches Exist":
              return f"This {row_type} has been matched with {match_count} {alt_row_type}. Click on the Matches menu for more information."
          if match['status_code'] == "New":
              return f"This {row_type} currently has no matched {alt_row_type}.  Check back regularly!"
          
                        
                            
def create_route_url(new_match):
    """Creates an Open Street Map url for pickup to dropoff route"""
    pickup_lon_lat = new_match['offer']['user']['approx_lon_lat']
    dropoff_lon_lat = new_match['request']['user']['approx_lon_lat']
    osm = "https://www.openstreetmap.org/directions?engine=graphhopper_foot&route="
    osm += pickup_lon_lat + "%3B" + dropoff_lon_lat
    print(osm)
    return osm

@anvil.server.callable
def save_approx_lon_lat(user="default"):
    "Fetches and saves approximate Longitude and Latitude for a given user's address"
    if user == "default":
        user = anvil.users.get_user()
    if user != None:
        address = [user['street'], user['town'], user['county']]
        try:
            address_data = nominatim_scrape(address)[0]
            user['approx_lon_lat'] = address_data['lat'] + "%2C" + address_data['lon']
        except IndexError:
            print(f"Problem getting Nominatim data for {address}")


# @anvil.tables.in_transaction
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
def get_match_by_id(row_id):
    if anvil.users.get_user() is not None:
        return app_tables.matches.get_by_id(row_id)
  
  
@anvil.server.callable
def get_my_deliveries():
    """ Returns rows from the Matches database where runner = user """
    if anvil.users.get_user() is not None:
        return [x for x in app_tables.matches.search() if x['approved_runner'] != None]

@anvil.server.callable
def get_my_matches():
    """ Returns rows from the Matches database """
    if anvil.users.get_user() is not None:
        return app_tables.matches.search(approved_runner=None)
        # When approved_runner != None, the Match effectively becomes a Delivery
        # TODO: Filter results by proximity

@anvil.server.callable
def _get_all_matches():
    return app_tables.matches.search()
  
@anvil.server.callable
def _get_test_match():
    return app_tables.matches.get()

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

# @anvil.tables.in_transaction
def nominatim_scrape(address_list):
    """Returns location & address dictionary for supplied address list"""
    nominatim = 'https://nominatim.openstreetmap.org/search?q='
    nominatim += f"{','.join(address_list).replace(', ',',').replace('&','%26')},{LOCALE},&format=json".replace(" ","%20")
    return anvil.http.request(nominatim, json=True)
  
# @anvil.tables.in_transaction  
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

# @anvil.tables.in_transaction      
@anvil.server.callable
def save_to_matches_database(match, runner, messages, status_dict):
    """ Returns 'Duplicate' if product_category request already exists"""
    if anvil.users.get_user() is None:
        return
    match.update(approved_runner = runner, messages_dict = messages, status_dict = status_dict)

# @anvil.tables.in_transaction
@anvil.server.callable
def save_matches_status_dict(match, status_dict):
    match.update(status_dict = status_dict)
    
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
    anvil.users.get_user()[field] = value
  
@anvil.server.callable
def string_to_datetime(string, format = "%d %b %Y"):
    """Converts a date-like string to a datetime object"""
    return datetime.datetime.strptime(string, format)
  
@anvil.server.callable
def terms_accepted(boolean_value):
    """ Records today's date (or None) in the User database for Terms Accepted"""
    anvil.users.get_user()['terms_accepted'] = datetime.datetime.today().date() if boolean_value else None

@anvil.server.callable
def update_offers_status(offer, status_code):
    if anvil.users.get_user() is None:
        return
    offer.update(status_code = status_code)
    
@anvil.server.callable
def update_requests_status(request, status_code):
    if anvil.users.get_user() is None:
        return
    request.update(status_code = status_code)

# @anvil.tables.in_transaction
@anvil.server.callable
def update_status_codes(match, new_status_code):
    match['request']['status_code'] = new_status_code
    match['offer']['status_code'] = new_status_code

# @anvil.tables.in_transaction    
@anvil.server.callable
def volunteer_as_runner(match, boolean_value):
    """ Volunteer/unvolunteer as available_runner in Matches"""
    user = anvil.users.get_user()
    if boolean_value:
        match['available_runners'] += [user]
    else:
        match["available_runners"] = [x for x in match["available_runners"] if x != user]
        
@anvil.server.callable
def _backfill_approx_lon_lat():
    for user in app_tables.users.search():
        if not user['approx_lon_lat']:
            print(f"Updating approx location for user {user['display_name']}")
            save_approx_lon_lat(user)
            time.sleep(1.5)
  