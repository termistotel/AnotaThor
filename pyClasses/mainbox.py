import os
from functools import partial
import json

from pyClasses.landmark import Landmark
from pyClasses.displaylayout import DisplayLayout
from pyClasses.toolbar import ToolbarContainer

from kivy.uix.boxlayout import BoxLayout


class MainBox(BoxLayout):
  def __init__(self, **kwargs):
    super(MainBox, self).__init__(**kwargs)

    self.previousList = []
    self.nextList = []


    # References to main widgets
    displayLayout = self.ids.display
    self.updateImageList()

    reloadButton = self.ids.reload
    nextButton = self.ids.next
    prevButton = self.ids.prev
    dragButton = self.ids.drag
    insertButton = self.ids.insert
    saveButton = self.ids.save

    # Two functions of display
    dragFunction = displayLayout.on_touch_down
    insertFunction = self.addLandmark

    # Button operations
    reloadButton.on_press = self.updateImageList
    nextButton.on_press = self.nextImage
    prevButton.on_press = self.prevImage
    dragButton.on_press = partial(self.changeMouseFunction, dragFunction)
    insertButton.on_press = partial(self.changeMouseFunction, insertFunction)
    saveButton.on_press = self.saveShape

    # Starting states
    insertButton.state = "down"
    displayLayout.on_touch_down = insertFunction

  def saveShape(self, *args, **kwargs):
    display = self.ids.display
    coords = []
    for child in display.children:
      if isinstance(child, Landmark):
        coords.append(child.center)

    dataPoint = {'imgName': self.nextList[len(self.nextList)-1], 'coords': coords}
    jsonString = json.dumps(dataPoint)

    with open('landmarks.json', 'a') as saveFile:
      saveFile.write(jsonString)
      saveFile.write("\n")

  def addLandmark(self, touch, *args, **kwargs):
    displayLayout = self.ids.display
    x, y = touch.pos

    newLandmark = Landmark()
    displayLayout.add_widget(newLandmark)
    newLandmark.center = (x,y)

  def changeMouseFunction(self, function, *args, **kwargs):
    self.ids.display.on_touch_down = function

  def updateImageList(self, *args, **kwargs):
    self.nextList = os.listdir('images/')
    self.previousList = []
    self.nextList.sort(reverse=True)
    self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

  def nextImage(self, *args, **kwargs):
    if len(self.nextList) > 1:
      self.previousList.append(self.nextList.pop())
      self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

  def prevImage(self, *args, **kwargs):
    if len(self.previousList) >=1:
      self.nextList.append(self.previousList.pop())
      self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])