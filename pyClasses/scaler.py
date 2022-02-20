from kivy.uix.slider import Slider

class Scaler(Slider):
  annotationParent = None
  def __init__(self, *args, **kwargs):
    super(Scaler, self).__init__(*args, **kwargs)

  def on_value(self, _, value):
    if self.annotationParent:
      for annotation in self.annotationParent.children:
        annotation.scale_to(value)