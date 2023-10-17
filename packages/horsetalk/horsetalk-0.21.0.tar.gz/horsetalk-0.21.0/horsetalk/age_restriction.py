import re


class AgeRestriction:
    REGEX = (
        r"(\d{1,2})[-]?(\d{1,2})?\s?y(?:ear)?(?:\s|-)?o(?:ld(?:s)?)?(?:\sonly)?(\+)?"
    )

    def __init__(self, string: str):
        """
        Initialize an AgeRestriction instance.

        Args:
            age_restriction_string: The age restriction string.

        Returns:
            An AgeRestriction instance.
        """
        groups = re.search(self.REGEX, string).groups()
        mini, maxi, plus = list(groups) + [None] * (3 - len(groups))

        self.minimum = int(mini)
        self.maximum = None if plus else int(maxi or mini)

    def __repr__(self):
        """
        Returns the age restriction as a repr.

        Returns:
            The age restriction as a repr.
        """
        return f"<AgeRestriction: {str(self)}>"

    def __str__(self):
        """
        Returns the age restriction as a string.

        Returns:
            The age restriction as a string.
        """
        if self.minimum == self.maximum:
            return f"{self.minimum}yo"
        elif self.maximum:
            return f"{self.minimum}-{self.maximum}yo"
        else:
            return f"{self.minimum}yo+"
