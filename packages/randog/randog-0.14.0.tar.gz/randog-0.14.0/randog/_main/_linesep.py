import enum
import typing as t


class Linesep(enum.Enum):
    LF = "\n"
    CRLF = "\r\n"
    CR = "\r"

    @classmethod
    def names(cls) -> t.Tuple[str, ...]:
        return tuple(map(lambda e: e.name, cls))
