import pendulum  # type: ignore
import re
from .horse_age import HorseAge


class Horse:
    REGEX = re.compile(
        r"""
        (?P<name>\w{3,18})                  # Horse's name
        \s*                                 # Optional whitespace
        (?:\((?P<country>\w+)\))?           # Country of origin
        \s*                                 # Optional whitespace
        (?P<age_or_yob>\d{1,4})?            # Age or year of birth
    """,
        re.VERBOSE,
    )

    def __init__(
        self, name, country=None, age_or_yob=None, context_date=pendulum.now()
    ):
        match = re.match(Horse.REGEX, name)

        self.name = match.group("name")
        self.country = match.group("country") or country

        if country and country != self.country:
            raise ValueError(
                f"Conflicting countries in name and country arguments: {country}"
            )

        if (
            age_or_yob
            and match.group("age_or_yob")
            and int(match.group("age_or_yob")) != age_or_yob
        ):
            raise ValueError(
                f"Conflicting age_or_yob in name and age_or_yob arguments: {age_or_yob}"
            )

        age_or_yob = int(match.group("age_or_yob") or age_or_yob or -1)

        if age_or_yob > 999:
            self.age = HorseAge(birth_year=age_or_yob, context_date=context_date)
        elif age_or_yob > 0:
            self.age = HorseAge(age_or_yob, context_date=context_date)
        else:
            self.age = None
