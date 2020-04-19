import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

green = '#5eb348'
dark_green = '#3d732f'
light_green = '#bbdfb3'
grey = '#d8d8d8'
red = '#ff8080'
blue = '#0080c0'
light_blue = '#cae4ff'
pale_blue = '#eaf4ff'
bright_blue = '#00a3f0'
white = "#ffffff"
pink = '#ffe6e6'
yellow = '#fefdc7'
dark_blue = '#0000ff'
black = '#3b3b3b'

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)
ITEM_HEIRARCHY = anvil.server.call("get_product_hierarchy")
UNITS_OF_MEASURE = anvil.server.call("get_units_of_measure")

STATUSES = {'1':  "New item(s) created",
            '2':  "Match found!",
            '3':  "Need to agree Pickup time",
            '4':  "Need to agree Dropoff time",
            '5':  "Urgent - expiry date close", 
            '6':  "Status Code 6",
            '7':  "Status Code 7",
            '8':  "Status Code 9",
            '9': "Delivery complete"}
