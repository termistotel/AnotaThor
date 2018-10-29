from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from pyClasses.annotations.annotationRegister import annotationRegister

class DisplayLayout(FloatLayout):

  def __init__(self, **kwargs):
    self.anotations = annotationRegister
    self.current = self.anotations["Landmark"]

    super(DisplayLayout, self).__init__(**kwargs)

    self.newImage=Image()
    self.add_widget(self.newImage)

  def changeImg(self, src):
    if src:
      self.newImage.source=src

  def changeAnnotationType(self, anot):
    self.current.update_widgets(list(self.newImage.children))
    self.current = self.anotations[anot]

    new_children = self.current.widgets
    self.newImage.clear_widgets()
    for child in new_children:
      self.newImage.add_widget(child)

  def addAnnotation(self, annotationParent, *args, **kwargs):
    self.current.addAnnotation(annotationParent, *args, **kwargs)
    self.current.update_widgets(list(annotationParent.children))

  def saveAnnotations(self, imgName, annotationParent):
    return self.current.saveAnnotations(imgName, annotationParent)

  def annotationSuicideModeToggle(self, annotationParent, *args, **kwargs):
    for anoType in self.anotations:
      for anotation in self.anotations[anoType].widgets:
        anotation.suicideModeToggle()
