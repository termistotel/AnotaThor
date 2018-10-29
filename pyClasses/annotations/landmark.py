from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior

from pyClasses.annotations.annotationHandler import AnnotationHandler

import json

class LandmarkHandler(AnnotationHandler):
  def __init__(self, *args, **kwargs):
    self.anoClass = Landmark
    self.name = "Landmark"

  def addAnnotation(self, annotationParent, scaler, touch, *args, **kwargs):
    if annotationParent.collide_point(*touch.pos):
      x, y = touch.pos

      newLandmark = Landmark(scaler)
      annotationParent.add_widget(newLandmark)
      newLandmark.center = (x,y)

  def saveAnnotations(self, imgName, annotationParent):
    coords = []
    relative = []
    imageSize = annotationParent.norm_image_size
    pic_zero = list(map( lambda x: x[0] - x[1]/2 , zip(annotationParent.center, imageSize) ) )

    for child in annotationParent.children:
      if isinstance(child, Landmark):
        relative_x = (child.center[0] - pic_zero[0])/imageSize[0]
        relative_y = (child.center[1] - pic_zero[1])/imageSize[1]
        relative.append((relative_x, relative_y))
        coords.append(child.center)

    dataPoint = {'imgName': imgName, 'coords': coords, 'relative': relative}
    jsonString = json.dumps(dataPoint)

    return jsonString

class Landmark(DragBehavior, ButtonBehavior, Widget):
  max_width = 80
  max_height = 80

  def __init__(self, scaler, *args, **kwargs):
    self.scaler = scaler
    super(Landmark, self).__init__(*args, **kwargs)
    self.stagingMode = self.suicide
    self.currentMode = self.on_press

  def suicideModeToggle(self):
    self.stagingMode, self.currentMode = self.currentMode, self.stagingMode
    self.on_press = self.currentMode

  def suicide(self, *args, **kwargs):
    self.parent.remove_widget(self)
