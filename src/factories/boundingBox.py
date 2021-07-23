import json

from .base import MetricsFactory
from evaluations.boundingBox import BoundingBoxEvaluation

class BoundingBoxEvaluationFactory(MetricsFactory):

    def __init__(self, dataset, output, previousEvaluation):
        super(BoundingBoxEvaluationFactory, self).__init__(dataset, output, "boundingBox", "boundingBoxOutput")
        self.previousEvaluation = previousEvaluation
        
    def getEvaluation(self, key, groundTruths, predictions):
        return BoundingBoxEvaluation(key, 
            groundTruths, 
            predictions, 
            None if self.previousEvaluation is None else [x for x in self.previousEvaluation if x["key"] == key][0]["output"]
        )
       