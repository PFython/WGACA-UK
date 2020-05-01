from ._anvil_designer import MatchesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ConfirmMatch import ConfirmMatch, green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink
import datetime

from ....Globals import CHAT_BLURB

class MatchesRow(MatchesRowTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.user = anvil.users.get_user()
      # Any code you write here will run when the form opens.
      self.show_route.url = self.item['route_url']
      self.show_route.foreground = green
      self.volunteers.bold = True
      self.dropoff.text = self.item['request']['user']['address']
      self.pickup.text = self.item['offer']['user']['address']
      self.offer_notes.text = self.item['offer']['notes']
      expiry = self.item['offer']['expiry_date']
      self.offer_expiry.text = expiry.strftime('%d %b %Y')
      if expiry <= datetime.datetime.today():
            self.offer_expiry.foreground = red
      self.offer.text = self.item['offer']['product_key']+" … "+str(self.item['offer']['units'])
      self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
      self.request.text = self.item['request']['product_category']
      self.request_notes.text = self.item['request']['notes']
    
    def volunteer_toggle_status(self, **event_args):
        """This method is called when the Volunteer Toggle CheckBox is shown on the screen"""
        if self.user in self.item['available_runners']:
            event_args['sender'].checked = True
            event_args['sender'].text = "You volunteered.\nUntick to cancel."
        else:
            event_args['sender'].checked = False
            event_args['sender'].text = "Tick to volunteer"

    def volunteer_toggle_change(self, **event_args):
        """This method is called when this Volunteer Toggle checkbox is checked or unchecked"""
        if event_args['sender'].checked:
            anvil.server.call("volunteer_as_runner", self.item, True)
        else:
            anvil.server.call("volunteer_as_runner", self.item, False)
        self.volunteer_toggle_status(**event_args)        
        self.set_volunteer_colour()

    def set_volunteer_colour(self):
        self.volunteers.text = str(len(self.item['available_runners']))+" volunteer(s)."
        self.volunteers.foreground = red if self.volunteers.text.startswith("0 ") else green
        self.volunteers.icon = "fa:heart o"if self.volunteers.text.startswith("0 ") else "fa:heart"      

    def show_myself(self, **event_args):
        """This method is called when the data row panel is shown on the screen"""
        self.set_volunteer_colour()
        user = anvil.users.get_user()

        if self.item['request']['user'] == user:
            self.show_route.foreground = green
            self.label_1.text  = "My Request"
            self.label_1.foreground = green
            self.label_4.foreground = green
            self.dropoff.foreground = green
            self.dropoff.icon = 'fa:home'
            self.request.foreground = green
            self.request_notes.foreground = green        

        if self.item['offer']['user'] == user:
            self.show_route.foreground = green
            self.label_1.text = f"Request by: {self.item['request']['user']['display_name']}"
            self.label_2.text  = "My Offer"
            self.label_2.foreground = green
            self.label_3.foreground = green        
            self.pickup.foreground = green
            self.pickup.icon = 'fa:home'
            self.offer.foreground = green
            self.offer_notes.foreground = green
            self.confirm_match.visible = True
            self.volunteer_toggle.visible = False

    def confirm_match_click(self, **event_args):
        """This method is called when the Select Volunteer button is clicked"""
        self.confirm_match.visible = False
        requester = self.item['request']['user']
        runners = [f"{self.user['display_name']} (myself)"] + [x['display_name'] for x in self.item['available_runners']]
        row_id = self.item.get_id()
        new_form = ConfirmMatch(requester, runners, row_id, CHAT_BLURB)
        self.flow_panel_1.add_component(new_form, column=None)
        self.flow_panel_1.visible = True
        user = anvil.users.get_user()






