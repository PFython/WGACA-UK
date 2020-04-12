from ._anvil_designer import DeliveriesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...Globals import green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class DeliveriesRow(DeliveriesRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.

    def show_myself(self, **event_args):
        """Colour codes display to highlight user's own data"""
        user = anvil.users.get_user()

        if self.item['request']['user'] == user:
            self.label_1.text  = "My Request"
            self.label_1.foreground = green
            self.label_4.foreground = green
            self.dropoff.foreground = green
            self.dropoff.icon = 'fa:home'
            self.request.foreground = green
            self.request_notes.foreground = green

        if self.item['offer']['user'] == user:
            self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
            self.label_2.text  = "My Offer"            
            self.label_2.foreground = green
            self.label_3.foreground = green        
            self.pickup.foreground = green
            self.pickup.icon = 'fa:home'
            self.offer.foreground = green
            self.offer_notes.foreground = green
            self.offer_expiry.foreground = green
 
    def populate_addresses(self):
        """ Fills in address details for Pickup and Dropoff, adding postcode if authorised"""
        for address, table in {self.pickup: 'offer', self.dropoff: 'request'}.items():
            address.text = self.item[table]['user']['display_name']+"\n"
            address.text += str(self.item[table]['user']['house_number'])+" "
            address.text += self.item[table]['user']['street']+"\n"
            address.text += self.item[table]['user']['town']+"\n"
            address.text += self.item[table]['user']['county']+"\n"

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
    
    def show_offer(self):
        self.offer.text = self.item['offer']['product_key'] + " … "
        self.offer.text += str(self.item['offer']['units'])
        self.offer_expiry.text = self.item['offer']['expiry_date'].strftime('%d %b %Y')
        self.offer_notes.text = self.item['offer']['notes']
        
    def show_request(self):
        self.request.text = self.item['request']['product_category']
        self.request_notes.text = self.item['request']['notes']
       
    def show_runner(self):
        runner = self.item['approved_runner']['display_name']
        self.runner.text = "Approved Runner: " + runner
        if runner == anvil.users.get_user()['display_name']:
            self.runner.foreground = green
            # TODO: Buttons to send Runner messages to Offerer and Requester      
      
    def show_deliveries_row(self, **event_args):
        """This method is called when the DeliveriesRow is shown on the screen"""
        self.show_offer()
        self.show_request()
        self.show_runner()
        self.show_myself()
        self.populate_addresses()
        self.show_messages()        

    def click_show_message(self, **event_args):
        """This method is called when the Button is shown on the screen"""
        textbox = {self.message1: self.message1_text, self.message2: self.message2_text}[event_args['sender']]
        textbox.text = event_args['sender'].tag
        textbox.visible = True if event_args['sender'].icon == 'fa:caret-down' else False
        if event_args['sender'].icon == 'fa:caret-down':
            event_args['sender'].icon = 'fa:caret-up'
        else:
            event_args['sender'].icon = 'fa:caret-down'
        
            



