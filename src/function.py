import boto3
import json

from factories.clasification import ClassificationEvaluationFactory
from factories.continuous import ContinuousEvaluationFactory
from factories.boundingBox import BoundingBoxEvaluationFactory
from factories.segmentation import SegmentationEvaluationFactory
from utils.binaryMap import BinaryClassificationMap


def lambda_handler(event, context):

    print('doing evaluation with event', event)

    datasetFileKey = event['datasetFileKey']
    outputFileKey = event['outputFileKey']
    bucket = event['bucket']
    binary_maps = None if 'binary_maps' not in event else event['binary_maps']
    threshold = 0.3 if 'threshold' not in event else ['threshold']

    s3 = boto3.resource('s3',region_name='us-east-1')
    
    datasetS3obj = s3.Object(bucket,datasetFileKey)
    datasetData = datasetS3obj.get()['Body'].read()
    dataset = json.loads(datasetData)
    
    outputS3obj = s3.Object(bucket,outputFileKey)
    outputData = outputS3obj.get()['Body'].read()
    output = json.loads(outputData)

    binaryMaps = None if binary_maps is None else {k:BinaryClassificationMap(v["presentLabels"], v["absentLabels"]) for (k,v) in binary_maps.items()}
    classificationFactory = ClassificationEvaluationFactory(dataset, output, threshold, binaryMaps)
    continuousFactory = ContinuousEvaluationFactory(dataset, output)
    boundingBoxFactory = BoundingBoxEvaluationFactory(dataset, output, None)
    segmentationFactory = SegmentationEvaluationFactory(dataset, output)


    evaluation = {
        "classification": classificationFactory.Create(),
        "continuous": continuousFactory.Create(),
        "boundingBox": boundingBoxFactory.Create(),
        "segmentation": segmentationFactory.Create()
    }

    print('calculated evaluation as ', evaluation)

    return evaluation
    

if __name__ == "__main__":
    event = {
        'datasetFileKey': 'job1/input/dataset.json',
        'outputFileKey': 'job1/output/output.json',
        'bucket': 'testailab',
        'binary_maps': None,
        'threshold': 0.3
    }
    context = []
    lambda_handler(event, context)