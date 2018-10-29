from kivy.uix.slider import Slider

class Scaler(Slider):
  annotationParent = None
  def __init__(self, *args, **kwargs):
    super(Scaler, self).__init__(*args, **kwargs)

  def on_value(self, _, value):
    if self.annotationParent:
      for annotation in self.annotationParent.children:
        old_center = annotation.center.copy()
        annotation.size = annotation.max_width*value, annotation.max_height*value
        annotation.center = old_center
