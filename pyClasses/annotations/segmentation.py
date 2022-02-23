from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

from kivy.properties import NumericProperty, StringProperty

from pyClasses.annotations.annotationHandler import AnnotationHandler

import json

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

class_colors = [
          np.array([0,0,0]), # Background, 0th class
          np.array([1,0,0]),
          np.array([0,1,0]),
          np.array([0,0,1]),
          ]

class SegmentationHandler(AnnotationHandler):
  def __init__(self, *args, **kwargs):
    # super(SegmentationHandler, self).__init__(SegmentationImg, *args, **kwargs)
    self.anoClass = SegmentationImg
    self.name = "Segmentation"
    self.image_widget = self.anoClass()

    # Create controlbox for tuning the number of classes
    self.class_controlbox = ControlBox(size_hint_x=0.1)
    # self.class_controlbox.bind(value=self.image_widget.update_class_num)

    # create toolbox_widget list for external display to modify
    self.toolbox_widgets = [self.class_controlbox]

  def addAnnotation(self, parent, scaler, touch, *args, **kwargs):
    if self.image_widget.parent:
      if self.image_widget.collide_point(*touch.pos):
        x, y = touch.pos
        parent = self.image_widget
        imageSize = parent.norm_image_size
        pic_zero = list(map( lambda x: x[0] - x[1]/2 , zip(parent.center, imageSize) ) )

        relative_x = (x - pic_zero[0])/imageSize[0]
        relative_y = 1-(y - pic_zero[1])/imageSize[1]

        true_x, true_y = int(relative_x*parent.label.shape[1]), int((1-relative_y)*parent.label.shape[0])
        parent.label[true_y-5:true_y+5,true_x-5:true_x+5,1] = 1
        parent.update_image()

    else:
      # Create Overlay image for label, bind position and size to the main image ones
      parent.add_widget(self.image_widget)
      self.image_widget.pos = parent.pos
      self.image_widget.size = parent.size
      parent.bind(pos=self.image_widget.setter('pos'), size=self.image_widget.setter('size'))
      # self.image_widget.label = np.random.uniform(size=(parent.arrayImg.shape[:2] + (2,)))>0.5
      self.image_widget.label = np.zeros((parent.arrayImg.shape[:2] + (2,)), dtype=bool)
      self.image_widget.label_image = (np.random.uniform(size=self.image_widget.label.shape[:2] + (4,))*255).astype(np.uint8)

      self.image_widget.update_image()
      # shp = self.image_widget.label_image.shape
      # texture = Texture.create(size=(shp[1], shp[0]))
      # texture.blit_buffer(self.image_widget.label_image.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')
      # self.image_widget.texture = texture

  def saveAnnotations(self, imgName, parent):
    return None


class SegmentationImg(Image, ButtonBehavior):
  def __init__(self, *args, **kwargs):
    super(SegmentationImg, self).__init__(*args, **kwargs)
    self.stagingMode = self.suicide
    self.currentMode = self.on_press
    self.opacity = 0.5

  def update_image(self):
    # Update opacity for images. Background areas are completely transparent (0th class is considered background)
    self.label_image[..., 3] = np.any(self.label[..., 1:], axis=-1)*(255*self.opacity)

    # Update each class according to preset color scheme in this file
    for i in range(1, self.label.shape[-1]):
      self.label_image[self.label[..., i] > 0.5, :-1] = class_colors[i]*255
      # print(i,self.label_image.dtype, np.max(self.label_image[..., -1]), np.max(self.label_image[..., :-1]))

    # Create new texture and blit to it
    shp = self.label_image.shape
    texture = Texture.create(size=(shp[1], shp[0]))
    texture.blit_buffer(self.label_image.reshape(-1), colorfmt='rgba', bufferfmt='ubyte')
    self.texture = texture    

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

class ControlBox(BoxLayout):
    """docstring for ControlBox"""
    perc_inc = NumericProperty(0.1)
    name = StringProperty("tst")
    typ = StringProperty("exp")
    min_val = NumericProperty(0)
    max_val = NumericProperty(1)
    value = NumericProperty(2)
    precision = NumericProperty(1)
    input_filter = StringProperty("float")

    def change_value(self, sign, *args):
        value = float(self.value)
        if self.typ == "exp":
            value += sign*self.perc_inc*value
        elif self.typ == "linear":
            value += sign*self.perc_inc
        elif self.typ == "linear_round":
            value = value + sign*self.perc_inc
            # value = (tmp_value//self.perc_inc) * self.perc_inc

        value = min(self.max_val, max(self.min_val, value))
        self.value = value

    def __init__(self, **kwargs):
        super(ControlBox, self).__init__(**kwargs)

        # Add control functions
        # self.ids.inc.on_press = print
        # self.ids.inc.on_press = partial(self.change_value, 1)
        # self.ids.dec.on_press = partial(self.change_value, -1)
