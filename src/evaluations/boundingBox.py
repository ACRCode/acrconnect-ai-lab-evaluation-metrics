
from utils.data import getStudyIndexDictionary, getValuesIndexDictionary
from utils.boundingBox import BoundingBox
import numpy as np


def BoundingBoxEvaluation(groundTruths, predictions, threshold):
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
    
    # calculate the metrics that aggregate the bounding box areas as one total area
    # (meanDiceCoefficient, scatterPlot, and meanIntersectionOverUnion)
    dices = []
    ious = []
    scatterPlot = []
    for i in range(len(gts)):
        gtBoxes = gts[i]
        predBoxes = preds[i]

        #get the dimensions of our area maps
        maxX = max(box.bottomRight.x for box in (gtBoxes + predBoxes)) + 1
        maxY = max(box.topLeft.y     for box in (gtBoxes + predBoxes)) + 1

        # cook our area maps with the areas of our boxes
        gtMap   = np.zeros((maxY, maxX), dtype=np.int)
        predMap = np.zeros((maxY, maxX), dtype=np.int)
        # +1 accounts for pixel space
        for box in gtBoxes:
            gtMap  [box.topLeft.y:box.bottomRight.y + 1, box.topLeft.x:box.bottomRight.x + 1] = 1
        for box in predBoxes:
            predMap[box.topLeft.y:box.bottomRight.y + 1, box.topLeft.x:box.bottomRight.x + 1] = 1

        # get the areas
        gtArea   = gtMap.sum()
        predArea = predMap.sum()

        # get the intersection
        intersectionMap = np.bitwise_and(gtMap, predMap)
        intersectionArea = intersectionMap.sum()

        # get the union
        unionMap = np.bitwise_or(gtMap, predMap)
        unionArea = unionMap.sum()

        # get the dice
        diceCoefficient = (2 * intersectionArea) / (gtArea + predArea)
        dices.append(diceCoefficient)

        #get the iou
        iou = intersectionArea / unionArea
        ious.append(iou)

        #add to scatter plot
        if len(gtBoxes) > 0 or len(predBoxes) > 0: # don't plot true negatives
            scatterPlot.append([gtArea.item(), predArea.item()])


    metrics = {
        "meanDiceCoefficient": np.mean(np.array(dices)),
        "meanAveragePrecision": getMeanAveragePrecision(gts, preds),
        "meanIntersectionOverUnion": np.mean(np.array(ious)),
        "scatterPlot": {
            "data": scatterPlot
        } 
    }
    return metrics

def getMeanAveragePrecision(gts, preds, threshold=0.5):
    averagePrecisions = []
    for i in range(len(gts)):
        tps = 0
        fps = 0
        fns = 0

        # A false negative indicates a ground truth object had no associated predicted object
        if(preds[i] is None or len(preds[i]) <= 0):
            fns += len(gts[i])
            continue

        for gtBox in gts[i]:
            # A true positive is counted when a single predicted object matches a ground truth object with an IoU above the threshold
            if any((gtBox.getIoU(predBox) > threshold) for predBox in preds[i]):
                tps += 1
                continue
            # A false positive indicates a predicted object had no associated ground truth object
            else:
                fps += 1
                continue

        precision = tps / (tps + fps)
        averagePrecision = precision / len(gts[i])
        averagePrecisions.append(averagePrecision)
    return np.mean(np.array(averagePrecisions))