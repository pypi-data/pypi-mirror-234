from enum import Enum
from typing import List, Type
from .age_category import AgeCategory
from .horse_experience_level import HorseExperienceLevel
from .gender import Gender
from .jump_category import JumpCategory
from .race_designation import RaceDesignation


class RaceTitle:
    """
    A class for parsing a race title into its component parts.

    Attributes:
        _words (List[str]): A list of words in the race title.

    Methods:
        parse(title: str) -> dict: Parses a race title into component parts and returns a dictionary.
        _lookup(enum: Type[Enum], allow_multiple: bool = False) -> List[Enum] | Enum | None:
            Private method to lookup an Enum value from a list of words.

    """

    _words: List[str] = []

    @classmethod
    def parse(cls, title: str) -> dict:
        """Parses a race title into component parts.

        Args:
            title: A race title.

        Returns:
            dict: A dictionary of component parts.
        """
        self = cls()
        self._words = title.split()

        enums = [
            AgeCategory,
            HorseExperienceLevel,
            Gender,
            JumpCategory,
            RaceDesignation,
        ]
        end_index = -1
        for i, word in enumerate(self._words):
            if any(getattr(enum, word, None) is not None for enum in enums):
                end_index = i
                break
        name = " ".join(self._words[:end_index])

        return {
            "age_category": self._lookup(AgeCategory),
            "horse_experience_level": self._lookup(HorseExperienceLevel),
            "gender": self._lookup(Gender, allow_multiple=True),
            "jump_category": self._lookup(JumpCategory),
            "race_designation": self._lookup(RaceDesignation),
            "name": name,
        }

    def _lookup(
        self, enum: Type[Enum], allow_multiple: bool = False
    ) -> List[Enum] | Enum | None:
        """Private method to lookup an enum value from a list of words.

        Args:
            enum (Type[Enum]): The Enum to search through.
            allow_multiple (bool, optional): Whether or not to allow multiple Enum values to be returned. Defaults to False.

        Returns:
            Union[List[Enum], Enum, None]: The found Enum value or None.

        """
        found_values = [
            found_value
            for word in self._words
            if (found_value := getattr(enum, word, None)) is not None
        ]
        return (
            None
            if not found_values
            else found_values
            if allow_multiple
            else found_values[-1]
        )
