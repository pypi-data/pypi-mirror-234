import re
from measurement.measures import Weight  # type: ignore


class RaceWeight(Weight):
    """
    A thin wrapper around the measurement library Weight class to allow for the creation of Weight objects
    from strings.
    """

    REGEX = r"(?:(\d+)(?:st|\-))?(?:(\d+)(?:lb)*)?"

    def __init__(self, weight: str = None, **kwargs):
        """
        Initialize a RaceWeight object from a string.
        """

        if weight:
            st, lbs = re.match(RaceWeight.REGEX, weight).groups()
            super().__init__(self, lb=(int(st or 0) * 14 + int(lbs or 0)))  # type: ignore
        else:
            super().__init__(self, **kwargs)

    def __repr__(self) -> str:
        """
        Returns the weight as a repr.
        """
        return f"<RaceWeight: {str(self)}>"

    def __str__(self) -> str:
        """
        Returns the weight as a string.
        """
        st = int(self.lb // 14)
        lb = int(self.lb % 14)
        return f"{st}st {lb}lb"
