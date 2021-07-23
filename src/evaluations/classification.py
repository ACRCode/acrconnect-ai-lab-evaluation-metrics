from sklearn.metrics import confusion_matrix, accuracy_score, cohen_kappa_score, recall_score, classification_report, roc_auc_score, roc_curve
from utils.data import getDicomIndexDictionary, getValuesIndexDictionary
import numpy as np

def ClassificationEvaluation(groundTruths, predictions, rocInputs, threshold):
    """
    Calculates the classification evaluation

    Parameters
    ----------
    groundTruths : dictionary
        dictionary having granularity hash as keys and ground truths as values
    predictions : dictionary
        dictionary having granularity hash as keys and predictions as values
    rocInputs : dictionary
        inputs for the binary ROC curve metrics (AUC) containing Y_true and Y_score values
    threshold: float
        the threshold of the evaluation
    Returns
    -------
    json object
        The evaluation

    """
    studyIndexDictionary = getDicomIndexDictionary(groundTruths, predictions)
    valuesIndexDictionary = getValuesIndexDictionary(groundTruths, predictions)
    
    # arrays with the values only, no studyuids
    length = len(studyIndexDictionary.items())
    gts = [None] * length
    preds = [None] * length
    for studyId, gt in groundTruths.items():
        gts[studyIndexDictionary[studyId]] = valuesIndexDictionary[gt]
    for studyId, pred in predictions.items():
        preds[studyIndexDictionary[studyId]] = valuesIndexDictionary[pred]


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

    #if we have no valid studies to compare
    if len(gts) <= 0:
        return None

    metrics = {
        # calculate superficial metrics that only need normal y_true and y_pred
        # we do rot90 and fliplr to get the radiologist axis as the x axis and the model axis as the y axis
        "confusionMatrix": np.rot90(np.fliplr(confusion_matrix(gts, preds))).tolist(),
        "kappa": cohen_kappa_score(gts, preds),
        "accuracy": accuracy_score(gts, preds),
        "matrixValueOrders": valuesIndexDictionary,
        #stubs, we'll do these next
        "sensitivity": None,
        "specificity": None,
        "auc": None
    }

    # calculate AUC and ROC
    if "Binary_ROC" in rocInputs:
        #AUC
        rocInput = rocInputs["Binary_ROC"]
        auc = roc_auc_score(rocInput["expected"], rocInput["actual"])
        metrics["auc"] = auc
        #ROC curve
        fpr, tpr, thresholds = roc_curve(y_true=rocInput["expected"], y_score=rocInput["actual"], drop_intermediate=False)
        metrics["rocCurve"] = {
            "falsePositiveRate": fpr.tolist(),
            "truePositiveRate": tpr.tolist(),
            "thresholds": thresholds.tolist()
        }

    # calculate sensitivity and specificity
    # because of the nature of these metrics, we must have a binary classification
    # or we must simulate one
    #start with true binaries
    if len(valuesIndexDictionary.keys()) == 2 and '0' in valuesIndexDictionary.keys():
        #true binary data will have the positive case as label index 0 instead of 1
        #due to ACR requirements, so our sensitivity and specificity will be flipped
        metrics["sensitivity"] = recall_score(gts, preds, pos_label=0)
        metrics["specificity"] = recall_score(gts, preds)
    #simulated binary, use the roc inputs
    elif "Binary_ROC" in rocInputs:
        rocInput = rocInputs["Binary_ROC"]
        binaryTruths = rocInput["expected"]
        binaryPreds = [1 if x >= threshold else 0 for x in rocInput["actual"]]
        metrics["specificity"] = recall_score(binaryTruths, binaryPreds, pos_label=0)
        metrics["sensitivity"] = recall_score(binaryTruths, binaryPreds)
    #otherwise rely on sklearn averaging
    else:
        metrics["specificity"] = recall_score(gts, preds, pos_label=0, average='macro')
        metrics["sensitivity"] = recall_score(gts, preds, average='macro')

    evaluation = {
        "generalMetrics": metrics
    }
    return evaluation
