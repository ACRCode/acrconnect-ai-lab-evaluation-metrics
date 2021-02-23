import json

from .base import MetricsFactory
from evaluations.segmentation import SegmentationEvaluation

class SegmentationEvaluationFactory(MetricsFactory):

    def __init__(self, dataset, output):
        super(SegmentationEvaluationFactory, self).__init__(dataset, output, "segmentation", "segmentationOutput")
        
    def getEvaluation(self, key, groundTruths, predictions):
        return SegmentationEvaluation(groundTruths, predictions)
       