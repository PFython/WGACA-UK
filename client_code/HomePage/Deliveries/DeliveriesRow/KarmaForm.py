from ._anvil_designer import KarmaFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
from ....Globals import yellow

class KarmaForm(KarmaFormTemplate):
    def __init__(self, row_id, regarding, regarding_role, user_role, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        print(row_id, regarding, regarding_role, user_role)
        self.row_id = row_id
        self.regarding = regarding
        self.regarding_role.text = regarding_role
        self.regarding_name.text = regarding['display_name']
        self.user_role.text = user_role
        self.user_name.text = anvil.users.get_user()['display_name']
        self.user = anvil.users.get_user()
        self.date.pick_time = True
        self.date.date = datetime.datetime.today()
        self.date.format = "D %b %Y"
        self.rating = self.label_3.text
        self.feedback.background = yellow
        
    def add_footer(self):
        """Adds details of the person giving feedback and the person who it's about"""
        footer = f"\n[{self.regarding_name.text} was the {self.regarding_role.text},"
        footer += f"{self.user_name.text} was the {self.user_role.text}]"
        return footer
    
    def submit_form(self, **event_args):
        """This method is called when the button is clicked"""
        match = anvil.server.call("get_match_by_id", self.row_id)
        kwargs = {'from_user': self.user,
                  'regarding_user': self.regarding,
                  'date_time': datetime.datetime.now(),
                  'feedback': self.feedback.text + self.add_footer(),
                  'rating': self.rating,
                  'regarding_match': match}
        karma_form = anvil.server.call("add_karma_row", **kwargs)
        anvil.server.call("save_karma_form_to_match", self.row_id, karma_form)
        self.parent.parent.parent.show_deliveries_row()
        self.remove_from_parent()
        self.clear()
  
    def cancel_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.clear()

    def select_star(self, **event_args):
          """This method is called when a Star link is clicked"""
          stars = {self.star_5: self.label_5,
                  self.star_4: self.label_4,
                  self.star_3: self.label_3,
                  self.star_2: self.label_2,
                  self.star_1: self.label_1}
          for star in stars:
              star.icon = 'fa:star-o'
          event_args['sender'].icon = 'fa:star'

























