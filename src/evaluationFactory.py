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

        #path transversal mitigation
        self.securePath(args.dataset_file_path)
        self.securePath(args.output_file_path)
        self.securePath(args.evaluation_file_path)

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
        self.boundingBoxFactory = BoundingBoxEvaluationFactory(self.dataset, self.output)
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

    def securePath(self, path):
        """
        secures paths for path transversal vulnerabilities. Throws security exception if path is insecure
        """
        examplesFolderPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../examples')
        aiLabFolderPath = '/app/Data'
        realPath = os.path.realpath(path)
        if not realPath.startswith(examplesFolderPath) and not realPath.startswith(aiLabFolderPath):
            raise Exception('Security Error: Invalid path: ' + realPath + '. Filepaths must reside within the examples folder if run locally or within the /app/Data folder if run from AI Lab')