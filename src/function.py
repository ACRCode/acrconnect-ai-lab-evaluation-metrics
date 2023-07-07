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
    threshold = 0.3 if 'threshold' not in event else event['threshold']

    s3 = boto3.resource('s3')

    print('bucket', bucket)
    print('datasetFileKey', datasetFileKey)
    
    print('loading dataset...')
    response = s3.get_object(Bucket=bucket,Key=datasetFileKey)
    print('got response', response)
    responsefile=response['Body'].read().decode('utf-8')
    responsefile=str(responsefile)
    print('responsefile', responsefile)

    datasetS3obj = s3.Object(bucket,datasetFileKey)
    print('got object', datasetS3obj)
    datasetDataBody = datasetS3obj.get()['Body']
    print('got body', datasetDataBody)
    datasetData = datasetDataBody.read()
    print('got data', datasetData)
    dataset = json.loads(datasetData)
    print('loading dataset...')

    print('loading output...')
    outputS3obj = s3.Object(bucket,outputFileKey)
    outputData = outputS3obj.get()['Body'].read()
    output = json.loads(outputData)
    print('output loaded...')


    binaryMaps = None if binary_maps is None else {k:BinaryClassificationMap(v["presentLabels"], v["absentLabels"]) for (k,v) in binary_maps.items()}
    classificationFactory = ClassificationEvaluationFactory(dataset, output, threshold, binaryMaps)
    continuousFactory = ContinuousEvaluationFactory(dataset, output)
    boundingBoxFactory = BoundingBoxEvaluationFactory(dataset, output, None)
    segmentationFactory = SegmentationEvaluationFactory(dataset, output)

    print('created evaluation factories')

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
        'datasetFileKey': 'jobs/b1db0661-6f91-4d94-a46f-dc0180f901e6/input/dataset.json',
        'outputFileKey': 'jobs/b1db0661-6f91-4d94-a46f-dc0180f901e6/output/output.json',
        'bucket': 'acr-ailab-dev-io-lambda',
        'binary_maps': {'breast-density-classification': {'presentLabels': ['1', '2'], 'absentLabels': ['3', '4']}},
        'threshold': 0.3
    }
    context = []
    lambda_handler(event, context)