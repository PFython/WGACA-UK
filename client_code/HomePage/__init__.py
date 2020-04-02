from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..MyOffers import MyOffers
from ..UserProfile import UserProfile
from ..MyRequests import MyRequests
from ..Matches import Matches
from ..Deliveries import Deliveries

class HomePage(HomePageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.fcolour = '#0080c0' # Foreground colour and active menu button background
        self.bcolour = '#cae4ff' # Background colour
        self.xcolour = '#eaf4ff' # Deselected text box
        self.ycolour = '#00a3f0' # Inactive menu button background
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.column_panel_1.add_component(MyOffers())
        self.highlight_selected_menu(self.menu_my_offers)


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







