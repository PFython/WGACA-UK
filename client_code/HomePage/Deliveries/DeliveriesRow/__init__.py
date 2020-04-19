from ._anvil_designer import DeliveriesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .KarmaForm import KarmaForm
import datetime

from ....Globals import green, grey, red, blue, dark_green, light_green, light_blue, pale_blue, bright_blue, white, red, yellow, pink, black
from ....Globals import STATUSES
from .StatusView import StatusView

class DeliveriesRow(DeliveriesRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.show_route.url = self.item['route_url']
        self.show_route.foreground = dark_green
        self.user = anvil.users.get_user()
               
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
        if runner == self.user['display_name']:
            self.runner.foreground = dark_green
            self.status_label.foreground = dark_green
            self.show_route.foreground = dark_green
        else:
            self.show_route.foreground = black
            
    def show_status(self):
        status = self.item['status_dict']
        if status:
            if not status['pickup_agreed'] or not status['dropoff_agreed']:
                colour = yellow
            if status['delivery']:
                colour = light_green
            self.column_panel_1.background = colour
            
    def show_myself(self, **event_args):
        """Colour codes display to highlight user's own data"""
        if self.item['offer']['user'] == self.user:
#             self.items_picked_up.foreground = dark_green
            self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
            self.label_2.text  = "My Offer"            
            self.label_2.foreground = dark_green
            self.label_3.foreground = dark_green        
            self.pickup.foreground = dark_green
            self.pickup.icon = 'fa:home'
            self.offer.foreground = dark_green
            self.offer_notes.foreground = dark_green
            self.offer_expiry.foreground = dark_green              
        if self.item['request']['user'] == self.user:
            self.label_1.text  = "My Request"
            self.label_1.foreground = dark_green
            self.label_4.foreground = dark_green
            self.dropoff.foreground = dark_green
            self.dropoff.icon = 'fa:home'
            self.request.foreground = dark_green
            self.request_notes.foreground = dark_green    

   
    def populate_addresses(self):
        """ Fills in address details for Pickup and Dropoff, adding postcode if authorised"""
        for address, table in {self.pickup: 'offer', self.dropoff: 'request'}.items():
            address.text = self.item[table]['user']['display_name']+"\n"
            if self.item['approved_runner'] == self.user or self.item[table]['user'] == self.user:
                address.text += str(self.item[table]['user']['house_number'])+" "
            address.text += self.item[table]['user']['street']+", "
            address.text += self.item[table]['user']['town']+", "
            address.text += self.item[table]['user']['county']+"\n"
          
    def show_deliveries_row(self, **event_args):
        """This method is called when the DeliveriesRow is shown on the screen"""
        self.show_offer()
        self.show_request()
        self.show_runner()
        self.show_myself()
        self.show_status()
        self.populate_addresses()
        self.combine_messages()
        self.row_id.text = self.item.get_id()
          
    def create_karma_form(self, user_role, regarding, regarding_role):
          form = KarmaForm()
          form.user.text = self.user['display_name']
          form.user_role.text = user_role
          form.regarding.text = regarding
          form.regarding_role.text = regarding_role
          self.parent.parent.add_component(form)
              
    def combine_messages(self):
        messages = self.item['messages_dict']
        # Remove unauthorised messages for user
        keys = 'offerer_to_runner runner_to_offerer runner_to_requester requester_to_runner'.split()
        if self.user != self.item['offer']['user'] and keys[1] in messages:
            del messages[keys[1]]
        if self.user != self.item['request']['user'] and keys[2] in messages:
            del messages[keys[2]]
        if self.user != self.item['approved_runner']:
            for k in (keys[1], keys[2]):
                if k in messages:
                    del messages[k]
        self.textbox.text = ""
        for address, message in self.item['messages_dict'].items():
            if message.replace("\n",""):
                self.textbox.text += address.replace("_"," ").upper() + ":\n"
                self.textbox.text += message + "\n"
        if not self.textbox.text:
            self.show_message.enabled = False
            self.show_message.background = grey
    
    def click_show_message(self, **event_args):
        """This method is called when a Message Button is shown on the screen"""
        sender = event_args['sender']
        self.textbox.visible = True if sender.icon == 'fa:caret-down' and self.textbox.text else False
        sender.icon = 'fa:caret-up' if self.textbox.visible else 'fa:caret-down'       

    def disable_similar_buttons(self, enabled = False):
        for row in [x for x in self.parent.get_components()]:
            columns = row.get_components()
            for column in columns:
                buttons = [x for x in column.get_components() if type(x) == Button]
                button = [x for x in buttons  if "Delivery Status" in x.text]
                button[0].enabled = not enabled
            
    def click_status_view(self, **event_args):
        """This method is called when the Status View button is clicked"""
        status_view = StatusView(self.item)
        status_view.row_id.text = self.row_id.text
        status_view.match = self.item
        status_view.visible = True
        sender = event_args['sender']
        self.disable_similar_buttons(sender)
        self.status_view_panel.add_component(status_view)
        self.status_view_panel.visible = True
            








