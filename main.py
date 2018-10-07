import kivy
kivy.require('1.10.0') # replace with your current kivy version !

import os
from kivy.app import App
from pyClasses.landmark import Landmark


class AnotathorApp(App):
  def build(self):
    mainbox = MainBox()
    return mainbox


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty


class MainBox(BoxLayout):
  def __init__(self, **kwargs):
    super(MainBox, self).__init__(**kwargs)

    self.previousList = []
    self.nextList = []
    self.updateImageList()

    displayLayout = self.ids.display
    reloadButton = self.ids.reload
    nextButton = self.ids.next
    prevButton = self.ids.prev

    displayLayout.on_touch_down = lambda touch: self.addLandmark(displayLayout, touch)
    reloadButton.on_press = self.updateImageList
    nextButton.on_press = self.nextImage
    prevButton.on_press = self.prevImage

  def addLandmark(self, displayLayout, touch):
    x, y = touch.pos

    newLandmark = Landmark()
    displayLayout.add_widget(newLandmark)
    newLandmark.center = (x,y)

    print(newLandmark.center)
    print(newLandmark.pos)
    print(newLandmark.width)

  def updateImageList(self, *args, **kwargs):
    self.nextList = os.listdir('images/')
    self.previousList = []
    self.nextList.sort(reverse=True)
    self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])


  def nextImage(self, *args, **kwargs):
    if len(self.nextList) > 1:
      self.previousList.append(self.nextList.pop())
      self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

    print('images/' + self.nextList[len(self.nextList)-1])

  def prevImage(self, *args, **kwargs):
    if len(self.previousList) >=1:
      self.nextList.append(self.previousList.pop())
      self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

    print('images/' + self.nextList[len(self.nextList)-1])

class ToolbarContainer(BoxLayout):
  pass

class DisplayLayout(FloatLayout):
  # TODO: Implement changable size of landmarks
  # landmarkScale = NumericProperty(0.1)

  def changeImg(self, src):
    if src:
      self.clear_widgets()
      self.add_widget(Image(source=src))

if __name__ == '__main__':
    AnotathorApp().run()