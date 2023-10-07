import re
from decimal import Decimal
from measurement.measures import Distance  # type: ignore


class RaceDistance(Distance):
    """
    A thin wrapper around the measurement library Distance class to allow for the creation of Distance objects
    from strings and to provide a way to initialize with furlongs.
    """

    REGEX = r"((?:\d+(?:m|f|y)\s*)+)"

    def __init__(self, distance: str) -> None:
        """
        Initialize a RaceDistance object from a string.
        """
        pattern = re.compile(r"(\d+\D+)")
        unit_dict = {"m": "mile", "f": "furlong", "y": "yard"}
        vals_and_units = pattern.findall(distance.replace(" ", "").replace(",", ""))

        distance = Distance(m=0)
        for vu in vals_and_units:
            matches = re.compile(r"(\d+)(\D+)").match(vu)
            if matches:
                val, unit = matches.groups()
                unit = unit_dict[unit] if unit in unit_dict and int(val) < 221 else unit

                if unit == "furlong":
                    distance += Distance(chain=int(val) * 10)
                else:
                    distance += Distance(**{unit: int(val)})

        super().__init__(self, m=distance.m)  # type: ignore

    def __repr__(self) -> str:
        """
        Returns the distance as a string.
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
