from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior

class Landmark(DragBehavior, ButtonBehavior, Widget):
  max_width = 20
  mag_height = 20
  def __init__(self, slider, *args, **kwargs):
    self.scaler = slider
    super(Landmark, self).__init__(*args, **kwargs)
    self.stagingMode = self.suicide
    self.currentMode = self.on_press

  def suicideModeToggle(self):
    self.stagingMode, self.currentMode = self.currentMode, self.stagingMode
    self.on_press = self.currentMode

  def suicide(self, *args, **kwargs):
    self.parent.remove_widget(self)
