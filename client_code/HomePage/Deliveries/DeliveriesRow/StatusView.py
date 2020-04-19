from ._anvil_designer import StatusViewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....Globals import green, grey, red, black, dark_green, dark_blue,blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink
from .KarmaForm import KarmaForm

class StatusView(StatusViewTemplate):
    def __init__(self, match, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.user = anvil.users.get_user()
        self.test_mode = False
        self.all_checkboxes = [x for x in self.card_1.get_components() if type(x) == CheckBox]
        self.all_arrows = [x for x in [x for x in self.card_1.get_components() if type(x) == Label] if x.icon == 'fa:arrow-down']
        self.feedback = [self.feedback_RUN_on_REQ,
        self.feedback_REQ_on_RUN,
        self.feedback_RUN_on_OFF,
        self.feedback_OFF_on_RUN,]
        self.initial_canvas()
        self.match = match
        self.ingest_match_data()
        self.define_options_by_role()        
        self.show_form()
        for checkbox in self.all_checkboxes:
            checkbox.set_event_handler("change", self.update_components)    


    def show_form(self, **event_args):
        print("show_form")
        self.display_options_by_role()
        self.update_components()
        
    def initial_canvas(self):
        """
        How the form layout (canvas) should look when first loaded e.g.
        colours, font size, labels, enabled and visible defaults
        """
        # Colours, Bold, Spacing, Enabled, Label Text
        for component in self.card_1.get_components():
            component.background = bright_blue
            component.foreground = white
            component.bold = False
            component.italic = True
            component.spacing_above = 'none'
            component.spacing_below = 'none'
            component.enabled = False
        for component in (self.confirm, self.cancel, self.toggle_view):
            component.enabled = True
            component.spacing_above = "medium"
            component.italic = False
        self.cancel.background = red
        self.confirm.background = green
        self.toggle_view.background = bright_blue
        self.card_1.background = bright_blue
        self.card_2.background = light_blue
        for component in [self.offerer, self.runner, self.requester]:
            component.background = bright_blue
            component.italic = False
            component.bold = True
        # Event Handling
        for checkbox in self.all_checkboxes:
            self.conceal(checkbox, True) 

    def ingest_match_data(self):
        """Update labels, checkboxes, and colours based on self.match data"""
        self.status_dict = self.match['status_dict'] or {"offer_matched": True,
                                                         "runner_selected": True}
        self.offerer.text = "Offerer: " + self.match['offer']['user']['display_name']
        self.runner.text = "Runner: " + self.match['approved_runner']['display_name']
        self.requester.text = "Requester: " + self.match['request']['user']['display_name']
        self.is_offerer.checked = self.user == self.match['offer']['user']
        self.is_runner.checked = self.user == self.match['approved_runner']
        self.is_requester.checked = self.user == self.match['request']['user']        
        # BUG For some reason 'sender' is detected as a CheckBox...    
        for checkbox, checked in self.status_dict.items():
            object = getattr(self, checkbox)
            setattr(object, "checked", checked)
        # TODO: Make general purpose/DRY method combined with lock_history()        
        
    def define_options_by_role(self):
        """Attributes set with list of visible options, determined by role"""
        self.offerer_options = [self.pickup_agreed,
                                self.offerer_confirms_pickup,
                                self.feedback_OFF_on_RUN,
                                self.delivery]
        self.runner_options = [self.pickup_agreed,
                               self.runner_confirms_pickup,
                               self.feedback_RUN_on_OFF,
                               self.dropoff_agreed,
                               self.runner_confirms_dropoff,
                               self.feedback_RUN_on_REQ,
                               self.delivery]
        self.requester_options = [self.dropoff_agreed,
                                  self.requester_confirms_dropoff,
                                  self.feedback_REQ_on_RUN,
                                  self.delivery]
        self.offererrunner_options = [self.dropoff_agreed,
                                      self.runner_confirms_dropoff,
                                      self.feedback_RUN_on_REQ,
                                      self.delivery]
        self.requesterrunner_options = [self.pickup_agreed,
                                        self.runner_confirms_pickup,
                                        self.feedback_RUN_on_OFF,
                                        self.delivery]
        
    def display_options_by_role(self, **event_args):
        # Single Roles: Offerer
        if self.is_offerer.checked and not self.is_runner.checked:
            self.checkboxes = self.offerer_options
        # Single Roles: Runner
        if self.is_runner.checked and not self.is_offerer.checked and not self.is_requester.checked:
            self.checkboxes = self.runner_options
        # Single Roles: Requester
        if self.is_requester.checked and (not self.is_runner.checked):
            self.checkboxes = self.requester_options
        # Dual Roles: Offerer=Runner
        if self.is_offerer.checked and self.is_runner.checked:
            self.checkboxes = self.offererrunner_options
        # Dual Roles: Requester=Runner  
        if self.is_requester.checked and self.is_runner.checked:
            self.checkboxes = self.requesterrunner_options            
        for checkbox in self.checkboxes:
            self.conceal(checkbox, False) # False means 'reveal'
            checkbox.enabled = True if not checkbox.checked else False
            checkbox.italic = False
            checkbox.bold = True
            checkbox.foreground = white
        self.delivery.enabled = True if self.is_requester.checked else False           
            
    def conceal(self, component, boolean_value):
        """
        Custom appearance/actions for toggling .visible.  During testing,
        can be helpful to colour code rather than make truly invisible.
        boolean_value = False means 'reveal' instead of 'conceal' and
        simply reverses values.
        """
        if self.test_mode:
            component.background = red if boolean_value else bright_blue
        else:
            component.visible = not boolean_value

    def update_components(self, **event_args):
        self.sender = event_args.get('sender')
        print("Updating components.\nSender:", self.sender)
        self.check_for_feedback()
        self.update_dependencies()
        self.update_predecessors()
        self.update_forwards()
        self.update_arrows()
        self.update_text_colour()
        self.lock_history()
    
    def check_for_feedback(self, **event_args):
        """Check for tick in one of the Feedback checkboxes and launch KarmaForm"""
        """self.feedback = [self.feedback_RUN_on_REQ,
            self.feedback_REQ_on_RUN,
            self.feedback_RUN_on_OFF,
            self.feedback_OFF_on_RUN,]"""
        if self.sender:
            self.visible = False
            form = KarmaForm()
            if self.sender == self.feedback_REQ_on_RUN:
                user_role = "Requester"
                regarding_role = "Runner"
                regarding = self.match['approved_runner']['display_name']
            if self.sender == self.feedback_OFF_on_RUN:
                user_role = "Offerer"
                regarding_role = "Runner"
                regarding = self.match['approved_runner']['display_name']
            if self.sender == self.feedback_RUN_on_REQ:
                user_role = "Runner"
                regarding_role = "Requester"
                regarding = self.match['request']['user']['display_name']
            if self.sender == self.feedback_RUN_on_OFF:
                user_role = "Runner"
                regarding_role = "Offerer"
                regarding = self.match['offer']['user']['display_name']
            form.regarding.text = regarding
            form.regarding_role.text = regarding_role
            form.user.text = self.user['display_name']
            form.user_role.text = user_role
            self.parent.add_component(form)                          
    
    def update_dependencies(self):
        """
        These are 1...1 dependencies.  Multiple predecessors
        i.e. 'backfill' are handled by update_predecessors
        """
        rules = [(self.offerer_confirms_pickup, self.feedback_OFF_on_RUN),
                 (self.runner_confirms_pickup, self.feedback_RUN_on_OFF),
                 (self.runner_confirms_dropoff, self.feedback_RUN_on_REQ),
                 (self.requester_confirms_dropoff, self.feedback_REQ_on_RUN),]
        for enabler, target in rules:
            target.enabled = True if enabler.checked else False
            if not enabler.checked:
                target.checked = False
                
    def update_predecessors(self):
        """
        Allows user to select later values and auto-complete/backfill earlier ones.
        """
        # TODO use dictionary/old dictionary to revert state otherwise back will remain checked
        backfill = False
        for checkbox in self.checkboxes[::-1]:
            if not checkbox.checked and not backfill:
                continue
            if checkbox.checked and not backfill:
                backfill = True # Backfill for remaining iterations
            if not checkbox.checked and backfill and checkbox not in self.feedback:
                checkbox.checked = True
        # Additional "backfill" for Delivery Complete
        if self.delivery.checked:
            for option in [self.pickup_agreed,
                           self.runner_confirms_pickup,
                           self.offerer_confirms_pickup,
                           self.dropoff_agreed,
                           self.runner_confirms_dropoff,
                           self.requester_confirms_dropoff,]:
                option.checked = True
                
    def update_forwards(self):
        # Additional "forward-fill" Requester+Runner
        if self.is_requester.checked and self.is_runner.checked and self.runner_confirms_pickup.checked:
            for option in [self.dropoff_agreed,
                           self.runner_confirms_dropoff,
                           self.requester_confirms_dropoff,
                           self.feedback_RUN_on_REQ,
                           self.feedback_REQ_on_RUN,]:
                option.checked = True
        # Additional "forward-fill" Offerer+Runner
        if self.is_offerer.checked and self.is_runner.checked:
            for option in [self.pickup_agreed,
                           self.runner_confirms_pickup,
                           self.offerer_confirms_pickup,
                           self.feedback_RUN_on_OFF,
                           self.feedback_OFF_on_RUN,]:
                option.checked = True
        # Additional "forward-fill" Requester Confirms Dropoff
        if self.is_requester and self.requester_confirms_dropoff.checked:
            self.delivery.checked = True

                
    def update_arrows(self):
        rules = [(self.offer_matched, self.arrow1),
                 (self.runner_selected, self.arrow2),
                 (self.pickup_agreed, self.arrow3),
                 (self.dropoff_agreed, [self.arrow4, self.arrow5]),
                 (self.delivery, self.arrow6)
                ]
        for component, arrows in rules:
            if type(arrows) != list:
                arrows = [arrows]
            for arrow in arrows:
                arrow.foreground = black if component.checked else white
            
    def update_text_colour(self):
        for checkbox in self.all_checkboxes:
            if checkbox.checked:
                checkbox.foreground = black 
            else:
                checkbox.foreground = white if checkbox.enabled else light_blue
                
    def lock_history(self):
        """Disable all checkboxes already saved as checked to the database"""
        for checkbox, checked in self.status_dict.items():
            object = getattr(self, checkbox)
            if getattr(object, "checked"):
                setattr(object, "enabled", False)

    def save_status(self):
        """Saves checkbox status to status_dict and back to Match database"""
        checkbox_names = [x for x in dir(self) if type(getattr(self,x)) == CheckBox]
        for checkbox_name in checkbox_names:
            checkbox_object = getattr(self, checkbox_name)
            self.status_dict[checkbox_name] = getattr(checkbox_object, "checked")
        # Remove false identities to avoid multi-user problems!
        removals = "sender is_offerer is_runner is_requester".split()
        for removal in removals:
            if removal in self.status_dict:
                del self.status_dict[removal]  
        anvil.server.call("save_matches_status_dict", self.match, self.status_dict)
        pass
     
    def click_confirm(self, **event_args):
        """This method is called when the Confirm button is clicked"""
        self.save_status()
        self.click_cancel()
      
    def click_cancel(self, **event_args):
        """This method is called when the Cancel button is clicked"""
        self.parent.parent.parent.show_status()
        self.parent.parent.parent.show_deliveries_row()
        self.parent.parent.parent.disable_similar_buttons(enabled = False)
        self.remove_from_parent()
#         self.parent.parent.parent.status_view.raise_event('click')        
        self.clear()        

    def click_toggle_view(self, **event_args):
        """This method is called when the Toggle View button is clicked"""
        sender = event_args['sender']
        if sender.icon == 'fa:search-plus':
            sender.icon = 'fa:search-minus'
            sender.text = "  My View"
            sender.background = blue
            for component in self.card_1.get_components():
                print(type(component))
                component.visible = True

        else: 
            sender.icon = 'fa:search-plus'
            sender.text = "  Full View"
            sender.background = bright_blue
            self.initial_canvas() 
            self.show_form()

              
              
          

