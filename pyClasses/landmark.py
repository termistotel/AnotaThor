from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior

class Landmark(DragBehavior, Widget):
  def __init__(self, **kwargs):
    super(Landmark, self).__init__(**kwargs)