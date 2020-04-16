from ._anvil_designer import StatusViewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....Globals import green, grey, red, black, dark_green, dark_blue,blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

class StatusView(StatusViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.match = anvil.server.call('_get_all_matches')[0] # Test data
        self.user = anvil.users.get_user()
        self.is_offerer.checked = self.user == self.match['offer']['user']
        self.is_runner.checked = self.user == self.match['approved_runner']
        self.is_requester.checked = self.user == self.match['request']['user']
        self.all_checkboxes = [x for x in self.card_1.get_components() if type(x) == CheckBox]
        self.initial_canvas() 
        self.refresh_canvas()

    def initial_canvas(self):
        self.offer_matched.checked = True
        if self.match['approved_runner']:
            self.runner_selected.checked = True
        for component in self.card_1.get_components():
            component.background = bright_blue
            component.foreground = white
            component.enabled = False
            component.bold = True
            component.spacing_above = 'none'
            component.spacing_below = 'none'
        self.card_1.background = light_blue
        self.complete.background = red
        self.offerer.background = dark_blue
        self.runner.background = dark_blue
        self.requester.background = dark_blue
        self.offerer.text = "Offerer: " + self.match['offer']['user']['display_name']
        self.runner.text = "Runner: " + self.match['approved_runner']['display_name']
        self.requester.text = "Requester: " + self.match['request']['user']['display_name']
        components = set()
        if self.is_runner.checked:
            components.update({self.runner_confirms_pickup, self.runner_confirms_dropoff, self.dropoff_agreed, self.pickup_agreed})
        if self.is_offerer.checked:
            components.update({self.offerer_confirms_pickup, self.pickup_agreed})
        if self.is_requester.checked:
            components.update({self.requester_confirms_dropoff, self.dropoff_agreed})
        for component in components:
            component.enabled = True
        for checkbox in self.all_checkboxes:
            checkbox.set_event_handler("change", self.refresh_canvas)
        
    def refresh_canvas(self, **event_args):
        self.update_arrows()
        self.update_text_colour()

    def update_arrows(self):
        rules = [(self.offer_matched, self.arrow1),
                 (self.runner_selected, self.arrow2),
                 (self.pickup_agreed, self.arrow3),
                 (self.dropoff_agreed, [self.arrow4, self.arrow5]),
                ]
        for component, arrows in rules:
            if type(arrows) != list:
                arrows = [arrows]
            for arrow in arrows:
                arrow.foreground = black if component.checked else light_blue
            
    def update_text_colour(self):
        for checkbox in self.all_checkboxes:
            checkbox.foreground = black if checkbox.checked else light_blue
        





              

