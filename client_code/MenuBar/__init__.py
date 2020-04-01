from ._anvil_designer import MenuBarTemplate
from anvil import *
import anvil.server
import anvil.microsoft.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..MyOffers import MyOffers
from ..UserProfile import UserProfile
from ..MyRequests import MyRequests

class MenuBar(MenuBarTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)

    def highlight_selected_menu(self, selected):
        self.menu_my_offers.foreground = ''
        self.menu_my_requests.foreground = ''
        self.menu_overview.foreground = ''
        self.menu_my_deliveries.foreground = ''
        self.menu_my_profile.foreground = ''
        self.menu_my_offers.underline = False
        self.menu_my_requests.underline = False
        self.menu_overview.underline = False
        self.menu_my_deliveries.underline = False
        self.menu_my_profile.underline = False
        selected.foreground = '#bb44a0'
        selected.underline = True
        
    def menu_my_offers_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)

    def menu_my_profile_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(UserProfile())
        self.highlight_selected_menu(self.menu_my_profile)

    def menu_my_requests_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.column_panel_1.clear()
        # Add Page1 to the content panel
        self.column_panel_1.add_component(MyRequests())
        self.highlight_selected_menu(self.menu_my_requests)



