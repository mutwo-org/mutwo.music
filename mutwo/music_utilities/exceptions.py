__all__ = ("DuplicatePlayingIndicatorConverterMappingWarning",)


class DuplicatePlayingIndicatorConverterMappingWarning(RuntimeWarning):
    def __init__(self, articulation_name: str, playing_indicator_converter):
        super().__init__(
            "Found two playing indicator converter mappings for "
            f"articulation name '{articulation_name}'! "
            "Mutwo will use the playing indicator converter "
            f"'{playing_indicator_converter}'."
        )
