import boto3
from botocore.client import Config
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

    config = Config(connect_timeout=5, retries={'max_attempts': 0})
    s3 = boto3.client('s3', config=config)
    

    
    # print('printing test output from boto3')
    # response = s3.list_objects_v2(Bucket=bucket)
    # files = response.get("Contents")
    # for file in files:
    #     print(f"file_name: {file['Key']}, size: {file['Size']}")


    print('loading dataset...')
    datasetresponse = s3.get_object(Bucket=bucket,Key=datasetFileKey)
    print('got response', datasetresponse)
    datasetresponsefile=datasetresponse['Body'].read().decode('utf-8')
    datasetresponsefile=str(datasetresponsefile)
    dataset = json.loads(datasetresponsefile)
    print('dataset loaded')

    print('loading output...')
    outputresponse = s3.get_object(Bucket=bucket,Key=outputFileKey)
    print('got response', outputresponse)
    outputresponsefile=outputresponse['Body'].read().decode('utf-8')
    outputresponsefile=str(outputresponsefile)
    output = json.loads(outputresponsefile)
    print('output loaded')

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