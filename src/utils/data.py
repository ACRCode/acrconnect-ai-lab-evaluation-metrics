

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