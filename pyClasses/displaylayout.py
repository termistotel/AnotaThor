from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from pyClasses.landmark import Landmark

import json

class DisplayLayout(FloatLayout):
  current = {}

  def __init__(self, **kwargs):
    self.anotations = {
                      "Landmark": {
                        "widgets": [], 
                        "addAnnotation": self.addLandmark,
                        "saveAnnotations": self.saveLandmarks
                        }, 
                      "Line": {
                        "widgets": [], 
                        "addAnnotation": self.addLine,
                        "saveAnnotations": self.saveLines
                        },
                      "Bounding Box": {
                        "widgets": []
                        }
                      }

    super(DisplayLayout, self).__init__(**kwargs)

    self.newImage=Image()
    self.add_widget(self.newImage)

  def changeImg(self, src):
    if src:
      self.newImage.source=src

  def changeAnnotationType(self, anot):
    self.current["widgets"] = list(self.newImage.children)
    self.current = self.anotations[anot]

    new_children = self.current["widgets"]
    self.newImage.clear_widgets()
    for child in new_children:
      self.newImage.add_widget(child)

  def addAnnotation(self, annotationParent, *args, **kwargs):
    self.current["addAnnotation"](annotationParent, *args, **kwargs)
    self.current["widgets"] = list(annotationParent.children)

  def saveAnnotations(self, imgName, annotationParent):
    return self.current["saveAnnotations"](imgName, annotationParent)

  def annotationSuicideModeToggle(self, annotationParent, *args, **kwargs):
    for anoType in self.anotations:
      for anotation in self.anotations[anoType]["widgets"]:
        anotation.suicideModeToggle()

  def addLandmark(self, annotationParent, touch, *args, **kwargs):
    if annotationParent.collide_point(*touch.pos):
      x, y = touch.pos

      # TODO: this line is bad
      scaler = self.parent.parent.ids.anotationsize

      newLandmark = Landmark(scaler)
      annotationParent.add_widget(newLandmark)
      newLandmark.center = (x,y)

  def saveLandmarks(self, imgName, annotationParent):
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

  def addLine(self, lineParent, touch, *args, **kwargs):
    if lineParent.collide_point(*touch.pos):
      x, y = touch.pos

      # Work in progress
      print("new Line")

  def saveLines(self, imgName, lineParent):
    return "To be implemented"
