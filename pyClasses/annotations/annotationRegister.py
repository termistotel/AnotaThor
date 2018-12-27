from pyClasses.annotations.landmark import LandmarkHandler
from pyClasses.annotations.line import LineHandler
from pyClasses.annotations.boundingBox import BoundingBoxHandler

annotationRegister = {
  "Landmark": LandmarkHandler(),
  "Line": LineHandler(),
  "BoundingBox": BoundingBoxHandler(),
}
