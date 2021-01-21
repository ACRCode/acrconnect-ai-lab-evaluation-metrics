import json

from .base import MetricsFactory
from evaluations.classification import ClassificationEvaluation

class ClassificationEvaluationFactory(MetricsFactory):

    def __init__(self, dataset, output, threshold, binary_maps):
        self.threshold = threshold
        self.binary_maps = binary_maps
        super(ClassificationEvaluationFactory, self).__init__(dataset, output, "classification", "classificationOutput")
        self.rocInputs = self.getROCInputDictionary(output, self.groundTruths, self.predictions, self.binary_maps)
        
    def getEvaluation(self, key, groundTruths, predictions):
        return ClassificationEvaluation(groundTruths, predictions, self.rocInputs[key], self.threshold)
       
    def getTargetPredictionFromOutput(self, output):
        #unknowns
        if output is None:
            return None
        #binary classifications
        elif len(output) == 1:
            firstValue = next(iter(output.values()))
            firstKey = next(iter(output.keys()))
            if firstValue >= self.threshold:
                return firstKey
            else:
                return "0"
        #multi-class
        else:
            maxLabel = max(output.keys(), key=(lambda key: output[key]))
            return maxLabel
        return output


    def getROCInputDictionary(self, outputs, groundTruths, predictions, binary_maps):
        if predictions  is None or groundTruths  is None:
            return None

        rocInputs = {}
        
        for study in [s for s in outputs["studies"] if "classificationOutput" in s and s["classificationOutput"] is not None]:
            for output in study["classificationOutput"]:
                if output["key"] not in rocInputs:
                    targetDict = {}
                    rocInputs[output["key"]] = targetDict
                else:
                    targetDict = rocInputs[output["key"]]

                #unknowns, we don't need to include unknowns on our ROC inputs since this can just be skipped as no calculation can take place on them
                if output["output"] is None:
                    continue;
                    
                
                for predictionKey in output["output"].keys():
                    outputVal = output["output"][predictionKey]

                    #make sure we have a matching ground truth for our predictions, otherwise, just ignore this prediction
                    if output["key"] not in groundTruths or study["studyInstanceUID"] not in groundTruths[output["key"]]:
                        continue
                    
                    BinaryRocKey = "Binary_ROC"

                    # when we do binary mapping, only take the first positive value as we well aggregate the rest of the positives
                    # and the negatives will simply be implied
                    if binary_maps is not None and output["key"] in binary_maps and binary_maps[output["key"]].mapLabel(predictionKey) == "1":
                        if BinaryRocKey not in targetDict:
                            rocIns = {}
                            targetDict[BinaryRocKey] = rocIns
                        else:
                            rocIns = targetDict[BinaryRocKey]
                        if("actual" not in rocIns):
                            rocIns["actual"] = []
                        if("expected" not in rocIns):
                            rocIns["expected"] = []

                        # for binary maps, the probability of whether a study is classified as "positive" or "negative" would
                        # be the sum of the probabilities of all the predictions in the same binary split
                        map = binary_maps[output["key"]]
                        siblingLabels = map.getSiblingLabels(predictionKey)
                        aggregate = 0
                        for label in output["output"].keys():
                            if label not in siblingLabels:
                                continue;
                            aggregate += output["output"][label]
                        rocIns["actual"].append(aggregate)

                        # similarly to the multi-classification actual flag calculation
                        # but we have to do a bitwise or on all the labels
                        if groundTruths[output["key"]][study["studyInstanceUID"]] in siblingLabels:
                            expected = 1
                        else:
                            expected = 0
                        rocIns["expected"].append(expected)

                        break # we are done with this output
                    
                    # if we have a binary classification (either is or isn't)
                    elif len(output["output"].keys()) == 1:
                        
                        if BinaryRocKey not in targetDict:
                            rocIns = {}
                            targetDict[BinaryRocKey] = rocIns
                        else:
                            rocIns = targetDict[BinaryRocKey]
                        if("actual" not in rocIns):
                            rocIns["actual"] = []
                        if("expected" not in rocIns):
                            rocIns["expected"] = []

                        rocIns["actual"].append(outputVal)
                        expected = 0 if groundTruths[output["key"]][study["studyInstanceUID"]] == "0" else 1
                        rocIns["expected"].append(expected)

                    # otherwise we have to find out whether our prediction falls in our class or a different class (pseudo-binary)
                    # basically, do we expect this or not this?
                    else:
                        if predictionKey not in targetDict:
                            rocIns = {}
                            targetDict[predictionKey] = rocIns
                        else:
                            rocIns = targetDict[predictionKey]
                        if("actual" not in rocIns):
                            rocIns["actual"] = []
                        if("expected" not in rocIns):
                            rocIns["expected"] = []

                        rocIns["actual"].append(outputVal)
                        expected = 1 if groundTruths[outputKey][study["studyInstanceUID"]] == outputVal else 0
                        rocIns["expected"].append(expected)
        
        return rocInputs
