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
        self.user = anvil.users.get_user()
        self.test_mode = True
        self.all_checkboxes = [x for x in self.card_1.get_components() if type(x) == CheckBox]
        self.all_arrows = [x for x in [x for x in self.card_1.get_components() if type(x) == Label] if x.icon == 'fa:arrow-down']
        if not hasattr(self, 'match'):
            return

    def show_form(self, **event_args):
        print("show_form")
        self.initial_canvas()
        self.import_match_data()
        self.setup_test_or_prod()
        self.imported_data()
        self.initial_options_by_role()
        self.refresh_canvas()
        
    def setup_test_or_prod(self, **event_args):
          for checkbox in (self.is_offerer, self.is_requester, self.is_runner):
              checkbox.enabled = self.test_mode
              checkbox.visible = self.test_mode
              checkbox.set_event_handler('change', show_form)
          if not self.test_mode:
              self.is_offerer.checked = self.user == self.match['offer']['user']
              self.is_runner.checked = self.user == self.match['approved_runner']
              self.is_requester.checked = self.user == self.match['request']['user']

    def imported_match_data(self):
        # Checkboxes
        self.offer_matched.checked = True if self.match else False
        if self.match['approved_runner']:
            self.runner_selected.checked = True

        self.offerer.text = "Offerer: " + self.match['offer']['user']['display_name']
        self.offerer.background = blue
        self.runner.text = "Runner: " + self.match['approved_runner']['display_name']
        self.runner.background = blue
        self.requester.text = "Requester: " + self.match['request']['user']['display_name']
        
    def initial_canvas(self):
        """
        How the form layout (canvas) should look when first loaded e.g.
        colours, font size, labels, enabled and visible defaults
        """
        # Colours, Bold, Spacing, Enabled, Label Text
        for component in self.card_1.get_components():
            component.background = bright_blue
            component.foreground = white
            component.enabled = False
            component.bold = True
            component.spacing_above = 'none'
            component.spacing_below = 'none'
        self.card_1.background = bright_blue
        self.card_2.background = light_blue
        self.offerer.background = dark_blue
        self.runner.background = dark_blue
        self.requester.background = dark_blue
        self.requester.background = blue

        
    def initial_options_by_role(self, **event_args):
        # Stickiness and Event Handling
        for checkbox in self.all_checkboxes:
            checkbox.set_event_handler("change", self.refresh_canvas)
            checkbox.sticky = True
            checkbox.visible = False
        # Single Roles: Offerer
        for checkbox in {self.pickup_agreed,
                         self.offerer_confirms_pickup,
                         self.runner_feedback_by_offerer,
                         self.delivery}:
            self.conceal(checkbox, not self.is_offerer.checked)
        # Single Roles: Runner
        for checkbox in {self.pickup_agreed,
                         self.runner_confirms_pickup,
                         self.offerer_feedback_by_runner,
                         self.dropoff_agreed,
                         self.runner_confirms_dropoff,
                         self.requester_feedback_by_runner,
                         self.delivery}:
            print(type(checkbox), not self.is_runner.checked)
            self.conceal(checkbox, self.is_runner.checked)
        # Single Roles: Requester
        for checkbox in {self.dropoff_agreed,
                         self.requester_confirms_dropoff,
                         self.runner_feedback_by_requester,
                         self.delivery}:
            self.conceal(checkbox, not self.is_requester.checked)
#         # Dual Roles: Offerer=Runner       
#         visible = red if self.is_offerer.checked and self.is_runner.checked else bright_blue
#         for checkbox in self.all_checkboxes[2:7]:
#             checkbox.background = visible
#         for arrow in self.all_arrows:
#             arrow.background = visible
#             self.arrow1.background = not visible
#             self.arrow2.background = not visible
#         # Dual Roles: Requester=Runner    
#         visible = red if self.is_runner.checked and self.is_requester.checked else bright_blue
#         for checkbox in self.all_checkboxes[7:12]:
#             checkbox.background = visible
#         for arrow in self.all_arrows[-3:-1]:
#             arrow.background = visible
        
    def refresh_canvas(self, **event_args):
        self.sender = event_args.get('sender')
        self.update_arrows()
#         self.update_text_colour()
        self.update_sticky_items()
        self.update_enablers()
        self.update_predecessors()
        
    def update_for_dual_statuses(self):
        if self.runner_confirms_pickup.checked and self.offerer_confirms_pickup.checked:
            self.pickup_agreed.checked = True
        self.update_text_colour()
        self.update_sticky_items()
        self.update_enablers()    
          
    def update_predecessors(self):
        rules = [(self.runner_confirms_dropoff, self.runner_confirms_pickup),
                 ]
        for component, predecessor in rules:
            if component.checked and not predecessor.checked:
                predecessor.checked = True
        self.update_text_colour()
        self.update_sticky_items()
        self.update_enablers()                  
        
    def update_enablers(self):
        rules = [(self.offerer_confirms_pickup, self.runner_feedback_by_offerer),
                 (self.runner_confirms_pickup, self.offerer_feedback_by_runner),
                 (self.requester_confirms_dropoff, self.runner_feedback_by_requester),
                 (self.runner_confirms_dropoff, self.requester_feedback_by_runner)]
        for enabler, target in rules:
            if enabler.checked:
                target.enabled = True
        self.update_sticky_items()
        
    def update_sticky_items(self):
        for checkbox in self.all_checkboxes:
            if checkbox.sticky and checkbox.checked:
                checkbox.enabled = False

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
                arrow.foreground = black if component.checked else white
            
    def update_text_colour(self):
        for checkbox in self.all_checkboxes:
            checkbox.foreground = black if checkbox.checked else light_blue
            
    def conceal(self, component, boolean_value):
        """
        Custom appearance/actions for toggling .visible.  During testing,
        can be helpful to colour code rather than make truly invisible
        """
        print("conceal")
        if self.test_mode:
            component.background = red if boolean_value else bright_blue
        else:
            component.visible = not boolean_value
        





              

