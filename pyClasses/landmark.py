from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty

class Landmark(DragBehavior, ButtonBehavior, Widget):
  max_width = 80
  max_height = 80
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

class Scaler(Slider):
  landmarkParent = None
  def __init__(self, *args, **kwargs):
    super(Scaler, self).__init__(*args, **kwargs)

  def on_value(self, _, value):
    if self.landmarkParent:
      for landmark in self.landmarkParent.children:
        old_center = landmark.center.copy()
        landmark.size = landmark.max_width*value, landmark.max_height*value
        landmark.center = old_center
