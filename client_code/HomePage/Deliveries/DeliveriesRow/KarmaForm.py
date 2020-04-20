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
    def __init__(self, row_id, status_dict_key, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.row_id = row_id
        self.status_dict_key = status_dict_key
        self.date.pick_time = True
        self.date.date = datetime.datetime.today()
        self.date.format = "D %b %Y"
        self.rating = self.label_3.text
        self.feedback.background = yellow
        
    def add_footer(self):
        """Adds details of the person giving feedback and the person who it's about"""
        footer = f"\n[{self.regarding.text} was the {self.regarding_role.text},"
        footer += f"{self.user.text} was the {self.user_role.text}]"
        return footer
    
    def submit_form(self, **event_args):
        """This method is called when the button is clicked"""
        regarding_user = anvil.server.call('get_user_from_display_name', self.regarding.text)
        user = anvil.server.call('get_user_from_display_name', self.user.text)
        kwargs = {'from_user': user,
                  'regarding_user': regarding_user,
                  'date_time': datetime.datetime.now(),
                  'feedback': self.feedback.text + self.add_footer(),
                  'rating': self.rating,}
        anvil.server.call("add_karma_row", **kwargs)
        match = anvil.server.call("get_match_by_id", self.row_id)
        status_dict = match['status_dict']
        status_dict[self.status_dict_key] = True
        anvil.server.call("save_matches_status_dict", match,  status_dict)
        buttons = [x for x in self.parent.parent.get_components() if type(x) == Button]
#         print(buttons)
        for button in buttons:
            button.enabled = True
#         self.parent.parent.refresh_data_bindings()
#         print("ppp",type(self.parent.parent.parent))
#         self.parent.parent.item.status_view.enabled = True
        print("remember to unhash the server call!")
        self.clear()
        alert("""Thanks for taking the time to keep things going around and coming around!""")

    def cancel_button_click(self, **event_args):
      """This method is called when the button is clicked"""

      self.clear()
#       self.parent.visible = False

    def description_change(self, **event_args):
      """This method is called when the text in this text area is edited"""
      pass

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
      self.rating = stars[event_args['sender']].text

























