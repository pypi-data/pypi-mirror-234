from peak_utility.enumeration.parsing_enum import ParsingEnum  # type: ignore
from .sex import Sex


class Gender(ParsingEnum):
    """
    An enumeration representing the gender of a horse.

    """

    FOAL = 0
    YEARLING = 1
    COLT = 2
    FILLY = 3
    STALLION = 4
    MARE = 5
    GELDING = 6
    RIG = 7

    # Abbreviations
    C = COLT
    F = FILLY
    S = STALLION
    M = MARE
    G = GELDING
    R = RIG

    # Plural
    FOALS = FOAL
    YEARLINGS = YEARLING
    COLTS = COLT
    FILLIES = FILLY
    STALLIONS = STALLION
    MARES = MARE
    GELDINGS = GELDING
    RIGS = RIG

    @property
    def sex(self):
        """
        Get the sex of the horse based on its gender.

        Raises:
            ValueError: If the gender of the horse is not specific enough to determine its sex.

        Returns:
            Sex: The sex of the horse, either `Sex.FEMALE` or `Sex.MALE`.

        """
        if self in [Gender.FOAL, Gender.YEARLING]:
            raise ValueError("Not enough information to provide sex of horse")

        return Sex.FEMALE if self in [Gender.FILLY, Gender.MARE] else Sex.MALE

    @staticmethod
    def determine(official_age: int, sex: Sex | None = None, **kwargs):
        """
        Determine the gender of a horse based on its sex, official age, and optional arguments.

        Args:
            official_age: The official age of the horse in years.
            sex: The sex of the horse.
            **kwargs: Additional keyword arguments that may be used to determine the gender. Accepts is_rig and is_gelded.

        Raises:
            ValueError: If a female horse is specified as a gelding or rig.

        Returns:
            Gender: The gender of the horse based on the input arguments.

        """
        if official_age == 0:
            return Gender.FOAL
        if official_age == 1:
            return Gender.YEARLING
        if kwargs.get("is_gelded"):
            if sex and sex is sex.FEMALE:
                raise ValueError("Female horse cannot be gelded")
            return Gender.GELDING
        if kwargs.get("is_rig"):
            if sex and sex is sex.FEMALE:
                raise ValueError("Female horse cannot be rig")
            return Gender.RIG
        if sex is None:
            raise ValueError("Not enough information to determine gender")
        if official_age <= 3:
            return Gender.COLT if sex is sex.MALE else Gender.FILLY
        else:
            return Gender.STALLION if sex is sex.MALE else Gender.MARE
