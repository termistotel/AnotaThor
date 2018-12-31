from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.behaviors import ButtonBehavior

from pyClasses.annotations.annotationHandler import AnnotationHandler

import json

# import matplotlib.pyplot as plt
import os
import cv2

class BoundingBoxHandler(AnnotationHandler):
  def __init__(self, *args, **kwargs):
    self.anoClass = BoundingBox
    self.name = "Bounding box"

  def addAnnotation(self, parent, scaler, touch, *args, **kwargs):
    if parent.collide_point(*touch.pos):
      x, y = touch.pos

      bb = BoundingBox(scaler)
      parent.add_widget(bb)
      bb.max_width = parent.norm_image_size[0]
      bb.max_height = parent.norm_image_size[1]
      bb.width = scaler.value*bb.max_width
      bb.height = scaler.value*bb.max_height
      bb.center = (x,y)

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
        cv2.imwrite('savedImages/' + outImgName, parent.arrayImg[ y-h:y, x:x+w, :])

        boxs.append((x, y-h, x+w, y))
        names.append(outImgName)

        # plt.imshow(parent.arrayImg[ y-h:y, x:x+w, :]/255)
        # plt.show()

    dataPoint = {'type': 'BoundingBox', 'orgImgName': imgName,'segImgNames': names, 'box_relative': boxs}
    jsonString = json.dumps(dataPoint)

    return jsonString


class BoundingBox(DragBehavior, ButtonBehavior, Widget):
  max_width = 80
  max_height = 80

  def __init__(self, scaler, *args, **kwargs):
    self.scaler = scaler
    super(BoundingBox, self).__init__(*args, **kwargs)
    self.stagingMode = self.suicide
    self.currentMode = self.on_press

  def suicideModeToggle(self):
    self.stagingMode, self.currentMode = self.currentMode, self.stagingMode
    self.on_press = self.currentMode

  def suicide(self, *args, **kwargs):
    self.parent.remove_widget(self)