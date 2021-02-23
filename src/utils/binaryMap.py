
class BinaryClassificationMap:
    """
    A class that represents a binary classification map and provides useful functions for maping labels

    ...

    Attributes
    ----------
    presentLabels : array
        array of strings specifying the labels that should be mapped to the positive label
    absentLabels : array
        array of strings specifying the labels that should be mapped to the negative label

    """
    
    def __init__(self, presentLabels, absentLabels):
        self.map = {}
        for label in presentLabels:
            self.map[label] = "1"
        for label in absentLabels:
            self.map[label] = "0"

    def mapLabel(self, label):
        """
        Maps a prediction label to the corresponding positive/negative label according to this map

        Parameters
        ----------
        label : string
            the prediction label to map
        Returns
        -------
        string
            The mapped label being a value of either "1" or "0"

        """
        if label not in self.map:
            return label

        return self.map[label]

    def getSiblingLabels(self, label):
        """
        Obtains an array with all the label values that have been mapped to the same binary value as the passed label

        Parameters
        ----------
        label : string
            the prediction label
        Returns
        -------
        array
            The prediction labels that correspond to the same binary value

        """
        if label not in self.map:
            return []

        siblings = []

        mappedLabel = self.mapLabel(label)
        for mapKey in self.map.keys():
            if self.map[mapKey] == mappedLabel:
                siblings.append(mapKey)

        return siblings


