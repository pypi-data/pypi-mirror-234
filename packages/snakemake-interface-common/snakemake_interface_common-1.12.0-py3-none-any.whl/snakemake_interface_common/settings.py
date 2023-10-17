from enum import Enum
from typing import FrozenSet, List, Set, TypeVar, Union

TSettingsEnumBase = TypeVar("TSettingsEnumBase", bound="SettingsEnumBase")


class SettingsEnumBase(Enum):
    @classmethod
    def choices(cls) -> List[str]:
        return sorted(item.item_to_choice() for item in cls)

    @classmethod
    def all(cls) -> FrozenSet[TSettingsEnumBase]:
        return frozenset(item for item in cls)

    @classmethod
    def parse_choices_list(self, choices: List[str]) -> List[TSettingsEnumBase]:
        return self._parse_choices_into(choices, list)

    @classmethod
    def parse_choices_set(self, choices: List[str]) -> Set[TSettingsEnumBase]:
        return self._parse_choices_into(choices, set)

    @classmethod
    def _parse_choices_into(
        cls, choices: str, container: Union[List, Set]
    ) -> List[TSettingsEnumBase]:
        return container(cls.parse_choice(choice) for choice in choices)

    @classmethod
    def parse_choice(cls, choice: str) -> TSettingsEnumBase:
        return cls[choice.replace("-", "_").upper()]

    def item_to_choice(self) -> str:
        return self.name.replace("_", "-").lower()

    def __str__(self):
        return self.item_to_choice()
