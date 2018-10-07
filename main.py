import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App

class AnotathorApp(App):
  def build(self):
    mainbox = MainBox()
    return mainbox


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.properties import NumericProperty

class MainBox(BoxLayout):
  def __init__(self, **kwargs):
    super(MainBox, self).__init__(**kwargs)

class ToolbarContainer(BoxLayout):
  pass

class DisplayLayout(FloatLayout):
  pass

class Landmark(DragBehavior, Widget):
  def __init__(self, **kwargs):
    super(Landmark, self).__init__(**kwargs)

if __name__ == '__main__':
    AnotathorApp().run()