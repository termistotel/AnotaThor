from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty
from kivy.uix.image import Image

from pyClasses.annotations.annotationHandler import AnnotationHandler

import json

import matplotlib.pyplot as plt
import os
import cv2

class SegmentationHandler(AnnotationHandler):
  def __init__(self, *args, **kwargs):
    # super(SegmentationHandler, self).__init__(SegmentationImg, *args, **kwargs)
    self.anoClass = SegmentationImg
    self.name = "Segmentation"
    self.image_widget = self.anoClass()

  def addAnnotation(self, parent, scaler, touch, *args, **kwargs):
    print(self.image_widget.parent)
    print(parent, scaler, touch)
    # if parent.collide_point(*touch.pos):
    #   x, y = touch.pos

    #   bb = BoundingBox(scaler)
    #   parent.add_widget(bb)
    #   bb.max_width = parent.norm_image_size[0]
    #   bb.max_height = parent.norm_image_size[1]
    #   bb.width = scaler.value*bb.max_width
    #   bb.height = scaler.value*bb.max_height
    #   bb.center = (x,y)
    #   bb.scale_to(scaler.value)

  def saveAnnotations(self, imgName, parent):
    imageSize = parent.norm_image_size
    pic_zero = list(map( lambda x: x[0] - x[1]/2 , zip(parent.center, imageSize) ) )
    shp = parent.arrayImg.shape

    boxs=[]
    names=[]
    for child in parent.children:
      if isinstance(child, BoundingBox):
        relative_x = (child.x - pic_zero[0])/imageSize[0]
        relative_y = 1-(child.y - pic_zero[1])/imageSize[1]
        # relative.append((relative_x, relative_y))

        x,y = int(relative_x*shp[1]), int((relative_y)*shp[0])
        w,h = int(child.width*shp[1]/imageSize[0]), int(child.height*shp[0]/imageSize[1])

        N = len(list(os.listdir("savedImages")))
        outImgName = 'img'+"{:06d}".format(N)+'.jpg'

        starty, startx = max(0, y-h), max(0, x)
        stopy, stopx = max(1, y), max(1, x+w)
        print(starty, stopy, y, h)
        print(startx, stopx, x, w)
        patch = parent.arrayImg[ starty:stopy, startx:stopx, :]
        # plt.imshow(patch)
        # plt.show()
        cv2.imwrite('savedImages/' + outImgName, patch)

        boxs.append((x, y-h, x+w, y))
        names.append(outImgName)

    dataPoint = {'type': 'BoundingBox', 'orgImgName': imgName,'segImgNames': names, 'box_relative': boxs}
    jsonString = json.dumps(dataPoint)

    return jsonString


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