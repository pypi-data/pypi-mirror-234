from typing import List, Literal, Optional, Union

from .action import Action
from .authorization import Authorization
from .balance import Balance
from .base import LikeObject, MutableLikeObject
from .cards import Cards
from .collection import Collection
from .collection_element import CollectionElement
from .file import File
from .game import Game
from .hand import Hand
from .input_file import BufferedInputFile, FileSystemInputFile, InputFile
from .player import Player
from .user import User

__all__ = (
    "Action",
    "Authorization",
    "Balance",
    "BufferedInputFile",
    "Cards",
    "Collection",
    "CollectionElement",
    "File",
    "FileSystemInputFile",
    "Game",
    "Hand",
    "InputFile",
    "LikeObject",
    "MutableLikeObject",
    "Player",
    "User",
)

for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "model_rebuild"):
        continue
    _entity.model_rebuild(
        _types_namespace={
            "List": List,
            "Optional": Optional,
            "Union": Union,
            "Literal": Literal,
            **{k: v for k, v in globals().items() if k in __all__},
        }
    )

del _entity
del _entity_name
