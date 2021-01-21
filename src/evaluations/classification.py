from sklearn.metrics import confusion_matrix, accuracy_score, cohen_kappa_score, recall_score, classification_report, roc_auc_score

def ClassificationEvaluation(groundTruths, predictions, rocInputs, threshold):
    """
    Calculates the classification evaluation

    Parameters
    ----------
    groundTruths : dictionary
        dictionary having study instance uids as keys and ground truths as values
    predictions : dictionary
        dictionary having study instance uids as keys and predictions as values
    rocInputs : dictionary
        inputs for the binary ROC curve metrics (AUC) containing Y_true and Y_score values
    threshold: float
        the threshold of the evaluation
    Returns
    -------
    json object
        The evaluation

    """
    studyIndexDictionary = getStudyIndexDictionary(groundTruths, predictions)
    valuesIndexDictionary = getValuesIndexDictionary(groundTruths, predictions)

    # arrays with the values only, no studyuids
    gts = [None] * len(studyIndexDictionary.items())
    preds = [None] * len(studyIndexDictionary.items())
    for studyId, gt in groundTruths.items():
        gts[studyIndexDictionary[studyId]] = valuesIndexDictionary[gt]
    for studyId, pred in predictions.items():
        preds[studyIndexDictionary[studyId]] = valuesIndexDictionary[pred]


    metrics = {
        # calculate superficial metrics that only need normal y_true and y_pred
        "confusionMatrix": confusion_matrix(gts, preds).tolist(),
        "kappa": cohen_kappa_score(gts, preds),
        "accuracy": accuracy_score(gts, preds),
        "matrixValueOrders": valuesIndexDictionary,
        #stubs, we'll do these next
        "sensitivity": None,
        "specificity": None,
        "auc": None
    }

    # calculate AUC
    if "Binary_ROC" in rocInputs:
        rocInput = rocInputs["Binary_ROC"]
        auc = roc_auc_score(rocInput["expected"], rocInput["actual"])
        metrics["auc"] = auc


    # calculate sensitivity and specificity
    # because of the nature of these metrics, we must have a binary classification
    # or we must simulate one
    #start with true binaries
    if len(valuesIndexDictionary.keys()) == 2 and '0' in valuesIndexDictionary.keys():
        metrics["specificity"] = recall_score(gts, preds, pos_label=0)
        metrics["sensitivity"] = recall_score(gts, preds)
    #simulated binary, use the roc inputs
    elif "Binary_ROC" in rocInputs:
        rocInput = rocInputs["Binary_ROC"]
        binaryTruths = rocInput["expected"]
        binaryPreds = [1 if x >= threshold else 0 for x in rocInput["actual"]]
        print(len(gts))
        print(len(binaryPreds))
        print("binaryPreds", binaryPreds)
        print("binaryTruths", binaryTruths)
        print("rocInput['actual']", rocInput["actual"])
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



def getStudyIndexDictionary(groundTruths, predictions):
    """
    creates an index dictionary for our study ids so that we can correctly match ground truths and predictions
    useful in case our studies are out of order between the ground truths and the predictions
    so we can have the correct gt and prediction side to side on the final int arrays
    i.e enumerates study instance uids
    """
    gtKeys = list(groundTruths.keys())
    predKeys = list(predictions.keys())
    union = list(set().union(gtKeys, predKeys))
    dict = {key:index for index, key in enumerate(union)}
    return dict


def getValuesIndexDictionary(groundTruths, predictions):
    """
    Will crate an enumeration of all possible prediction values assigning an integer index 
    so that all matrix values can correspond to a range between 0 and some other higher integer.
    """
    gtValues = list(groundTruths.values())
    predValues = list(predictions.values())
    union = list(set().union(gtValues, predValues))
    union.sort()
    dict = {key:index for index, key in enumerate(union)}
    return dict