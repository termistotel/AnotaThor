from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

class DisplayLayout(FloatLayout):
  def __init__(self, **kwargs):
    self.anotations = {}

    super(DisplayLayout, self).__init__(**kwargs)

    self.newImage=Image()
    self.add_widget(self.newImage)


  def changeImg(self, src):
    if src:
      self.newImage.source=src

  def changeAnotationType(self, anot):
    try:
      new_children = self.anotations[anot]
      self.newImage.clear_widgets()
      for child in new_children:
        self.newImage.add_widget(child)
    except Exception as e:
      raise e
