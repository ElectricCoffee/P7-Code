class LocationVector(list):
    def __le__(self, other):
            for location, otherlocation in self, other:
                if otherlocation != '*' and location != otherlocation:
                    return False
            return True

    def __ge__(self, other):
        return other <= self

    def __lt__(self, other):
        return self <= other and self != other

    def __gt__(self, other):
        return other <= self and self != other
