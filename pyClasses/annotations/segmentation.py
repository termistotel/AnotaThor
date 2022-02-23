from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

from pyClasses.annotations.annotationHandler import AnnotationHandler

import json

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

class SegmentationHandler(AnnotationHandler):
  def __init__(self, *args, **kwargs):
    # super(SegmentationHandler, self).__init__(SegmentationImg, *args, **kwargs)
    self.anoClass = SegmentationImg
    self.name = "Segmentation"
    self.image_widget = self.anoClass()

  def addAnnotation(self, parent, scaler, touch, *args, **kwargs):
    if self.image_widget.parent:
      pass
    else:
      # Create Overlay image for label, bind position and size to the main image ones
      parent.add_widget(self.image_widget)
      self.image_widget.pos = parent.pos
      self.image_widget.size = parent.size
      parent.bind(pos=self.image_widget.setter('pos'), size=self.image_widget.setter('size'))
      self.image_widget.label = np.zeros(parent.arrayImg.shape[:2] + (1,), dtype = bool)

      self.image_widget.label_image = (np.random.uniform(size=self.image_widget.label.shape[:2] + (4,))*255).astype(np.uint8)
      shp = self.image_widget.label_image.shape
      texture = Texture.create(size=(shp[1], shp[0]))
      texture.blit_buffer(self.image_widget.label_image.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')
      self.image_widget.texture = texture

  def saveAnnotations(self, imgName, parent):
    return None


class SegmentationImg(Image, ButtonBehavior):
  def __init__(self, *args, **kwargs):
    super(SegmentationImg, self).__init__(*args, **kwargs)
    self.stagingMode = self.suicide
    self.currentMode = self.on_press

  def suicideModeToggle(self):
    self.stagingMode, self.currentMode = self.currentMode, self.stagingMode
    self.on_press = self.currentMode

  def suicide(self, *args, **kwargs):
    self.parent.remove_widget(self)
    del self

  def scale_to(self, value):
    self.line_width = max(1, self.max_line_width*value)

  def scroll_to(self, value):
    old_center = self.center.copy()
    self.current_scale = min(max(0.01, self.current_scale + value), 1)
    self.size = self.max_width*self.current_scale, self.max_height*self.current_scale
    self.center = old_center