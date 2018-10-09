import os
from functools import partial
import json

from pyClasses.landmark import Landmark
from pyClasses.displaylayout import DisplayLayout
from pyClasses.toolbar import ToolbarContainer
from pyClasses.buttons import ToggleButtonAlt

from kivy.uix.boxlayout import BoxLayout

def appendFuns(*funs):
  def tmp(*args, **kwargs):
    for fun in funs:
      ret = fun(*args, **kwargs)
    return ret
  return tmp

class MainBox(BoxLayout):
  def __init__(self, **kwargs):
    super(MainBox, self).__init__(**kwargs)

    self.previousList = []
    self.nextList = []

    # References to main widgets
    displayLayout = self.ids.display
    landmarkParent = displayLayout.newImage
    reloadButton = self.ids.reload
    nextButton = self.ids.next
    prevButton = self.ids.prev
    dragButton = self.ids.drag
    insertButton = self.ids.insert
    saveButton = self.ids.save
    deleteButton = self.ids.deleteToggle
    clearButton = self.ids.clearall

    # Landmark parent's on_touch_down modes
    dragFunction = landmarkParent.on_touch_down
    insertFunction =  appendFuns( partial(self.addLandmark, landmarkParent), landmarkParent.on_touch_down )
    deleteFunction = landmarkParent.on_touch_down
    defaultFunction = dragFunction

    # ToggleButton toggler functions
    dragButton.toggleFunction = partial(self.toggleMouseFunction, landmarkParent, dragFunction, defaultFunction)
    insertButton.toggleFunction = partial(self.toggleMouseFunction, landmarkParent, insertFunction, defaultFunction)
    deleteButton.toggleFunction = partial(self.landmarkSuicideModeToggle, landmarkParent)

    # Button operations
    reloadButton.on_press = self.updateImageList
    nextButton.on_press = self.nextImage
    prevButton.on_press = self.prevImage
    saveButton.on_press = partial(self.saveShape, landmarkParent)
    clearButton.on_press = partial(self.clearLandmarks, landmarkParent)

    # Starting states
    insertButton.state = "down"
    reloadButton.on_press()

  def clearLandmarks(self, landmarkParent, *args, **kwargs):
    for child in list(landmarkParent.children):
      if isinstance(child, Landmark):
        landmarkParent.remove_widget(child)

  def saveShape(self, landmarkParent, *args, **kwargs):
    coords = []
    for child in landmarkParent.children:
      if isinstance(child, Landmark):
        coords.append(child.center)

    dataPoint = {'imgName': self.nextList[len(self.nextList)-1], 'coords': coords}
    jsonString = json.dumps(dataPoint)

    with open('landmarks.json', 'a') as saveFile:
      saveFile.write(jsonString)
      saveFile.write("\n")

  def addLandmark(self, landmarkParent, touch, *args, **kwargs):
    x, y = touch.pos

    newLandmark = Landmark()
    landmarkParent.add_widget(newLandmark)
    newLandmark.center = (x,y)

  def landmarkSuicideModeToggle(self, landmarkParent, *args, **kwargs):
    for child in landmarkParent.children:
      if isinstance(child, Landmark):
        child.suicideModeToggle()

  def toggleMouseFunction(self, widget, function1, function2,  *args, **kwargs):
    if widget.on_touch_down == function1:
      widget.on_touch_down = function2
    else:
      widget.on_touch_down = function1

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
