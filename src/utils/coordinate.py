class Coordinate(object):
    """
    Class that contains useful properties and functions for coordinates

    ...

    Attributes
    ----------
    data : json object
        a json object representing the coordinate and having the following schema
        {
            "x": 0,
            "y": 0
        }
    """
    def __init__(self, data):
        if data is None:
            raise Exception("no data provided for the coordinate")
        if "y" not in data:
            raise Exception("the coordinate does not have an y value")
        if "x" not in data:
            raise Exception("the coordinate does not have an x value")
        
        self.x = data["x"]
        self.y = data["y"]

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