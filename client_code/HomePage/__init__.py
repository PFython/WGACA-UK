from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .MyOffers import MyOffers
from .UserProfile import UserProfile
from .MyRequests import MyRequests
from .Matches import Matches
from .Deliveries import Deliveries
from .UserSetup import UserSetup
from .TermsOfUse import TermsOfUse

class HomePage(HomePageTemplate):
    def __init__(self, **properties):
        anvil.users.login_with_form(allow_remembered=False)
        # Set Form properties and Data Bindings.
        self.fcolour = '#0080c0' # Foreground colour and active menu button background
        self.bcolour = '#cae4ff' # Background colour
        self.xcolour = '#eaf4ff' # Deselected text box
        self.ycolour = '#00a3f0' # Inactive menu button background
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
#         self.enable_menu_buttons(False)
        # 2nd step of registration process to force completion of required contact data        
        self.force_user_setup()
    
    def check_required_fields(self):
        """
        Very cursory checks that all fields are completed
        TODO: Validate by data type and permitted values
        """
        checks = [anvil.users.get_user()['house_number']]
        checks += [anvil.users.get_user()['street']]
        checks += [anvil.users.get_user()['town']]
        checks += [anvil.users.get_user()['county']]
        checks += [anvil.users.get_user()['postcode']]
        checks += [anvil.users.get_user()['display_name']]
        checks += [anvil.users.get_user()['telephone']]
        return all(checks)
    
    def force_user_setup(self):
        # Test convenience - resets Will Gaca each time...
        if anvil.users.get_user()['display_name'] == "Will Gaca":
            anvil.server.call('details_complete', False)
            anvil.server.call('terms_accepted', False)
        while not anvil.users.get_user()['terms_accepted']:
            alert(content=TermsOfUse(), title = "Please read and accept the following Privacy Statement & Terms of Use:", large=True,)
        while not anvil.users.get_user()['details_complete']:
            alert(content=UserSetup(), title = "Please confirm your personal details:", large=True,)
            if self.check_required_fields():
                anvil.server.call("details_complete", True)
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)
#         self.enable_menu_buttons(True)
#             self.column_panel_1.add_component(UserSetup())
#             self.highlight_selected_menu(self.menu_my_data)

#     def enable_menu_buttons(self, boolean_value):
#         """ Enables / disables all menu buttons"""
#         self.menu_my_offers.enabled = boolean_value
#         self.menu_my_requests.enabled = boolean_value
#         self.menu_my_matches.enabled = boolean_value
#         self.menu_my_deliveries.enabled = boolean_value
#         self.menu_my_data.enabled = boolean_value     
            
    def highlight_selected_menu(self, selected):        
        self.menu_my_offers.background = self.fcolour
        self.menu_my_requests.background = self.fcolour
        self.menu_my_matches.background = self.fcolour
        self.menu_my_deliveries.background = self.fcolour
        self.menu_my_data.background = self.fcolour
        self.menu_my_offers.foreground = self.bcolour
        self.menu_my_requests.foreground = self.bcolour
        self.menu_my_matches.foreground = self.bcolour
        self.menu_my_deliveries.foreground = self.bcolour
        self.menu_my_data.foreground = self.bcolour
        self.menu_my_offers.bold = False
        self.menu_my_requests.bold = False
        self.menu_my_matches.bold = False
        self.menu_my_deliveries.bold = False
        self.menu_my_data.bold = False
        self.menu_my_offers.font_size = 12
        self.menu_my_requests.font_size = 12
        self.menu_my_matches.font_size = 12
        self.menu_my_deliveries.font_size = 12
        self.menu_my_data.font_size = 12
        selected.background = self.ycolour
        selected.foreground = "#ffffff"
        selected.bold = True
        selected.font_size = 12
        # Hide all images
        images = {self.menu_my_offers: self.image_1,
                  self.menu_my_requests: self.image_2,
                  self.menu_my_matches: self.image_3,
                  self.menu_my_deliveries: self.image_4,
                  self.menu_my_data: self.image_5}        
        for image in images.values():
            setattr(image, "visible", False)
        # Unhide selected image
        setattr(images[selected], "visible", True)
        
    def menu_my_offers_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)
        
    def menu_my_requests_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(MyRequests())
        self.highlight_selected_menu(self.menu_my_requests)
    
    def menu_my_matches_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(Matches())
        self.highlight_selected_menu(self.menu_my_matches)
        
    def menu_my_deliveries_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(Deliveries())
        self.highlight_selected_menu(self.menu_my_deliveries)        
        
    def menu_my_data_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(UserProfile())
        self.highlight_selected_menu(self.menu_my_data)







