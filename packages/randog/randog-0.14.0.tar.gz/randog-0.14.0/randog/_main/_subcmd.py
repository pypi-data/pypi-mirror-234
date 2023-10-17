from enum import Enum


class Subcmd(Enum):
    Byfile = "byfile"
    Bool = "bool"
    Int = "int"
    Float = "float"
    String = "str"
    Decimal = "decimal"
    Datetime = "datetime"
    Date = "date"
    Time = "time"
    Timedelta = "timedelta"
