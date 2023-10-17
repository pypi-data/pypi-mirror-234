import re
from decimal import Decimal
from measurement.measures import Distance  # type: ignore


class HorseHeight(Distance):
    """
    A class for measuring a horse's height, created by wrapping the measurement library Distance class to allow
    for the use of hands as a unit.

    """

    def __init__(self, distance: str) -> None:
        """
        Initialize a HorseHeight object from a string.
        """
        pattern = re.compile(r"(\d+\D+)")
        vals_and_units = pattern.findall(distance.replace(" ", ""))

        height = Distance(inch=0)
        for vu in vals_and_units:
            matches = re.compile(r"(\d+)(\D+)").match(vu)
            if matches:
                val, unit = matches.groups()
                if unit == "hands" or unit == "hh":
                    height += Distance(inch=int(val) * 4)
                else:
                    height += Distance(**{unit: int(val)})

        super().__init__(self, inch=height.inch)

    def __repr__(self) -> str:
        """
        Returns:
            A representation of the HorseHeight object.
        """
        return f"<HorseHeight: {self.hand}hh>"

    def __str__(self) -> str:
        """
        Returns:
            A string representation of the HorseHeight object.
        """
        return f"{self.hand}hh"

    @property
    def hand(self) -> Decimal:
        """
        Returns the height in hands.
        """
        return Decimal(self.inch / 4)
