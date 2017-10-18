class LocationVector:
    def __init__(self, *locations):
        self.locations = locations

    def is_comparable(self, other):
        for location, otherlocation in self.locations, other.locations:
            if location != '*' and otherlocation != '*' and location != otherlocation:
                return False
        return True

    def __eq__(self, other):
        if self.is_comparable(other):
            return self.locations == other.locations
        else:
            return None

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        if self.is_comparable(other):
            for location, otherlocation in self.locations, other.locations:
                if location == '*' and otherlocation != '*':
                    return False
            return True
        else:
            return False

    def __ge__(self, other):
        return other <= self

    def __lt__(self, other):
        reverse_result = self >= other
        if reverse_result is None:
            return None
        else:
            return not reverse_result

    def __gt__(self, other):
        reverse_result = self <= other
        if reverse_result is None:
            return None
        else:
            return not reverse_result