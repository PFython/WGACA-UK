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
          
    def show_deliveries_row(self, **event_args):
        """This method is called when the DeliveriesRow is shown on the screen"""
        self.show_offer()
        self.show_request()
        self.show_runner()
        self.show_myself()
        self.populate_addresses()
        self.get_status_function(self.get_user_role(), "display")
        self.show_messages()
        
    def get_user_role(self):
        user = anvil.users.get_user()
        if self.item['offer']['user'] == user and self.item['approved_runner'] == user:
            return "Offerer+Runner"
        if self.item['approved_runner'] == user and self.item['request']['user'] == user:
            return ("Requester+Runner")
        if self.item['offer']['user'] == user and self.item['approved_runner'] != user:
            return "Offerer"
        if self.item['request']['user'] == user and self.item['approved_runner'] != user:
            return "Requester"
        if self.item['approved_runner'] == user:
            if self.item['request']['user'] != user:
                if self.item['offer']['user'] != user:  
                    return "Runner"
                  
    def get_status_function(self):
        lookup = {'3': self.status3,
          '4': self.status4,
          '5': self.status5,
          '6': self.status6,
          '7': self.status7,
          '8': self.status8,
          '9': self.status9,}
        status_code = self.item['status_code']       
        return lookup[status_code]                  
                  
    def make_status_active(self):
        self.status.enabled = True
        self.status.italic = False
            
    def make_status_inactive(self):
        self.status.enabled = False
        self.status.italic = True
        
    def status3(self, role, option = "display"):
    # NB ConfirmMatch will have already moved to status 6 if Offerer+Runner
        self.make_status_active if role in ("Offerer", "Runner", "Requester+Runner") else self.make_status_inactive()
        if role == "Offerer":
            self.status.text = "Please arrange pick-up with Runner, then click here to confirm they've collected your item(s)."
            self.click('4')
        if role == "Offerer+Runner":
            self.status.text = "You've picked up the item(s).  Please agree delivery with Requester."
        if role == "Runner" or role == "Requester+Runner":
            self.status.text = "Please arrange pick-up with Offerer, then click here to confirm you've collected their item(s)."
            self.click('5')
        if role == "Requester" :
          self.status.text = "Item(s) are waiting to be picked up."        

    def status4(self, role, option = "display"):
    # NB ConfirmMatch will have already moved to status 6 if Offerer+Runner
        self.make_status_active if role in ("Runner", "Requester+Runner") else self.make_status_inactive()
        if role == "Offerer":
            self.status.text = "Items have been picked up."
        if role == "Runner":
            self.status.text = "Please confirm you've picked up item(s) from the Offerer."
            self.click('6')
        if role == "Requester+Runner":
            self.status.text = "Items have been picked up."
            self.click('9')
        if role == "Requester":
            self.status.text = "Awaiting confirmation of pick-up."

    def status5(self, role, option = "display"):
    # NB ConfirmMatch will have already moved to status 6 if Offerer+Runner
        self.make_status_active if role in ("Offerer") else self.make_status_inactive()
        if role == "Offerer":
            self.status.text = "Please confirm the Runner has picked up item(s) from you."
            self.click('6')
        if role == "Runner":
            self.status.text = "Items have been picked up.  Please agree delivery with Requester."
        if role == "Requester+Runner":
            self.status.text = "Items picked up, delivery complete!"
        if role == "Requester":
            self.status.text = "Awaiting confirmation of pick-up."

    def status6(self, role, option = "display"):
        self.make_status_active if role in ("Runner", "Offerer+Runner") else self.make_status_inactive()
        if role == "Offerer":
            self.status.text = "You've given your item(s) to the Runner.  Thank you!"
        if role == "Runner" or role == "Offerer+Runner":
            self.status.text = "You've picked up the item(s).  Please click to confirm you've delivered them."
            self.click('8')
        if role == "Requester+Runner":
            self.status.text = "Items picked up, delivery complete!"
        if role == "Requester":
            self.status.text = "Runner has your item(s).  Please click to confirm once they've been delivered."
            self.click('7')
        
    def status7(self, role, option = "display"):
        self.make_status_active if role in ("Runner", "Offerer+Runner") else self.make_status_inactive()
        if role == "Offerer":
            self.status.text = "Awaiting confirmation of delivery"
        if role == "Runner" or role == "Offerer+Runner":
            self.status.text = "Please confirm you've dropped the item(s) off with the Requester."
            self.click('9')
        if role == "Requester":
            self.status.text = "Items dropped off, delivery complete!"
        if role == "Requester+Runner":
            self.status.text = "Items picked up, delivery complete!"
        
    def status8(self, role, option = "display"):
        self.make_status_active if role in ("Requester") else self.make_status_inactive()
        if role == "Offerer":
            self.status.text = "Awaiting confirmation of delivery"
        if role == "Runner" or role == "Offerer+Runner":
          self.status.text = "Items have been dropped off.  Awaiting final confirmation from Requester."  
        self.status.text = "Please click to give feedback on the Requester"
        if role == "Requester":
            self.status.text = "Please confirm item(s) have been dropped off by Runner."
            self.click('9')
        if role == "Requester+Runner":
            self.status.text = "Items picked up, delivery complete!"
    
    def status9(self, role, option = "display"):
        self.make_status_inactive()
        self.status.text = "Delivery complete.  What goes around comes around!"
        
    def click_update_status(self, **event_args):
        """
        Progress to next status_code where allowed, then trigger KarmaForm for feedback.
        show_deliveries_row already handles whether the checkbox is enabled.
        """
        self.get_status_function(self.get_user_role(), "click")

    def change_status(self, new_status):
        """Update to new status in status STATUSES and write to Matches, Offers, Requests tables"""        
#         anvil.server.call("save_to_matches_database", self.item, runner, messages, new_status)
#         anvil.server.call("update_offers_status", self.parent.parent.parent.item['offer'], new_status)
#         anvil.server.call("update_requests_status", self.parent.parent.parent.item['request'], new_status)
        anvil.server.call('update_status_codes', self.item, new_status)
        anvil.server.call('generate_matches')
        self.show_deliveries_row()
      
    def create_karma_form(self, user_role, regarding, regarding_role):
          form = KarmaForm()
          form.user.text = anvil.users.get_user()['display_name']
          form.user_role.text = user_role
          form.regarding.text = regarding
          form.regarding_role.text = regarding_role
          self.parent.parent.add_component(form)
              
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






