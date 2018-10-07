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

    displayLayout = self.ids.display
    displayLayout.on_touch_down = lambda touch: self.addLandmark(displayLayout, touch)


  def addLandmark(self, displayLayout, touch):
    x, y = touch.pos

    newLandmark = Landmark()
    displayLayout.add_widget(newLandmark)
    newLandmark.center = (x,y)

    print(newLandmark.center)
    print(newLandmark.pos)
    print(newLandmark.width)

class ToolbarContainer(BoxLayout):
  pass

class DisplayLayout(FloatLayout):
  pass
  # TODO: Implement changable size of landmarks
  # landmarkScale = NumericProperty(0.1)

class Landmark(DragBehavior, Widget):
  def __init__(self, **kwargs):
    super(Landmark, self).__init__(**kwargs)

if __name__ == '__main__':
    AnotathorApp().run()