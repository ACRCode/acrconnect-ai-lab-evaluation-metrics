import json
import sys
import os.path

from factories.clasification import ClassificationEvaluationFactory
from factories.continuous import ContinuousEvaluationFactory
from factories.boundingBox import BoundingBoxEvaluationFactory
from factories.segmentation import SegmentationEvaluationFactory
from utils.binaryMap import BinaryClassificationMap

class EvaluationFactory:
    """
    Factory that uses sub factories for every algorith type to create the final metrics output

    ...

    Attributes
    ----------
    args : arguments
        the arguments obtained from running the python script
    """
    def __init__(self, args):


        if not os.path.exists(args.dataset_file_path):
            raise Exception('The dataset json file {0} does not exist'.format(args.dataset_file_path))
        with open(args.dataset_file_path) as datasetFile:
            self.dataset = json.load(datasetFile)
        if not os.path.exists(args.output_file_path):
            raise Exception('The output json file {0} does not exist'.format(args.output_file_path))
        with open(args.output_file_path) as outputJsonFile:
            self.output = json.load(outputJsonFile) 

        if args.use_cache and args.evaluation_file_path is not None and len(args.evaluation_file_path) > 0 and os.path.isfile(args.evaluation_file_path) and os.stat(args.evaluation_file_path).st_size > 0:
            with open(args.evaluation_file_path) as previousEvaluationFile:
                self.previousEvaluation = json.load(previousEvaluationFile)
        else:
            self.previousEvaluation = None

        binaryMaps = None if args.binary_maps is None else {k:BinaryClassificationMap(v["presentLabels"], v["absentLabels"]) for (k,v) in args.binary_maps.items()}
        self.classificationFactory = ClassificationEvaluationFactory(self.dataset, self.output, args.threshold, binaryMaps)
        self.continuousFactory = ContinuousEvaluationFactory(self.dataset, self.output)
        self.boundingBoxFactory = BoundingBoxEvaluationFactory(self.dataset, self.output, None if self.previousEvaluation is None else self.previousEvaluation["boundingBox"])
        self.segmentationFactory = SegmentationEvaluationFactory(self.dataset, self.output)

    def Create(self):   
        """
        Creates the evaluation
        """
        
        evaluation = {
            "classification": self.classificationFactory.Create(),
            "continuous": self.continuousFactory.Create(),
            "boundingBox": self.boundingBoxFactory.Create(),
            "segmentation": self.segmentationFactory.Create()
        }
        return evaluation

