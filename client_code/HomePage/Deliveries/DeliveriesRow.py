from ._anvil_designer import DeliveriesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DeliveriesRow(DeliveriesRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.

    def show_myself(self, **event_args):
        """Colour codes display to highlight user's own data"""
        user = anvil.users.get_user()
        # Green: #5eb348
        # Blue: #0080c0
        # Red: #ff8080
        if self.item['request']['user'] == user:
            self.label_1.text  = "My Request"
            self.label_1.foreground = '#5eb348'
            self.label_4.foreground = '#5eb348'
            self.dropoff.foreground = '#5eb348'
            self.dropoff.icon = 'fa:home'
            self.request.foreground = '#5eb348'
            self.request_notes.foreground = '#5eb348'

        if self.item['offer']['user'] == user:
            self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
            self.label_2.text  = "My Offer"
            self.label_2.foreground = '#5eb348'
            self.label_3.foreground = '#5eb348'        
            self.pickup.foreground = '#5eb348'
            self.pickup.icon = 'fa:home'
            self.offer.foreground = '#5eb348'
            self.offer_notes.foreground = '#5eb348'
            self.confirm_match.visible = True
            self.volunteer_toggle.visible = False        
 
    def populate_addresses(self):
        """ Fills in address details for Pickup and Dropoff, adding postcode if authorised"""
        for address, table in {self.pickup: 'offer', self.dropoff: 'request'}.items():
            address.text = self.item[table]['user']['display_name']+"\n"
            address.text += str(self.item[table]['user']['house_number'])+" "
            address.text += self.item[table]['user']['street']+"\n"
            address.text += self.item[table]['user']['town']+"\n"
            address.text += self.item[table]['user']['county']+"\n"

    def expose_messages(self):
        user = anvil.users.get_user()
        messages = self.item['messages_dict']
        if user == self.item['offer']['user'] :
            self.message1.text = " Message from Runner"
            self.message1.tag = messages.get('runner_to_offerer')
            self.message2.text = " Message from Requester"
            self.message2.tag = messages.get('requester_to_offerer')
            self.pickup.text += self.item['offer']['user']['postcode'] or ""

        if user == self.item['approved_runner'] :
            self.message1.text = " Message from Offerer"
            self.message1.tag = messages.get('offerer_to_runner')
            self.message2.text = " Message from Requester"
            self.message2.tag = messages.get('requester_to_runner')

        if user == self.item['request']['user'] :
            self.message1.text = " Message from Offerer"
            self.message1.tag = messages.get('offerer_to_requester') 
            self.message2.text = " Message from Runner"
            self.message2.tag = messages.get('runner_to_requester')
            self.dropoff.text += self.item['offer']['user']['postcode'] or ""
            if user in self.item['offer']['user']['postcode_shared_with']:
                self.pickup.text += self.item['offer']['user']['postcode'] or ""
            
        for message in (self.message1, self.message2):
            message.tag = message.tag or ""
            message.tag = message.tag.strip()
            if not message.tag:
#                 message.visible = False # Comment in for production, comment out during Test
                message.enabled = False
  
  
    def show_deliveries_row(self, **event_args):
        """This method is called when the DeliveriesRow is shown on the screen"""
        self.show_myself()
        self.populate_addresses()
        self.expose_messages()
        

    def click_show_message(self, **event_args):
        """This method is called when the Button is shown on the screen"""
        textbox = {self.message1: self.message1_text, self.message2: self.message2_text}[event_args['sender']]
        textbox.text = event_args['sender'].tag
        textbox.visible = True if event_args['sender'].icon == 'fa:caret-down' else False
        if event_args['sender'].icon == 'fa:caret-down':
            event_args['sender'].icon = 'fa:caret-up'
        else:
            event_args['sender'].icon = 'fa:caret-down'
        
            



