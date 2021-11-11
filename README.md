ACRConnect AI-LAB Evaluation Metrics
====

Calculate performance metrics for machine learning algorithms for medical imaging according to [AI-LAB Evaluation Standards](https://github.com/ACRCode/AILAB_documentation/wiki/AILAB-Evaluation-Standards).

Features
--------
* Provides metrics analysis for machine learning models for classification, bounding box, continuous, and segmentation use cases
* Provides information on unknown and failed study results on the final predictions

General Usage
-----

    $ python src/main.py \
        --dataset_file_path="/path/to/dataset.json" \
        --output_file_path="/path/to/output.json"

### Required Arguments
- `--dataset_file_path`: Specifies the path of the json file containing the ground truths.
- `--output_file_path`: Specifies the path of the json file containing the predictions. This file should follow the [AI-LAB Output JSON Standard](https://github.com/ACRCode/AILAB_documentation/wiki/AILAB-Output-JSON-Standards)

### Optional Arguments
- `--evaluation_file_path`: Specifies the path where the evaluation json should be saved. If this is not provided, the json will simply be printed to the console.
- `--threshold`: The threshold to use for the evaluation for binary classification. Should be a value between 0 and 1. The default threshold is 0.5

## Binary Maps

Classification use cases have several metrics that require the predictions and ground truths to be in a true binary form (that is the only two possible prediction labels being "0" and some other label). These metrics are specificity, sensitivity, and AUC score. In order to allow non-binary use cases to calculate these metrics, a binary mapping can be provided to the evaluation scripts as a way to create pseudo-binary data from which these metrics can be calculated

    $ python src/main.py \
        --dataset_file_path="/path/to/dataset.json" \
        --output_file_path="/path/to/output.json" \
        --evaluation_file_path="/path/to/evaluation.json" \
        --binary_maps="{\"classificationKey\": {\"presentLabels\":[\"1\", \"2\"], \"absentLabels\":[\"3\", \"4\"]}}"

The binary maps must be a dictionary containing the annotation class key/slug as the element key and a value of a binary map in the form:

```javascript
{
    //The annotation class key/slug that this map will be related to
    "classificationKey": {

        //An array of strings representing the prediction labels that will be associated with the "positive/present" prediction label of "1"
        "presentLabels": ["1", "2"], 

        //An array of strings representing the prediction labels that will be associated with the "negative/absent" prediction label of "0"
        "absentLabels": ["3", "4"]
    }
}
```


Dataset JSON
--------
The following json schema is used by the scripts to process the dataset on the json file specified by the `--dataset_file_path` argument

```javascript
[
    {
        "studyInstanceUid": "0.0.000.000000.0.00.0000000000.00000000000000000.00000",
        "annotationData": annotationData,
        "series": [
            {
                "seriesInstanceUid": "0.0.000.000000.0.00.0000000000.00000000000000000.00000",
                "annotationData": annotationData,
                "instances": [
                    {
                        "sopInstanceUid": "0.0.000.000000.0.00.0000000000.00000000000000000.00000",
                        "annotationData": annotationData,
                        "frames": [
                            {
                                "frameIndex": 1,
                                "annotationData": annotationData
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```

For each level of annotation (study->series->instance->frame) a property called `annotationData` accepts annotation objects with the following schema 

```javascript
{
    "classification": [
        {
            "key": "annotationKey",

            //value type is string
            "value": "1"
        }
    ],
    "boundingBox": [
        {
            "key": "annotationKey",

            //value type is array of bounding boxes
            "value" : [
                {
                    "bottom_right_hand_corner": {
                        "x": 0,
                        "y": 0
                    },
                    "top_left_hand_corner": {
                        "x": 0,
                        "y": 0
                    }
                }
            ]
        }
    ],
    "continuous":[
        {
            "key": "annotationKey",

            //value type is float
            "value": 0.0
        }
    ],
    "segmentation":[
        {
            "key": "annotationKey",

            //value type is object
            "value": {}
        }
    ]
}
```

Output JSON
--------
For the output json schema used by the `--output_file_path` please see the [AI-LAB Output JSON Standards](https://github.com/ACRCode/AILAB_documentation/wiki/AILAB-Output-JSON-Standards)
