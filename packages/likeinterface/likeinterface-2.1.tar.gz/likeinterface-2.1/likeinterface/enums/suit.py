from enum import Enum


class Suit(str, Enum):
    """
    This object represents card suit.
    """

    CLUBS = "C"
    DIAMONDS = "D"
    HEARTS = "H"
    SPADES = "S"
