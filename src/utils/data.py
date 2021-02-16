import hashlib

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

    # for true binary cases, we want to see the positive label first on the confusion matrix
    # so we use this flag to determine the sorting order
    isTrueBinary = len(union) == 2 and "0" in union

    union.sort(reverse=isTrueBinary)
    dict = {key:index for index, key in enumerate(union)}
    return dict

def hashGranularityIdentifier(studyInstanceUid='', seriesInstanceUid='', sopInstanceUid='', frameIndex='', hashes=None):
    """
    Creates a hash value of the identifying information for the granularity of a data object.
    This will use MD5 to encode the concatenated values and return a hex representation of the resulting bytes
    
    Parameters
    ----------
    studyInstanceUid : string
        study instance uid
    seriesInstanceUid : string
        series instance uid
    sopInstanceUid : string
        SOP instance uid
    frameIndex : string
        frame index
    hashes : dictionary
        optional dictionary to save a mapping of the hashed values for reverse lookups
    """
    concat = "{0}:{1}:{2}:{3}".format(studyInstanceUid, seriesInstanceUid, sopInstanceUid, frameIndex)
    hash_object = hashlib.md5(concat.encode())
    hash = hash_object.hexdigest()
    if hashes is not None:
        hashes[hash] = {
            "studyInstanceUid": studyInstanceUid,
            "seriesInstanceUid": seriesInstanceUid,
            "sopInstanceUid": sopInstanceUid,
            "frameIndex": frameIndex,
        }
    return hash

