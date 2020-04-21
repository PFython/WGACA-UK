from ._anvil_designer import DeliveriesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import datetime

from ....Globals import green, grey, red, blue, dark_green, light_green, light_blue, pale_blue, bright_blue, white, red, yellow, pink, black
from .StatusView import StatusView
from .KarmaForm import KarmaForm

class DeliveriesRow(DeliveriesRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.show_route.url = self.item['route_url']
        self.show_route.foreground = dark_green
        self.user = anvil.users.get_user()
        self.feedback = [self.feedback_on_offerer,
                 self.feedback_on_runner,
                 self.feedback_on_requester,]
               
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
              self.offer_expiry.bold = True
              self.offer_expiry.italic = False
        
    def show_request(self):
        self.request.text = self.item['request']['product_category']
        self.request_notes.text = self.item['request']['notes']
       
    def show_runner(self):
        runner = self.item['approved_runner']['display_name']
        self.runner.text = "Runner: " + runner
            
    def show_status(self):
        status = self.item['status_dict']
        colour = pale_blue
        if not status['pickup_agreed'] or not status['dropoff_agreed']:
            colour = yellow
        if status['delivery']:
            colour = light_green
        elif self.item['offer']['expiry_date'] <= datetime.datetime.today():
            colour = pink
        self.column_panel_1.background = colour
            
    def show_myself(self, **event_args):
        """Colour codes display to highlight user's own data"""
        if self.item['offer']['user'] == self.user:
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
        if self.item['approved_runner'] == self.user:
            self.runner.foreground = dark_green
            self.show_route.foreground = dark_green
            self.status_message.foreground = dark_green
        else:
            self.show_route.foreground = black
   
    def populate_addresses(self):
        """ Fills in address details for Pickup and Dropoff, adding postcode if authorised"""
        for address, table in {self.pickup: 'offer', self.dropoff: 'request'}.items():
            address.text = self.item[table]['user']['display_name']+"\n"
            if self.item['approved_runner'] == self.user or self.item[table]['user'] == self.user:
                address.text += str(self.item[table]['user']['house_number'])+" "
            address.text += self.item[table]['user']['street']+", "
            address.text += self.item[table]['user']['town']+", "
            address.text += self.item[table]['user']['county']+"\n"
            address.text += self.item[table]['user']['postcode'] if self.item[table]['user'] == self.user else ""
            shared =  self.item[table]['user']['postcode_shared_with']
            if shared != None:
                address.text += self.item[table]['user']['postcode'] if self.user in shared else ""
          
    def show_deliveries_row(self, **event_args):
        """This method is called when the DeliveriesRow is shown on the screen"""
        self.show_myself()
        self.show_offer()
        self.show_request()
        self.show_runner()
        self.show_status()
        self.populate_addresses()
        self.show_feedback_buttons()
        self.row_id.text = self.item.get_id()
        self.status_message.text = anvil.server.call("get_status_message", self.item)
                          
    def click_show_message(self, **event_args):
        """This method is called when a Message Button is shown on the screen"""
        sender = event_args['sender']
        self.textbox.visible = True if sender.icon == 'fa:caret-down'else False
        self.chat_input.visible = True if sender.icon == 'fa:caret-down' else False
        sender.icon = 'fa:caret-up' if self.textbox.visible else 'fa:caret-down'
        if sender.icon == 'fa:caret-up':
            self.textbox.text = anvil.server.call('get_chat_text', self.row_id.text)
            self.refresh_data_bindings()

    def enter_chat_input(self, **event_args):
        """This method is called when a user press ENTER in chat"""
        self.textbox.text = anvil.server.call('get_chat_text', self.row_id.text) or self.textbox.text
        message = f"\n({self.user['display_name']} at "
        message += datetime.datetime.now().strftime("%d %b %Y on %H:%M)\n\n")        
        message = "> " + self.chat_input.text + message
        self.chat_input.text = ""        
        self.textbox.text = message  + self.textbox.text
        anvil.server.call('save_to_chat', self.row_id.text, self.textbox.text)        
        
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
        
    def show_feedback_buttons(self):
        """Checks status_dict and reveals feedback buttons as appropriate"""
        if self.user == self.item['offer']['user'] and self.user != self.item['approved_runner']:
            options = [self.feedback_on_runner]
            self.user_role = "Offerer"
        if self.user == self.item['request']['user']:
            options = [self.feedback_on_runner, self.feedback_on_offerer]
            self.user_role = "Requester"
            if self.user == self.item['approved_runner']:
                options.remove(self.feedback_on_runner)
                self.user_role = "Runner"
        if self.user == self.item['approved_runner']:
            self.user_role = "Runner"
            options = [self.feedback_on_offerer, self.feedback_on_requester]
            if self.user == self.item['offer']['user']:
                options.remove(self.feedback_on_offerer)
            if self.user == self.item['request']['user']:
                options.remove(self.feedback_on_requester)        
        for option in options:
            option.visible = True
            option.enabled =  not self.check_for_previous_feedback(option)                
                
    def check_for_previous_feedback(self, option):
        """ Returns True if exisiting feedback foun"""
        karma_forms = anvil.server.call("get_karma_forms_from_user", self.item) # self.item = match?
        regarding = {self.feedback_on_runner: self.item['approved_runner'],
                     self.feedback_on_offerer: self.item['offer']['user'],
                     self.feedback_on_requester: self.item['request']['user'],}
        for form in karma_forms:
            if form['regarding_user'] == regarding[option]:
                print("Found existing feedback regarding", form['regarding_user']['display_name'])
                return True
            
    def click_feedback_button(self, **event_args):
        """Check for tick in one of the Feedback buttons and launch KarmaForm"""
        self.sender = event_args.get('sender')
        if self.sender == self.feedback_on_runner:
            regarding_role = "Runner"               
            regarding = self.item['approved_runner']
        if self.sender == self.feedback_on_requester:
            regarding = "Requester"
            regarding = self.item['request']['user']
        if self.sender == self.feedback_on_offerer:
            regarding_role = "Offerer"
            regarding = self.item['offer']['user']
        row_id = self.item.get_id()
        form = KarmaForm(row_id, regarding, regarding_role, self.user_role)
        self.status_view_panel.add_component(form)
        self.status_view_panel.visible = True
        form.visible = True








