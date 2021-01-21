import json
import sys
import os.path

from factories.clasification import ClassificationEvaluationFactory
from factories.continuous import ContinuousEvaluationFactory
from utils.binaryMap import BinaryClassificationMap

class EvaluationFactory:
    def __init__(self, args):
        if not os.path.exists(args.dataset_file_path):
            raise Exception('The dataset json file {0} does not exist'.format(args.dataset_file_path))
        with open(args.dataset_file_path) as datasetFile:
            self.dataset = json.load(datasetFile)
        if not os.path.exists(args.output_file_path):
            raise Exception('The output json file {0} does not exist'.format(args.output_file_path))
        with open(args.output_file_path) as outputJsonFile:
            self.output = json.load(outputJsonFile) 

        binaryMaps = None if args.binary_maps is None else {k:BinaryClassificationMap(v["presentLabels"], v["absentLabels"]) for (k,v) in args.binary_maps.items()}
        self.classificationFactory = ClassificationEvaluationFactory(self.dataset, self.output, args.threshold, binaryMaps)
        self.continuousFactory = ContinuousEvaluationFactory(self.dataset, self.output)


    def Create(self):   
        
        evaluation = {
            "classification": self.classificationFactory.Create(),
            "continuous": self.continuousFactory.Create(),
        }
        return evaluation