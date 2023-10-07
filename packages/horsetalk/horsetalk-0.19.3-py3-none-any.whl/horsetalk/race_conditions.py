from pendulum import DateTime
from .going import Going
from .race_designation import RaceDesignation
from .race_distance import RaceDistance
from .race_level import RaceLevel
from .racecourse import Racecourse
from .stalls_position import StallsPosition


class RaceConditions:
    """
    A class for grouping together race conditions into a single object.

    """

    def __init__(
        self,
        *,
        datetime: DateTime,
        racecourse: Racecourse,
        distance: RaceDistance,
        going: Going,
        race_designation: RaceDesignation,
        race_level: RaceLevel,
        stalls_position: StallsPosition | None = None,
    ):
        """
        Initialize a RaceConditions instance.

        Args:
            datetime: The datetime of the race
            racecourse: The racecourse on which the race is run
            distance: The race distance
            going: The going of the race
            race_designation: The designation of the race, i.e. whether it is a handicap, maiden, etc.
            race_level: The level of the race, i.e. Group 1, Group 2, etc.
            stalls_position: The position of the stalls on the track

        """
        self.datetime = datetime
        self.racecourse = racecourse
        self.distance = distance
        self.going = going
        self.race_designation = race_designation
        self.race_level = race_level
        self.stalls_position = stalls_position

    def __repr__(self):
        return (
            f"<RaceConditions: datetime={self.datetime}, "
            f"racecourse={self.racecourse!r}, "
            f"distance={self.distance}, "
            f"going={self.going}, "
            f"race_designation={self.race_designation.name.title()}, "
            f"race_level={self.race_level.grade or self.race_level.class_}, "
            f"stalls_position={self.stalls_position}>"
        )

    def __str__(self):
        return (
            f"{self.datetime.format('D MMM YYYY, HH:mm')}, "
            f"{self.racecourse.name}, "
            f"{self.distance.furlong}f ({self.going}), "
            f"{self.race_designation.name.title()} "
            f"{self.race_level}"
            f"{', Stalls: ' + str(self.stalls_position.name.title()) if self.stalls_position else ''}"
        )
