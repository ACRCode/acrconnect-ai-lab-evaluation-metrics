from collections import namedtuple

from .coordinate import Coordinate

class BoundingBox(object):
    """
    Class that contains useful properties and functions for bounding boxes

    ...

    Attributes
    ----------
    topLeft : Coordinate
        the top left coordinate
    bottomRight : Coordinate
        the bottom right coordinate
    """

    def __init__(self, topLeft, bottomRight):
        if topLeft is None:
            raise Exception("no top left coordinate provided for the bounding box")
        if bottomRight is None:
            raise Exception("no top left coordinate provided for the bounding box")
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        
    @classmethod
    def fromJsonData(cls, data):
        """
        Builds a bounding box from json data

        Parameters
        ----------
        data : json object
            a json object representing the bounding box and having the following schema
            {
                "bottom_right_hand_corner": {
                    "x": 0,
                    "y": 0
                },
                "top_left_hand_corner": {
                    "x": 0,
                    "y": 0
                }
            }
        Returns
        -------
        BoundingBox
            The bounding box
        """
        if data is None:
            raise Exception("no data provided for the bounding box")
        if "top_left_hand_corner" not in data:
            raise Exception("data does not have a top_left_hand_corner field")
        if "bottom_right_hand_corner" not in data:
            raise Exception("data does not have a bottom_right_hand_corner field")

        return cls(Coordinate.fromJsonData(data["top_left_hand_corner"]), Coordinate.fromJsonData(data["bottom_right_hand_corner"]))


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

    def getIntersection(self, other):
        """
        Calculates the intersection of this box and another box

        Parameters
        ----------
        other : BoundingBox
            the other bounding box to get the intersection
        Returns
        -------
        BoundingBox
            The intersecting box if there is an intersection, None otherwise

        """
        if other is None:
            return None
        
        # determine the (x, y)-coordinates of the intersection rectangle
        topLeftX = max(self.topLeft.x, other.topLeft.x)
        topLeftY = max(self.topLeft.y, other.topLeft.y)
        bottomRightX = min(self.bottomRight.x, other.bottomRight.x)
        bottomRightY = min(self.bottomRight.y, other.bottomRight.y)

        # make sure that the boxes intersect
        if bottomRightX < topLeftX or bottomRightY < topLeftY:
            return None

        return BoundingBox(Coordinate(topLeftX, topLeftY), Coordinate(bottomRightX, bottomRightY))

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

        interBox = self.getIntersection(other)
        if interBox is None:
            return 0

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interBox.getArea() / (self.getArea() + other.getArea() - interBox.getArea() )
        return iou
