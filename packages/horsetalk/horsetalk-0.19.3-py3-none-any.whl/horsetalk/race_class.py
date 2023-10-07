from peak_utility.number import RepresentationalInt  # type: ignore


class RaceClass(RepresentationalInt):
    """
    A class to represent a race's class.

    """

    def __new__(cls, value: str | int):
        """
        Create a RaceClass instance.

        Args:
            value: The value to initialize with

        Raises:
            ValueError: If the value is not valid

        """
        class_value = str(value).lower().replace("class", "").strip()

        if not 1 <= int(class_value) <= 7:
            raise ValueError(f"Class must be between 1 and 7, not {value}")

        return super().__new__(cls, int(class_value))

    def __repr__(self) -> str:
        return f"<RaceClass: {str(int(self))}>"

    def __str__(self) -> str:
        return f"Class {str(int(self))}"

    def __eq__(self, other):
        if isinstance(other, RaceClass) or (isinstance(other, int) and other < 4):
            return super().__eq__(other)

        return False

    def __lt__(self, other):
        return super().__gt__(other)

    def __gt__(self, other):
        return super().__lt__(other)
