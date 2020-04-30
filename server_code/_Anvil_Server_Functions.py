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

LOCALE = "United Kingdom"

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.

print("_Anvil_Server_Functions")

# DEVELOPER TOOLS

@anvil.server.callable
def _backfill_approx_lon_lat():
    for user in app_tables.users.search():
        if not user['approx_lon_lat']:
            print(f"Updating approx location for user {user['display_name']}")
            save_approx_lon_lat(user)
            time.sleep(1.5)

def admin(func):
      """ Function only available to admin users """
      def wrapper(*args, **kwargs):
          if not anvil.users.get_user()['admin']:
              print("⚠ Sorry, you do not have permission to run this function.")
              return False
          else:
            data = func(*args, **kwargs)
            return (data)
      return wrapper

@anvil.server.callable("_store_uploaded_media")
@admin
def _store_uploaded_media(media, custom_name):
    media_upload = app_tables.uploads.add_row(name=custom_name, media = media, datetime = datetime.datetime.now())
    print(f"{media.name} saved to uploads databases as {custom_name}.")
    return media_upload

@anvil.server.callable("_convert_old_addresses")
@admin
def _convert_old_addresses():
    """
    Old addresses had separate fields for Street, Town, and County
    New addresses are a single combined text field
    """
    all_users = app_tables.users.search()
    for user in all_users:
        address = f"{user['street']}; {user['town']}; {user['county']}"
        user['address'] = address
        user['valid_address'] = True
        print(address)
        
@anvil.server.callable("_scratch_offers_matches_requests")
@admin
def _scratch_offers_matches_requests():
    for table in [app_tables.matches,  app_tables.requests,  app_tables.offers]:
        table.delete_all_rows()
        print(table,"deleted!")
            
@anvil.server.callable
def _get_test_match():
    return app_tables.matches.get()
    
# GET DATA    

@anvil.server.callable
def string_to_datetime(string, format = "%d %b %Y"):
    """Converts a date-like string to a datetime object"""
    return datetime.datetime.strptime(string, format)

@anvil.server.callable
def get_initial_address_matches(text, max_options):
    print("get_initial_address_matches")
    new_options = []
    text = text.lower()
    address_media = [x for x in app_tables.uploads.search(tables.order_by("datetime"), name="Address_Data_UK") if 'OS' in x['media'].name]
    address_lines = address_media[0]['media'].get_bytes().decode('utf-8')
    data = address_lines.split("\n")
    for option in data:
      if option.lower().startswith(text):
          new_options.append(option)
          if len(new_options) == max_options:
              break
    return sorted(new_options)
  
@anvil.server.callable
def get_product_list(filter):
    """
    Filters the list of product descriptions and returns a list for dropdown menu
    Filter can be 'all', 'street', 'town' or 'county'
    """
    position = {'street': 0, 'town': 1, 'county': 2}[filter]
    requests = app_tables.requests.search()
    print(len(requests),"requests found.")    
    requests = [x for x in requests if x['user']['address'].split("; ")[position] == anvil.users.get_user()['address'].split("; ")[position]]
    print(len(requests), "requests when filtered by", filter)  
    product_categories = {x['product_category'] for x in requests}
    print(product_categories)
    product_list = []
    ITEM_HEIRARCHY = get_product_hierarchy()
    for product_category in product_categories:
        product_list += [x for x in ITEM_HEIRARCHY if product_category in x]    
    return sorted(list(product_list))
  
@anvil.server.callable
def check_for_display_name(display_name):
    """ Returns boolean check for whether display name already exists in Users database, or is simply invalid"""
    if display_name.startswith(" "):
      return True
    if display_name != None and display_name != "":
      return True if app_tables.users.get(display_name = display_name) else False
    
                            
def get_initial_status_dict():
    return  {"offer_matched":True,
             "runner_selected":True,
             "pickup_agreed":False,
             "offerer_confirms_pickup":False,
             "dropoff_agreed":False,
             "delivery":False,
             "requester_confirms_dropoff":False,
             "runner_confirms_pickup":False,
             "runner_confirms_dropoff":False}
              
@anvil.server.callable  
def get_status_message_from_match(data_row):
    status = data_row['status_dict']
    if status['delivery']:
        return "Delivery complete!  What goes around comes around..."    
    if status['dropoff_agreed'] and data_row['approved_runner'] != data_row['request']['user']:
        return "A Dropoff time has been agreed between the Requester and Runner."
    if status['offerer_confirms_pickup'] and status['runner_confirms_pickup']:
        return "Both the Offerer and Runner have confirmed Pickup is complete."
    if status['offerer_confirms_pickup'] and not status['runner_confirms_pickup']:
        return "The Offerer (only) has confirmed Pickup is complete."
    if not status['offerer_confirms_pickup'] and status['runner_confirms_pickup']:
        return "The Runner (only) has confirmed Pickup is complete."        
    if status['pickup_agreed'] and data_row['approved_runner'] != data_row['offer']['user']:
        return "A Pickup time has been agreed between the Offerer and Runner."
    if status['runner_selected']:
        return f"The offerer has confirmed {data_row['approved_runner']['display_name']} as the Runner."
    if status['offer_matched']:
        return f"This request has been... "
      
