import ast
import configparser
import typing

from mutwo import music_parameters

__all__ = ("IndicatorCollectionParser",)


class IndicatorCollectionParser(configparser.ConfigParser):
    """Parse strings to :class:`~mutwo.music_parameters.abc.IndicatorCollection`.

    See :class:`configparser.ConfigParser` for provided arguments.
    """

    STATEMENT_DELIMITER = ";"

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            allow_no_value=True,
            empty_lines_in_values=False,
            interpolation=None,
            **kwargs,
        )

    def parse(
        self, s: str, indicator_collection: music_parameters.abc.IndicatorCollection
    ) -> music_parameters.abc.IndicatorCollection:
        self.clear()
        section_name = "indicatorcollection"
        section = f"[{section_name}]\n{self._preprocess(s)}"
        self.read_string(section)
        for k, v in self[section_name].items():
            v = self._guess_type(v)
            o = indicator_collection
            attribute_list = k.split(".")
            for attribute in attribute_list[:-1]:
                o = getattr(o, attribute)
            setattr(o, attribute_list[-1], v)
        return indicator_collection

    def _preprocess(self, s: str) -> str:
        return "\n".join(
            line.strip()
            for line in s.replace(self.STATEMENT_DELIMITER, "\n").splitlines()
        )

    def _guess_type(self, v: str) -> typing.Any:
        try:
            return ast.literal_eval(v)
        except (ValueError, SyntaxError):
            return v
