import json

class MetricsFactory:

    def __init__(self, dataset, output, annotationTypeKey, outputTypeKey):

        if dataset is None:
            raise ValueError("no dataset found")
        if output is None:
            raise ValueError("no output found")

        #useful sorted data
        self.predictions = self.getPredictionDictionary(output, outputTypeKey)
        self.groundTruths = self.getGroundTruthDictionary(dataset, annotationTypeKey)
        self.keys = self.getkeys(dataset, annotationTypeKey)
        # contains ground truth keys that are present in our predictions
        self.predictedKeys = list(filter(lambda x: x in self.predictions.keys(), self.keys))

    def Create(self):
        evaluations = list(map(self.getEvaluationWrapperForkey, self.predictedKeys))
        return evaluations

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
        
        #only consider the ground truths that we have a prediction for, we will account for the rest as "failures"
        groundTruthsForKey = self.groundTruths[key]
        validGroundTruths = {k:v for k,v in groundTruthsForKey.items() if k in predictionsForKey}

        #FAILURES
        failedPredictions  = {k:v for k,v in groundTruthsForKey.items()  if k not in predictionsForKey.keys()}
        failures = list(map(lambda x: x[0], failedPredictions.items()))

        return {
            "key": key,
            "unknowns": unknowns,
            "failures": failures,
            "output": self.getEvaluation(key, validGroundTruths, nonNullPredictions)
        }

    def getEvaluation(self, key, groundTruths, predictions):
        raise NotImplementedError()


    # dictionary in the form of
    # {
    #   key: {
    #       studyUid: predictionLabel
    #   }
    # }
    def getPredictionDictionary(self, output, outputTypeKey):

        if output is None or len(output["studies"]) <= 0:
            return None

        predictions = {}

        for study in [s for s in output["studies"] if outputTypeKey in s and s[outputTypeKey] is not None]:
            for output in study[outputTypeKey]:
                if output["key"] not in predictions:
                    targetDict = {}
                    predictions[output["key"]] = targetDict
                else:
                    targetDict = predictions[output["key"]]

                targetDict[study["studyInstanceUID"]] = self.getTargetPredictionFromOutput(output["output"])
        return predictions

    def getTargetPredictionFromOutput(self, output):
        return output

    # dictionary in the form of
    # {
    #   key: {
    #       studyUid: groundTruth
    #   }
    # }
    def getGroundTruthDictionary(self, dataset, annotationTypeKey):
        if dataset  is None or len(dataset) <= 0:
            return None
        
        groundTruths = {}

        def processAnnotations(annotations, studyInstanceUid):
            if annotations is None:
                return
            for annotationData in annotations:
                targetGroundTruths = annotationData[annotationTypeKey]
                if targetGroundTruths is None:
                    continue

                for groundTruth in targetGroundTruths:
                    
                    if groundTruth["key"] not in groundTruths:
                        targetDict = {}
                        groundTruths[groundTruth["key"]] = targetDict
                    else:
                        targetDict = groundTruths[groundTruth["key"]]

                    targetDict[studyInstanceUid] = groundTruth["value"]

        for data in dataset:
            processAnnotations(data["annotationData"], data["studyInstanceUid"])
            if "series" not in data or data["series"] is None:
                continue
            for series in data["series"]:
                processAnnotations(series["annotationData"], data["studyInstanceUid"])
                if "instances" not in series or series["instances"] is None:
                    continue
                for instance in series["instances"]:
                    processAnnotations(instance["annotationData"], data["studyInstanceUid"])
                    if "frames" not in instance or instance["frames"] is None:
                        continue
                    for frame in instance["frames"]:
                        processAnnotations(frame["annotationData"], data["studyInstanceUid"])

        return groundTruths

        

    def getkeys(self, dataset, annotationTypeKey):
        if dataset  is None or len(dataset) <= 0:
            return None
        
        keys = set()

        def findKeys(annotations):
            if annotations is None:
                return
            for annotationData in annotations:
                targetGroundTruths = annotationData[annotationTypeKey]
                if targetGroundTruths is None:
                    continue
                for groundTruth in targetGroundTruths:
                    keys.add(groundTruth["key"])

        for data in dataset:
            findKeys(data["annotationData"])
            if "series" not in data or data["series"] is None:
                continue
            for series in data["series"]:
                findKeys(series["annotationData"])
                if "instances" not in series or series["instances"] is None:
                    continue
                for instance in series["instances"]:
                    findKeys(instance["annotationData"])
                    if "frames" not in instance or instance["frames"] is None:
                        continue
                    for frame in instance["frames"]:
                        findKeys(frame["annotationData"])

        return keys
