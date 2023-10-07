from peak_utility.enumeration.parsing_enum import ParsingEnum  # type: ignore


class AgeCategory(ParsingEnum):
    """
    An enumeration that represents the age category of a horse.

    """

    JUVENILE = 1
    VETERAN = 2

    # Alternatives
    VETERANS = VETERAN
