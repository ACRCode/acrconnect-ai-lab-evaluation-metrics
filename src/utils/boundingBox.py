from collections import namedtuple

from .coordinate import Coordinate

class BoundingBox(object):

    def __init__(self, data):
        if data is None:
            raise Exception("no data provided for the bounding box")
        if "top_left_hand_corner" not in data:
            raise Exception("data does not have a top_left_hand_corner field")
        if "bottom_right_hand_corner" not in data:
            raise Exception("data does not have a bottom_right_hand_corner field")

        self.topLeft = Coordinate(data["top_left_hand_corner"])
        self.bottomRight = Coordinate(data["bottom_right_hand_corner"])

    def __str__(self):
        return "<{0} - {1}>".format(self.topLeft, self.bottomRight)

    def __repr__(self):
        return "<{0} - {1}>".format(self.topLeft, self.bottomRight)
        
    def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.topLeft == other.topLeft) and (self.bottomRight == other.bottomRight))
        else:
            return False
            
    def __ne__(self, other):
        return (not self.__eq__(other))
            
    def __hash__(self):
        return hash(self.__str__())

    def getArea(self):
        """
        Calculates the area of this bounding box

        Returns
        -------
        float
            The area

        """
        # add + 1 to dimensions to account for pixel coordinates
        return (self.bottomRight.x - self.topLeft.x + 1) * (self.bottomRight.y - self.topLeft.y + 1)


    def getIoU(self, other):
        """
        Calculates the intersection over union of this bounding box and another

        Parameters
        ----------
        other : BoundingBox
            the other bounding box to get the iou with
        Returns
        -------
        float
            The iou

        """
        if other is None:
            return 0
        
        # determine the (x, y)-coordinates of the intersection rectangle
        topLeftX = max(self.topLeft.x, other.topLeft.x)
        topLeftY = max(self.topLeft.y, other.topLeft.y)
        bottomRightX = max(self.bottomRight.x, other.bottomRight.x)
        bottomRightY = max(self.bottomRight.y, other.bottomRight.y)

        # make sure that the boxes intersect
        if bottomRightX < topLeftX or bottomRightY < topLeftY:
            return 0
            
        # compute the area of intersection rectangle
        # add + 1 to dimensions to account for pixel coordinates
        interArea = (bottomRightX - topLeftX + 1) * (bottomRightY - topLeftY + 1)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / (self.getArea() + other.getArea() - interArea)
        return iou
