class Coordinate(object):
    """
    Class that contains useful properties and functions for coordinates

    ...

    Attributes
    ----------
    x : number
        the x value
    y : number
        the y value
    """
    def __init__(self, x, y):
        if x is None:
            raise Exception("no x coordinate provided for the coordinate")
        if y is None:
            raise Exception("no y coordinate provided for the coordinate")
        
        self.x = x
        self.y = y
        
    @classmethod
    def fromJsonData(cls, data):
        """
        Builds a coordinate from json data

        Parameters
        ----------
        data : json object
            a json object representing the coordinate and having the following schema
            {
                "x": 0,
                "y": 0
            }
        Returns
        -------
        Coordinate
            The coordinate
        """
        if data is None:
            raise Exception("no data provided for the coordinate")
        if "y" not in data:
            raise Exception("the coordinate does not have an y value")
        if "x" not in data:
            raise Exception("the coordinate does not have an x value")
        return cls(data["x"], data["y"])

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.x == other.x) and (self.y == other.y))
        else:
            return False
            
    def __ne__(self, other):
        return (not self.__eq__(other))
            
    def __hash__(self):
        return hash(self.__str__())