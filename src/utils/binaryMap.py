
class BinaryClassificationMap:
    
    def __init__(self, presentLabels, absentLabels):
        self.map = {}
        for label in presentLabels:
            self.map[label] = "1"
        for label in absentLabels:
            self.map[label] = "0"

    def mapLabel(self, label):
        if label not in self.map:
            return label

        return self.map[label]

    def getSiblingLabels(self, label):
        if label not in self.map:
            return []

        siblings = []

        mappedLabel = self.mapLabel(label)
        for mapKey in self.map.keys():
            if self.map[mapKey] == mappedLabel:
                siblings.append(mapKey)

        return siblings


