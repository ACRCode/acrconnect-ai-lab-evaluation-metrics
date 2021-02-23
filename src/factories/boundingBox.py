import json

from .base import MetricsFactory
from evaluations.boundingBox import BoundingBoxEvaluation

class BoundingBoxEvaluationFactory(MetricsFactory):

    def __init__(self, dataset, output):
        super(BoundingBoxEvaluationFactory, self).__init__(dataset, output, "boundingBox", "boundingBoxOutput")
        
    def getEvaluation(self, key, groundTruths, predictions):
        return BoundingBoxEvaluation(groundTruths, predictions)
       