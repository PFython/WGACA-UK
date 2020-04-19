from ._anvil_designer import DeliveriesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .KarmaForm import KarmaForm
import datetime

from ....Globals import green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink, black
from ....Globals import STATUSES
from .StatusView import StatusView

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
            self.status_label.foreground = green
            self.show_route.foreground = green
        else:
            self.show_route.foreground = black
            
    def show_status(self):
        status = self.item.get('status_dict')
        if status:
            if status['delivery'].checked:
                self.column_panel_1.background = Green
            
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
          form.user.text = anvil.users.get_user()['display_name']
          form.user_role.text = user_role
          form.regarding.text = regarding
          form.regarding_role.text = regarding_role
          self.parent.parent.add_component(form)
              
    def combine_messages(self):
        user = anvil.users.get_user()
        messages = self.item['messages_dict']
        # Remove unauthorised messages for user
        keys = 'offerer_to_runner runner_to_offerer runner_to_requester requester_to_runner'.split()
        if user != self.item['offer']['user'] and keys[1] in messages:
            del messages[keys[1]]
        if user != self.item['request']['user'] and keys[2] in messages:
            del messages[keys[2]]
        if user != self.item['approved_runner']:
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
            








