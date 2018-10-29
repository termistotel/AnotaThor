from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior

from pyClasses.annotations.annotationHandler import AnnotationHandler

import json

class LineHandler(AnnotationHandler):
  def __init__(self, *args, **kwargs):
    self.anoClass = Line
    self.name = "Line"

  def addAnnotation(self, lineParent, scaler, touch, *args, **kwargs):
    if lineParent.collide_point(*touch.pos):
      x, y = touch.pos

      # Work in progress
      print("new Line")

  def saveAnnotations(self, imgName, lineParent):
    return "To be implemented"

class Line(DragBehavior, ButtonBehavior, Widget):
	pass