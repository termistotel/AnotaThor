from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

class DisplayLayout(FloatLayout):
  def __init__(self, **kwargs):
    super(DisplayLayout, self).__init__(**kwargs)

    self.newImage=Image()
    self.add_widget(self.newImage)

  # TODO: Implement changable size of landmarks
  # landmarkScale = NumericProperty(0.1)

  def changeImg(self, src):
    if src:
      self.newImage.source=src