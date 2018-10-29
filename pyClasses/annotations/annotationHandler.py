class AnnotationHandler(object):
  widgets = []

  def __init__(self, anoClass, *args, **kwargs):
    self.anoClass = anoClass
    self.name = anoClass.__name__

  def addAnnotation(self, annotationParent, scaler, touch, *args, **kwargs):
    print("Instance of " + type(self).__name__ + " has called addAnnotation method")

  def saveAnnotations(self, imgName, annotationParent):
    print(imgName)

  def update_widgets(self, widgets):
    self.widgets = widgets
