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
from ._DeveloperTools import _DeveloperTools
from .ContactUs import ContactUs
from .News import News
from .TitleButton import TitleButton

from ..Globals import LOCALE, green, grey, red, blue, light_blue, pale_blue, bright_blue, white, red, yellow, pink

menu_font_size = 16

class HomePage(HomePageTemplate):
    def __init__(self, **properties):
         # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.background = bright_blue
        self.navigation_bar.background = blue
        for button, tag in {self.menu_about: 'About',
                            self.menu_contact_us: 'Contact Us',
                            self.menu_my_offers: 'My Offers',
                            self.menu_my_requests: 'My Requests',
                            self.menu_my_matches: 'My Matches',
                            self.menu_my_deliveries: 'My Deliveries',
                            self.menu_my_details: 'My Details'}.items():
            button.tag = tag
        self.column_panel_1.add_component(TitleButton(self.menu_about.tag, self.menu_about.background))
        self.column_panel_1.add_component(AboutThisApp())
        self.highlight_selected_menu(self.menu_about)
        version = anvil.server.get_app_origin()
        if "test" in version:
            self.test_version.visible = True
            self.test_version.text = version

        
    def check_for_boss(self):
#         if anvil.users.get_user():
        if anvil.users.get_user()['admin']:
              print("Good day to you, Boss...")
              self.navigation_bar.add_component(_DeveloperTools())
        
    def check_updates(self):
        """Checks if user has seen latest update and creates an alert if not"""
        user = anvil.users.get_user()        
        latest_update = News()
        date = News().date.text
        updates_read = user['updates_read']
        if not updates_read:
            alert(content=latest_update)
            updates_read = []
        elif date not in user['updates_read']:
            alert(content=latest_update)        
        anvil.server.call("save_user_setup", "updates_read", updates_read + [date])        
        
    def check_permissions(self):
        # 1st step of registration process requires email and password
        anvil.users.login_with_form(allow_remembered=True)
        # 2nd step of registration process requires contact data and read/accept Terms of Use
        self.force_user_setup()
        self.check_updates()
        self.check_for_boss()
    
    def required_fields_are_populated(self):
        """ Checks that all required fields are completed """
        user = anvil.users.get_user()
        checks = [user['house_number']]
        checks += [user['street']]
        checks += [user['town']]
        checks += [user['county']]
        checks += [user['display_name']]
        return all(checks)
    
    def force_user_setup(self):
        """ Blocks until i) Terms of Use accepted; ii) Required contact data supplied """
        addresses = self.addresses = anvil.server.call("get_address_hierarchy", LOCALE)
        while not anvil.users.get_user()['terms_accepted']:
            alert(content=TermsOfUse(), title = "Please read and accept the following Privacy Statement & Terms of Use:", large=True,)
        while not self.required_fields_are_populated():
            alert(content=UserSetup(addresses), title = "Please confirm your personal details:", large=True,)

    def highlight_selected_menu(self, selected):
        """ Visual confirmation of currently selected Menu item """
        images = {self.menu_my_offers: self.image_1,
                  self.menu_contact_us: self.image_1,
          self.menu_my_requests: self.image_2,
          self.menu_my_details: self.image_2,
          self.menu_my_matches: self.image_3,
          self.menu_about: self.image_3,
          self.menu_my_deliveries: self.image_4,}   
        for button in images:
            button.bold = False
            button.font_size = menu_font_size
        selected.bold = True
        selected.font_size = menu_font_size
        # Hide all images
        for image in images.values():
            setattr(image, "visible", False)
        # Unhide selected image
        setattr(images[selected], "visible", True)
        
        
    def menu_my_offers_click(self, **event_args):
        """This method is called when the Offers menu item is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)
        
    def menu_my_requests_click(self, **event_args):
        """This method is called when the Requests menu item is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(MyRequests())
        self.highlight_selected_menu(self.menu_my_requests)
    
    def menu_my_matches_click(self, **event_args):
        """This method is called when the Matches menu item is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(Matches())
        self.highlight_selected_menu(self.menu_my_matches)
        
    def menu_my_deliveries_click(self, **event_args):
        """This method is called when the Deliveries menu item is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(Deliveries())
        self.highlight_selected_menu(self.menu_my_deliveries)        
        
    def menu_my_details_click(self, **event_args):
        """This method is called when the Data menu item is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(UserProfile())
        self.highlight_selected_menu(self.menu_my_details)

    def menu_about_click(self, **event_args):
        """This method is called when the About button is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(AboutThisApp())
        self.highlight_selected_menu(self.menu_about)
        
    def menu_contact_us_click(self, **event_args):
        """This method is called when the Contact Us button is clicked"""
        self.check_permissions()
        sender = event_args['sender']
        self.column_panel_1.background = sender.background
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(TitleButton(sender.tag, sender.background))
        self.column_panel_1.add_component(ContactUs())
        self.highlight_selected_menu(self.menu_contact_us)


    def log_out_click(self, **event_args):
        """This method is called when the Log Out button is clicked"""
#         self.clear()
#         self.remove_from_parent()
        anvil.users.logout()
        anvil.users.login_with_form()
        self.refresh_data_bindings()
        self.menu_my_details.raise_event("click")









