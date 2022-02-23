from pyClasses.annotations.landmark import LandmarkHandler
from pyClasses.annotations.line import LineHandler
from pyClasses.annotations.boundingBox import BoundingBoxHandler
from pyClasses.annotations.segmentation import SegmentationHandler

annotationRegister = {
  "Landmark": LandmarkHandler(),
  "Line": LineHandler(),
  "BoundingBox": BoundingBoxHandler(),
  "Segmentation": SegmentationHandler(),
}