@anvil.server.callable  
def get_status_message(data_row):
    try:
        status = data_row['status_dict']
        # data_row is a Match
        return get_status_message_from_match(data_row)
    except anvil.tables.TableError:
    # data_row is an Offer or Request
        try:
            x = data_row['product_category']
            row_type = "Request"
            alt_row_type = "Offer(s)"
        except anvil.tables.TableError:
            row_type = "Offer"
            alt_row_type = "Request(s)"
        match_count = len(data_row['matches'])
        if data_row['matches']:
            for match in data_row['matches']:
                if match['approved_runner'] != None:
                    # match is THE Match
                    break
            if match['approved_runner'] != None:
                status = match['status_dict']
                return get_status_message_from_match(match)
        if data_row['status_code'] == "Matches Exist":
            return f"This {row_type} has been matched with {match_count} {alt_row_type}. Click on the Matches menu for more information."
        if data_row['status_code'] == "New":
            return f"This {row_type} currently has no matched {alt_row_type}.  Check back regularly!"   


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
def get_karma_forms_from_user(match):
    return app_tables.karma.search(regarding_match=match, from_user = anvil.users.get_user())
        

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

@anvil.server.callable
def get_chat_text(row_id):
    return app_tables.matches.get_by_id(row_id)['chat']  
          
# POST DATA

@anvil.server.callable
def add_karma_row(**kwargs):
    return app_tables.karma.add_row(**kwargs)
  
# @anvil.tables.in_transaction    
@anvil.server.callable
def save_to_chat(row_id, full_text):
    """Saves full chat history to Match"""
    if anvil.users.get_user() is None:
        return
    match = app_tables.matches.get_by_id(row_id)
    match.update(chat = full_text)   

# @anvil.tables.in_transaction      
@anvil.server.callable
def save_to_matches_database(match, runner, status_dict):
    """ Returns 'Duplicate' if product_category request already exists"""
    if anvil.users.get_user() is None:
        return
    match.update(approved_runner = runner,status_dict = status_dict)

# @anvil.tables.in_transaction
@anvil.server.callable
def save_matches_status_dict(match, status_dict):
    match.update(status_dict = status_dict)
    
@anvil.server.callable
def save_to_offers_database(product_key, units, expiry_date, notes, status_code="New"):
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
def save_to_requests_database(product_category, urgent, notes, status_code="New"):
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
def save_karma_form_to_match(row_id,karma_form):
    match = app_tables.matches.get_by_id(row_id)
    forms = match['karma_forms'] or []
    forms += [karma_form]
    match['karma_forms'] = list(set(forms))  
  
@anvil.server.callable
def terms_accepted(boolean_value):
    """ Records today's date (or None) in the User database for Terms Accepted"""
    anvil.users.get_user()['terms_accepted'] = datetime.datetime.today().date() if boolean_value else None

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
    


# PROCESS DATA

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
    for request in (x for x in requests if x['status_code'] in ['New','Matches Exist']):
        for offer in (x for x in offers if x['status_code'] in ['New','Matches Exist']):
            if request['product_category'] in offer['product_key']:
                if request['user']['display_name'] != offer['user']['display_name']:
                    # check if new or existing match
                    if not app_tables.matches.get(request=request, offer=offer):
                        new_match =  app_tables.matches.add_row(available_runners = [], request = request, offer=offer, status_dict=get_initial_status_dict())
                        request.update(status_code = "Matches Exist")
                        offer.update(status_code = "Matches Exist")
                        new_match['route_url'] = create_route_url(new_match)
                        # 'or []' added to address possible database corruption i.e. value = None rather than value = []
                        if new_match not in (offer['matches'] or []):
                            offer['matches'] = (offer['matches'] or []) + [new_match]
                        if new_match not in (request['matches'] or []):
                            request['matches'] = (request['matches'] or []) + [new_match]             
                            
def create_route_url(new_match):
    """Creates an Open Street Map url for pickup to dropoff route"""
    pickup_lon_lat = new_match['offer']['user']['approx_lon_lat']
    dropoff_lon_lat = new_match['request']['user']['approx_lon_lat']
    osm = "https://www.openstreetmap.org/directions?engine=graphhopper_foot&route="
    osm += pickup_lon_lat + "%3B" + dropoff_lon_lat
    print("Request sent to OpenStreetView:")
    print(osm)
    return osm

@anvil.server.callable
def save_approx_lon_lat(user="default"):
    "Fetches and saves approximate Longitude and Latitude for a given user's address"
    if user == "default":
        user = anvil.users.get_user()
    if user != None:
        address = user['address'].split("; ")
        try:
            address_data = nominatim_scrape(address)[0]
            user['approx_lon_lat'] = address_data['lat'] + "%2C" + address_data['lon']
        except IndexError:
            print(f"Problem getting Nominatim data for {address}")

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
     