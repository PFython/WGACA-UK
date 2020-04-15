from ._anvil_designer import DeliveriesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .KarmaForm import KarmaForm
import datetime

from ...Globals import green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink
from ...Globals import STATUSES

class DeliveriesRow(DeliveriesRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.show_route.url = self.item['route_url']
        self.show_route.foreground = green
#         self.items_picked_up.visible = False
#         self.items_dropped_off.visible = False

    def show_deliveries_row(self, **event_args):
        """This method is called when the DeliveriesRow is shown on the screen"""
        self.show_offer()
        self.show_request()
        self.show_runner()
        self.show_myself()
        self.populate_addresses()
        user = anvil.users.get_user()
        if user == self.item['offer']['user'] and user != self.item['approved_runner']:
            self.show_offerer_status()
        if user == self.item['approved_runner']:
            self.show_runner_status()
        if user == self.item['request']['user']:
            self.show_requester_status()
        self.show_messages() 
            
    def show_offer(self):
        self.offer.text = self.item['offer']['product_key'] + " … "
        self.offer.text += str(self.item['offer']['units'])
        expiry = self.item['offer']['expiry_date']
        self.offer_expiry.text = expiry.strftime('%d %b %Y')
        if expiry <= datetime.datetime.today():
            self.offer_expiry.foreground = red
        self.offer_notes.text = self.item['offer']['notes']
        expiry = self.item['offer']['expiry_date']
        self.offer_expiry.text = expiry.strftime('%d %b %Y')
        if expiry <= datetime.datetime.today():
              self.offer_expiry.foreground = red
        
    def show_request(self):
        self.request.text = self.item['request']['product_category']
        self.request_notes.text = self.item['request']['notes']
       
    def show_runner(self):
        runner = self.item['approved_runner']['display_name']
        self.runner.text = "Approved Runner: " + runner
        if runner == anvil.users.get_user()['display_name']:
            self.runner.foreground = green
            
    def show_myself(self, **event_args):
        """Colour codes display to highlight user's own data"""
        user = anvil.users.get_user()
        if self.item['offer']['user'] == user:
#             self.items_picked_up.foreground = green
            self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
            self.label_2.text  = "My Offer"            
            self.label_2.foreground = green
            self.label_3.foreground = green        
            self.pickup.foreground = green
            self.pickup.icon = 'fa:home'
            self.offer.foreground = green
            self.offer_notes.foreground = green
            self.offer_expiry.foreground = green              
        if self.item['request']['user'] == user:
            self.label_1.text  = "My Request"
            self.label_1.foreground = green
            self.label_4.foreground = green
            self.dropoff.foreground = green
            self.dropoff.icon = 'fa:home'
            self.request.foreground = green
            self.request_notes.foreground = green      
   
    def populate_addresses(self):
        """ Fills in address details for Pickup and Dropoff, adding postcode if authorised"""
        user=anvil.users.get_user()
        for address, table in {self.pickup: 'offer', self.dropoff: 'request'}.items():
            address.text = self.item[table]['user']['display_name']+"\n"
            if self.item['approved_runner'] == user or self.item[table]['user'] == user:
                address.text += str(self.item[table]['user']['house_number'])+" "
            address.text += self.item[table]['user']['street']+"\n"
            address.text += self.item[table]['user']['town']+"\n"
            address.text += self.item[table]['user']['county']+"\n"
            
    def show_offerer_status(self):
        """ Enables and selects relevant status prompt for Offerer"""
        if self.item['status_code'] == '3':
            print("Offerer,3")
            self.status.enabled = True
            self.status.visible = True
            self.status.text = "Please arrange pick-up with Runner, then click here to confirm they've collected your item(s)."
        else:
            print("Offerer, not 3")
            self.status.enabled = False
            self.status.visible = True
            self.status.text = anvil.server.call("general_status_messages", self.item['status_code'])
    
    def show_runner_status(self):
        """ Enables and selects relevant status prompt for Runner"""
        if self.item['status_code'] in ['3','4']:
            print(f"Runner,3 or 4/{self.item['status_code']}")
            self.status.enabled = True
            self.status.visible = True
            self.status.text = "Please arrange pick-up with Offerer, then click here to confirm you've collected their item(s)."
        elif self.item['status_code'] == '6':
            print(f"Runner,6/{self.item['status_code']}")
            self.status.enabled = True
            self.status.visible = True
            self.status.text = "Please arrange drop-off with Requester, then click here to confirm you've delivered the item(s)."
        else:
            print(f"Runner, not 3,4, or 6/{self.item['status_code']}")
            self.status.enabled = False
            self.status.visible = True
            self.status.text = anvil.server.call("general_status_messages", self.item['status_code'])
    
    def show_requester_status(self):
        """ Enables and selects relevant status prompt for Requester"""  
        if self.item['status_code'] == '6':
            print("Requester,6")
            self.status.enabled = True
            self.status.visible = True
            self.status.text = "Please arrange drop-off with Runner, then click here to confirm you've received the item(s)."
        else:
            print("Requester, not 6")
            self.status.enabled = False
            self.status.visible = True
            self.status.text = anvil.server.call("general_status_messages", self.item['status_code'])
     
    def change_status(self, new_status):
        """Update to new status in status STATUSES and write to Matches, Offers, Requests tables"""        
#         anvil.server.call("save_to_matches_database", self.item, runner, messages, new_status)
#         anvil.server.call("update_offers_status", self.parent.parent.parent.item['offer'], new_status)
#         anvil.server.call("update_requests_status", self.parent.parent.parent.item['request'], new_status)
        anvil.server.call('update_status_codes', self.item, new_status)
        # 3 in STATUSES = "Runner confirmed"
        anvil.server.call('generate_matches')
        self.show_deliveries_row()
      
    def create_karma_form(self, user_role, regarding, regarding_role):
          form = KarmaForm()
          form.user = anvil.users.get_user()
          self.add_component(form)
          
    def click_update_status(self, **event_args):
        """Define user's role and the name/role of the person for use in the Karma Form"""
        user = anvil.users.get_user()
        if self.item['offer']['user'] == user and self.item['status_code'] == '3':
        # Offerer can confirm pickup complete and submit KarmaForm for Runner
            self.change_status('4')
            self.create_karma_form("Offerer", self.item['approved_runner']['display_name'], "Runner")
        if self.item['approved_runner'] == user:
        # Runner can confirm pickup complete and submit KarmaForm for Offerer
        # Runner can confirm dropoff complete and submit KarmaForm for Requester
            if self.item['status_code'] == '3':
                self.change_status('5')
                self.create_karma_form("Runner", self.item['offer']['user']['display_name'], "Offerer")              
            if self.item['status_code'] == '4':
                self.change_status('6')
                self.create_karma_form("Runner", self.item['offer']['user']['display_name'], "Offerer")
            if self.item['status_code'] == '6':
                self.change_status('8')
                self.create_karma_form("Runner", self.item['request']['user']['display_name'], "Requester")
            if self.item['status_code'] == '7':
                self.change_status('9')            
                self.create_karma_form("Runner", self.item['request']['user']['display_name'], "Requester")
        if self.item['request']['user'] == user:
        # Requester can confirm dropoff complete and submit KarmaForm for Runner
            if self.item['status_code'] == '6':
                self.change_status('7')
                self.create_karma_form("Requester", self.item['approved_runner']['display_name'], "Runner")
            if self.item['status_code'] == '8':
                self.change_status('9')
                self.create_karma_form("Requester", self.item['approved_runner']['display_name'], "Runner")
      
    def show_messages(self):
        user = anvil.users.get_user()
        messages = self.item['messages_dict']
        if user == self.item['offer']['user'] :
            self.message1.text = " Message from Runner"
            self.message1.tag = messages.get('runner_to_offerer')
            self.pickup.text += self.item['offer']['user']['postcode'] or ""
            self.message2.visible = False

        if user == self.item['approved_runner'] :
            self.message1.text = " Message from Offerer"
            self.message1.tag = messages.get('offerer_to_runner')
            self.message2.text = " Message from Requester"
            self.message2.tag = messages.get('requester_to_runner')
            # Check if Runner is authorised to see Request/Offer postcodes
            for shared, address in {self.item['offer']: self.pickup,
                                    self.item['request']: self.dropoff}.items():
                post_code_shared = shared['user']['postcode_shared_with'] or []
                if user in post_code_shared:
                    address.text += self.item['offer']['user']['postcode'] or ""

        if user == self.item['request']['user'] :
            self.message2.text = " Message from Runner"
            self.message2.tag = messages.get('runner_to_requester')
            self.dropoff.text += self.item['offer']['user']['postcode'] or ""
            self.message1.visible = False
            
        for message in (self.message1, self.message2):
            message.tag = message.tag or ""
            message.tag = str(message.tag).strip()
            if not message.tag:
                message.enabled = False
                message.background = grey
    
    def click_show_message(self, **event_args):
        """This method is called when a Message Button is shown on the screen"""
        textbox = {self.message1: self.message1_text, self.message2: self.message2_text}[event_args['sender']]
        textbox.text = event_args['sender'].tag
        textbox.visible = True if event_args['sender'].icon == 'fa:caret-down' else False
        if event_args['sender'].icon == 'fa:caret-down':
            event_args['sender'].icon = 'fa:caret-up'
        else:
            event_args['sender'].icon = 'fa:caret-down'       






