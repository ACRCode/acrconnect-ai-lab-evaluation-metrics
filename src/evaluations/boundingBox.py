
from utils.data import getDicomIndexDictionary, getValuesIndexDictionary
from utils.boundingBox import BoundingBox
import numpy as np

import time

def st_time(func):
    """
        st decorator to calculate the total time of a func
    """

    def st_func(*args, **keyArgs):
        t1 = time.time()
        r = func(*args, **keyArgs)
        t2 = time.time()
        print("Function=%s, Time=%s" % (func.__name__, t2 - t1))
        return r

    return st_func

def BoundingBoxEvaluation(key, groundTruths, predictions, previousEvaluation):
    """
    Calculates the bounding box evaluation

    Parameters
    ----------
    groundTruths : dictionary
        dictionary having granularity hash as keys and an array of bounding boxes as values
    predictions : dictionary
        dictionary having granularity hash as keys and an array of bounding boxes as values
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

    # in case we nave None in any of our array elements
    gtsClean = []
    predsClean = []
    for i in range(length):
        
        #to account for the one-to-many relationships of ground truth and prediction granularity levels
        #we can simply flatten the array of arrays of predicted boxes to get the aggregated array of all boxes predicted for the ground truth level
        predBoxes = [box for predBoxes in ([] if preds[i] is None else preds[i]) for box in predBoxes]

        #exclude true negatives from calculations
        if (gts[i] is None or len(gts[i]) == 0) and (preds[i] is None or len(predBoxes) == 0):
            continue

        if gts[i] is None:
            gtsClean.append([])
        else:
            gtsClean.append([BoundingBox.fromJsonData(gt) for gt in gts[i]])

        if predBoxes is None or len(predBoxes) <= 0:
            predsClean.append([])
        else:
            predsClean.append([BoundingBox.fromJsonData(pred) for pred in predBoxes])

    gts = gtsClean
    preds = predsClean
    
    #if we have no valid studies to compare
    if len(gts) <= 0:
        return None
    
    metrics = {
        "meanAveragePrecision": getMeanAveragePrecision(gts, preds)
    }

    if previousEvaluation is not None:
        metrics["meanDiceCoefficient"] = previousEvaluation["meanDiceCoefficient"]
        metrics["meanIntersectionOverUnion"] = previousEvaluation["meanIntersectionOverUnion"]
        metrics["scatterPlot"] = previousEvaluation["scatterPlot"]
    else:
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
            maxY = max(box.bottomRight.y for box in (gtBoxes + predBoxes)) + 1

            # cook our area maps with the areas of our boxes
            gtMap   = np.zeros((maxY, maxX), dtype=int)
            predMap = np.zeros((maxY, maxX), dtype=int)
            # +1 accounts for pixel space
            for box in gtBoxes:
                gtMap  [box.topLeft.y:box.bottomRight.y + 1, box.topLeft.x:box.bottomRight.x + 1] = 1
            for box in predBoxes:
                predMap[box.topLeft.y:box.bottomRight.y + 1, box.topLeft.x:box.bottomRight.x + 1] = 1

            # get the areas
            gtArea   = gtMap.sum()
            predArea = predMap.sum()

            #exclude any cases where there is no ground truth or prediction areas
            #this is usually indicative of bad data where the bottom right corner is not south and east of the top left corner
            #inclusion of these will cause N/A values for our IOU and mean dice calculations
            if(gtArea + predArea <= 0):
                continue

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

        metrics["meanDiceCoefficient"] = np.mean(np.array(dices))
        metrics["meanIntersectionOverUnion"] = np.mean(np.array(ious))
        metrics["scatterPlot"] = {
            "data": scatterPlot,
            "name": key
        } 

    return metrics

def getMeanAveragePrecision(gts, preds):
    """
    Calculates the  mean of the average precision for each study in the ground truth and predictions

    Parameters
    ----------
    gts : array
        an array with each element containing an array of bounding boxes that correspond to the ground truth of a single study
    preds : array
        an array with each element containing an array of bounding boxes that correspond to the output of a single study
    Returns
    -------
    float
        The mean average precision

    """
    averagePrecisions = []

    thresholds = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]

    for i in range(len(gts)):

        averagePrecision = 0
        for threshold in thresholds:

            tps = 0
            fps = 0
            fns = 0

            matchedPredBoxes = []
            for gtBox in gts[i]:

                # iterate through the non-matched prediction boxes and get the best match
                highestMatchedIoU = None
                matchedPredBox = None
                for predBox in (diff(preds[i], matchedPredBoxes)): 
                    IoU = gtBox.getIoU(predBox)
                    if IoU > threshold and (highestMatchedIoU is None or IoU > highestMatchedIoU):
                        highestMatchedIoU = IoU
                        matchedPredBox = predBox

                # A false negative indicates a ground truth object had no associated predicted object
                if highestMatchedIoU is None or matchedPredBox is None:
                    fns += 1

                # A true positive is counted when a single predicted object matches a ground truth object with an IoU above the threshold
                else:
                    tps += 1
                    matchedPredBoxes.append(matchedPredBox)

            # A false positive indicates a predicted object had no associated ground truth object
            fps += len(diff(preds[i], matchedPredBoxes))

            if tps + fps == 0: # avoid division by 0
                precision = 0
            else:
                precision = tps / (tps + fps)

            averagePrecision += precision / len(thresholds)

        averagePrecisions.append(averagePrecision)
    return np.mean(np.array(averagePrecisions))

def diff(li1, li2):
    """
    Finds the difference of two lists
    """
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif