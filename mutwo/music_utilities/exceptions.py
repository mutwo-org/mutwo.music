__all__ = (
    "DuplicatePlayingIndicatorConverterMappingWarning",
    "UnsortedIntervalTupleError",
    "NotInstalledError",
)


class DuplicatePlayingIndicatorConverterMappingWarning(RuntimeWarning):
    def __init__(self, articulation_name: str, playing_indicator_converter):
        super().__init__(
            "Found two playing indicator converter mappings for "
            f"articulation name '{articulation_name}'! "
            "Mutwo will use the playing indicator converter "
            f"'{playing_indicator_converter}'."
        )


class UnsortedIntervalTupleError(Exception):
    def __init__(self, interval_tuple):
        super().__init__(
            f"Interval sequence '{interval_tuple}' is neither"
            "falling nor rising. Please either call "
            "'sorted(interval_sequence)' or 'sorted(interval_sequence, "
            "reverse=True)' before passing your interval sequence to "
            "'ScaleFamily'."
        )


class NotInstalledError(Exception):
    def __init__(self, object_: str, package: str):
        super().__init__(
            f"Can't use '{object_}', because optional "
            f"package '{package}' isn't installed!"
        )
