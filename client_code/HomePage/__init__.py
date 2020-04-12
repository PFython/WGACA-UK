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
from .AboutThisApp import AboutThisApp

green = '#5eb348'
grey = '#d8d8d8'
red = '#ff8080'
blue = '#0080c0'
light_blue = '#cae4ff'
pale_blue = '#eaf4ff'
bright_blue = '00a3f0'
white = "#ffffff"
colours = (green, grey, red, blue, light_blue, pale_blue, bright_blue, white)
menu_font_size = 17

class HomePage(HomePageTemplate):
    def __init__(self, **properties):
         # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.background = bright_blue
        self.navigation_bar.background = blue
        self.title_bar.background = light_blue
#         self.card_1.background = light_blue
        for button, tag in {self.menu_about: 'About',
                            self.menu_my_offers: 'My Offers',
                            self.menu_my_requests: 'My Requests',
                            self.menu_my_matches: 'My Matches',
                            self.menu_my_deliveries: 'My Deliveries',
                            self.menu_my_details: 'My Details'}.items():
            button.tag = tag
        self.column_panel_1.add_component(AboutThisApp())
        self.highlight_selected_menu(self.menu_about)
        self.check_permissions()
        
    def check_permissions(self):
        # 1st step of registration process requires email and password
        anvil.users.login_with_form(allow_remembered=True)
        # 2nd step of registration process requires contact data and read/accept Terms of Use
        self.force_user_setup()
    
    def required_fields_are_populated(self):
        """ Checks that all required fields are completed """
        user = anvil.users.get_user()
        checks = [user['house_number']]
        checks += [user['street']]
        checks += [user['town']]
        checks += [user['county']]
        checks += [user['display_name']]
#         checks += [user['postcode']]        
#         checks += [user['telephone']]
        return all(checks)
    
    def force_user_setup(self):
        """ Blocks until i) Terms of Use accepted; ii) Required contact data supplied """
        while not anvil.users.get_user()['terms_accepted']:
            alert(content=TermsOfUse(), title = "Please read and accept the following Privacy Statement & Terms of Use:", large=True,)
        while not self.required_fields_are_populated():
            alert(content=UserSetup(), title = "Please confirm your personal details:", large=True,)
#         self.column_panel_1.add_component(MyOffers())
#         self.highlight_selected_menu(self.menu_my_offers)
            
    def highlight_selected_menu(self, selected):
        """ Visual confirmation of currently selected Menu item """
        self.title_bar.text = selected.tag
        self.menu_my_offers.background = blue
        self.menu_my_requests.background = blue
        self.menu_my_matches.background = blue
        self.menu_my_deliveries.background = blue
        self.menu_my_details.background = blue
        self.menu_my_offers.foreground = light_blue
        self.menu_my_requests.foreground = light_blue
        self.menu_my_matches.foreground = light_blue
        self.menu_my_deliveries.foreground = light_blue
        self.menu_my_details.foreground = light_blue
        self.menu_my_offers.bold = False
        self.menu_my_requests.bold = False
        self.menu_my_matches.bold = False
        self.menu_my_deliveries.bold = False
        self.menu_my_details.bold = False
        self.menu_my_offers.font_size = menu_font_size
        self.menu_my_requests.font_size = menu_font_size
        self.menu_my_matches.font_size = menu_font_size
        self.menu_my_deliveries.font_size = menu_font_size
        self.menu_my_details.font_size = menu_font_size
        selected.background = bright_blue
        selected.foreground = white
        selected.bold = True
        selected.font_size = menu_font_size
        # Hide all images
        images = {self.menu_about: self.image_0,
                  self.menu_my_offers: self.image_1,
                  self.menu_my_requests: self.image_2,
                  self.menu_my_matches: self.image_3,
                  self.menu_my_deliveries: self.image_4,
                  self.menu_my_details: self.image_5}        
        for image in images.values():
            setattr(image, "visible", False)
        # Unhide selected image
        setattr(images[selected], "visible", True)
        
    def menu_my_offers_click(self, **event_args):
        """This method is called when the Offers menu item is clicked"""
        self.check_permissions()
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)
        
    def menu_my_requests_click(self, **event_args):
        """This method is called when the Requests menu item is clicked"""
        self.check_permissions()
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(MyRequests())
        self.highlight_selected_menu(self.menu_my_requests)
    
    def menu_my_matches_click(self, **event_args):
        """This method is called when the Matches menu item is clicked"""
        self.check_permissions()
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(Matches())
        self.highlight_selected_menu(self.menu_my_matches)
        
    def menu_my_deliveries_click(self, **event_args):
        """This method is called when the Deliveries menu item is clicked"""
        self.check_permissions()
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(Deliveries())
        self.highlight_selected_menu(self.menu_my_deliveries)        
        
    def menu_my_details_click(self, **event_args):
        """This method is called when the Data menu item is clicked"""
        self.check_permissions()
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(UserProfile())
        self.highlight_selected_menu(self.menu_my_details)

    def menu_about_click(self, **event_args):
        """This method is called when the About button is clicked"""
        self.check_permissions()
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(AboutThisApp())
        self.highlight_selected_menu(self.menu_about)









