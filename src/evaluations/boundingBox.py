
from utils.data import getStudyIndexDictionary, getValuesIndexDictionary
from utils.boundingBox import BoundingBox

def BoundingBoxEvaluation(groundTruths, predictions):
    """
    Calculates the bounding box evaluation

    Parameters
    ----------
    groundTruths : dictionary
        dictionary having study instance uids as keys and an array of bounding boxes as values
    predictions : dictionary
        dictionary having study instance uids as keys and an array of bounding boxes as values
    Returns
    -------
    json object
        The evaluation

    """

    studyIndexDictionary = getStudyIndexDictionary(groundTruths, predictions)
    
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
        #also create our bounding box objects here
        gtsClean.append([BoundingBox(gt) for gt in gts[i]])
        predsClean.append([BoundingBox(pred) for pred in preds[i]])
    gts = gtsClean
    preds = predsClean

    print(gts)
    print(preds)

    
    metrics = {
        "meanDiceCoefficient": getMeanDiceCoefficient(gts, preds),
        "meanAveragePrecision": getMeanAveragePrecision(gts, preds),
        "meanIntersectionOverUnion": getMeanIntersectionOverUnion(gts, preds),
        "scatterPlot": getScatterPlot(gts, preds)
    }
    return metrics

def getScatterPlot(gts, preds):
    # Steps for calculation:
    # 1. Plot sum of ground truth area vs. sum of predicted area
    # 2. No need to 'match' ground truth boxes to predicted boxes in this instance
    # 3. Do not plot true negatives (ground truth is absent AND prediction is absent). Plot everything else
    # 4. Units should be in pixels
    plot = []
    for i in range(len(gts)):
        gtBoxes = gts[i]
        predBoxes = preds[i]
        if len(gtBoxes) <= 0 and len(predBoxes <= 0): # true negatives
            continue
        gtSum = 0 if len(gtBoxes) <= 0 else sum(box.getArea() for box in gtBoxes)
        predSum = 0 if len(predBoxes) <= 0 else sum(box.getArea() for box in predBoxes)
        plot.append([gtSum, predSum])
    return plot

def getMeanDiceCoefficient(gts, preds):
    return 0

def getMeanAveragePrecision(gts, preds):
    return 0

def getMeanIntersectionOverUnion(gts, preds):
    return 0