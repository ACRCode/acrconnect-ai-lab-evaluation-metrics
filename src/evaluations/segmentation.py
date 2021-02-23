
from utils.data import getDicomIndexDictionary, getValuesIndexDictionary

def SegmentationEvaluation(groundTruths, predictions):
    """
    Calculates the segmentation evaluation

    Parameters
    ----------
    groundTruths : dictionary
        dictionary having study instance uids as keys and an array of segmentations as values
    predictions : dictionary
        dictionary having study instance uids as keys and an array of segmentations as values
    Returns
    -------
    json object
        The evaluation

    """

    studyIndexDictionary = getDicomIndexDictionary(groundTruths, predictions)
    
    # arrays with the values only, no studyuids
    length = len(studyIndexDictionary.items())
    gts = [None] * length
    preds = [None] * length
    for studyId, gt in groundTruths.items():
        gts[studyIndexDictionary[studyId]] = gt
    for studyId, pred in predictions.items():
        preds[studyIndexDictionary[studyId]] = pred
    # in case we nave None in any of our array elements, we have to remove those indeces from both arrays
    gtsClean = []
    predsClean = []
    for i in range(length):
        if gts[i] is None or preds[i] is None:
            continue
        gtsClean.append(gts[i])
        predsClean.append(preds[i])
    gts = gtsClean
    preds = predsClean
    
    metrics = {
        "meanDiceCoefficient": None,
        "meanAveragePrecision": None,
        "meanIntersectionOverUnion": None,
        "scatterPlot": {
            "data": None
        } 
    }
    return metrics
