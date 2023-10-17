import re
from decimal import Decimal
from measurement.measures import Distance  # type: ignore


class RaceDistance(Distance):
    """
    A thin wrapper around the measurement library Distance class to allow for the creation of Distance objects
    from strings and to provide a way to initialize with furlongs.
    """

    REGEX = r"(?:(\d+)(?:m)\s*)?(?:(\d+)(?:f)\s*)?(?:(\d+)(?:y)\s*)?"

    def __init__(self, distance: str = None, **kwargs) -> None:
        """
        Initialize a RaceDistance object from a string.

        """
        if distance:
            if not re.fullmatch(r"(?:\d+[m|f|y]\s*)*", distance.replace(",", "")):
                raise AttributeError(f"Invalid distance string: {distance}")

            miles_or_metres, furlongs, yards = re.match(
                RaceDistance.REGEX, distance.replace(",", "")
            ).groups()

            if int(miles_or_metres or 0) > 10:
                kwargs["m"] = int(miles_or_metres or 0)
            else:
                kwargs["yd"] = (
                    int(miles_or_metres or 0) * 1760
                    + int(furlongs or 0) * 220
                    + int(yards or 0)
                )

        super().__init__(self, **kwargs)

    def __repr__(self) -> str:
        """
        Returns the distance as a repr.
        """
        return f"<RaceDistance: {str(self)}>"

    def __str__(self) -> str:
        """
        Returns the distance as a string.
        """
        mile = self.furlong // 8
        furlong = (self.furlong % 8) // 1
        yard = int((self.furlong % 1) * 220)
        return " ".join(
            [
                f"{mile}m" if mile else "",
                f"{furlong}f" if furlong else "",
                f"{yard}y" if yard else "",
            ]
        ).strip()

    @property
    def furlong(self) -> Decimal:
        """
        Returns the distance in furlongs.
        """
        return Decimal(self.chain / 10)
