from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # Avoid circular imports
    from datadoc_model.LanguageStrings import LanguageStrings
    from datadoc_model.Enums import SupportedLanguages


class LanguageStringsEnum(Enum):
    def __init__(self, language_strings: "LanguageStrings"):
        """Store the LanguageStrings object for displaying enum values
        in multiple languages.

        We don't particularly care what the value of the enum is,
        but when serialised it's convenient and readable to use the
        name of the enum, so we set the value to be the name.
        """
        self._value_ = self.name
        self.language_strings = language_strings

    @classmethod
    def _missing_(cls, value):
        """Support constructing an enum member from a supplied name string"""
        try:
            member = cls._member_map_[value]
        except KeyError:
            # Raise the expected exception with a useful explanation
            raise ValueError(f"{value} is not a valid {cls.__qualname__}")
        else:
            return member

    def get_value_for_language(self, language: "SupportedLanguages") -> str:
        """Retrieve the string for the relevant language"""
        return getattr(self.language_strings, language.value)
