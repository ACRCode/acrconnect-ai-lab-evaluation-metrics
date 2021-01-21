import json

from .base import MetricsFactory
from evaluations.continuous import ContinuousEvaluation

class ContinuousEvaluationFactory(MetricsFactory):

    def __init__(self, dataset, output):
        super(ContinuousEvaluationFactory, self).__init__(dataset, output, "continuous", "continuousOutput")
        
        self.datasetStudyUids = list()

        for key in self.groundTruths.keys():
            groundTruthDict = self.groundTruths[key]
            self.datasetStudyUids = list(set().union(self.datasetStudyUids, list(groundTruthDict.keys())))
        
    def Create(self):
        #don't use self.predictedKeys as we don't need to intersect prediction keys with ground truth keys for continuous evaluations
        evaluations = list(map(self.getEvaluationWrapperForkey, self.predictions.keys()))
        return evaluations
        
    #for continuous evaluations we have to calculate unknowns and predictions
    #differently because our output keys are not necessarily contained in our ground truth keys
    def getEvaluationWrapperForkey(self, key):    
        """
        Builds the common wrapper object for an evaluation that will contain information about unknowns, failures, and keys

        Parameters
        ----------
        key : string
            they key of the annotation class for this evaluation wrapper

        Returns
        -------
        json object
            The evaluation wrapper

        """

        predictionsForKey  = self.predictions[key]

        #UNKNOWNS
        #filter all the unknowns from our predictions as these should be excluded from the metrics calculations
        nonNullPredictions  = {k:v for k,v in predictionsForKey.items()  if v is not None}
        #now get a list of all the unknown predictions
        nullPredictions  = {k:v for k,v in predictionsForKey.items()  if v is None}
        unknowns = list(map(lambda x: x[0], nullPredictions.items()))
        
        #FAILURES
        #Here we just consider wether there is an output for the particular study that has a "continuousOutput" object
        failures = list(filter(lambda uid: uid not in predictionsForKey.keys(), self.datasetStudyUids))

        return {
            "key": key,
            "unknowns": unknowns,
            "failures": failures,
            "output": ContinuousEvaluation(key, self.groundTruths, nonNullPredictions)
        }