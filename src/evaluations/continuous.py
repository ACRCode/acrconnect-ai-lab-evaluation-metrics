from sklearn.metrics import mean_squared_error, mean_absolute_error
from utils.data import getDicomIndexDictionary, getValuesIndexDictionary

def ContinuousEvaluation(key, allGroundTruths, predictions):
    """
    Calculates the continuous evaluation

    Parameters
    ----------
    keys: string
        the base key for this evaluation
    allGroundTruths : dictionary
        dictionary having prediction labels as keys and ground truth dictionaries as values (study instance uids as keys and ground truths as values)
    predictions : dictionary
        dictionary having study instance uids as keys and predictions as values

    Returns
    -------
    json object
        The evaluation

    """
    if allGroundTruths is None or predictions is None:
        return None

    meanSquaredError = 0
    meanAbsoluteError = 0
    plots = []

    # we must scatter plot our predictions against every input key
    for gtKey in allGroundTruths:
        groundTruths = allGroundTruths[gtKey]
        studyIndexDictionary = getDicomIndexDictionary(groundTruths, predictions)
        
        # arrays with the values only, no studyuids
        gts = [None] * len(studyIndexDictionary.items())
        preds = [None] * len(studyIndexDictionary.items())
        for studyId, gt in groundTruths.items():
            gts[studyIndexDictionary[studyId]] = gt
        for studyId, pred in predictions.items():
            preds[studyIndexDictionary[studyId]] = pred

        plotData = []
        for i in list(map(lambda x: studyIndexDictionary[x], studyIndexDictionary.keys())):
            if gts[i] is None or preds[i] is None:
                continue
            plotData.append([gts[i], preds[i]])
        
        # calculate our mse and mae only if these ground truths match our target evaluation key
        # otherwise the metrics don't make much sense if the gts and preds belong to different keys
        if gtKey == key:
            meanSquaredError = mean_squared_error(gts, preds)
            meanAbsoluteError = mean_absolute_error(gts, preds)


        plot = {
            "name": gtKey,
            "data": plotData
        }
        plots.append(plot)

    evaluation = {
        "meanSquaredError": meanSquaredError,
        "meanAbsoluteError": meanAbsoluteError,
        "scatterPlot": plots
    }
    return evaluation
