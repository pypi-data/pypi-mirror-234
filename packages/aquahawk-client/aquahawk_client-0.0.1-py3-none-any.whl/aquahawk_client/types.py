"""Define package types."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

import dataclasses_json.cfg
from dataclasses_json import LetterCase, config

dataclasses_json.cfg.global_config.encoders[datetime] = datetime.isoformat
dataclasses_json.cfg.global_config.decoders[datetime] = datetime.fromisoformat


class Interval(Enum):
    ONE_HOUR = "1 hour"
    ONE_DAY = "1 day"
    ONE_MONTH = "1 month"
    ONE_YEAR = "1 year"


@dataclass
class WaterUsage(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]
    num: float
    min: float
    max: float
    sum: float
    sumSq: float
    sumIx: float
    gallons: float
    thousandGallons: float = field(metadata=config(field_name="thousand gallons"))
    hundredGallons: float = field(metadata=config(field_name="hundred gallons"))
    cubicMeters: float = field(metadata=config(field_name="cubic meters"))
    liters: float
    thousandCubicFeet: float = field(metadata=config(field_name="thousand cubic feet"))
    hundredCubicFeet: float = field(metadata=config(field_name="hundred cubic feet"))
    cubicFeet: float = field(metadata=config(field_name="cubic feet"))
    acreInches: float = field(metadata=config(field_name="acre inches"))
    acreFeet: float = field(metadata=config(field_name="acre feet"))


@dataclass
class Rainfall(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]
    num: int
    min: int
    max: int
    sum: int
    sum_sq: int
    sum_ix: int
    inches: int
    centimeters: int
    millimeters: int


@dataclass
class Temperature(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]
    num: int
    min: float
    max: float
    sum: float
    sum_sq: float
    sum_ix: float
    sum_pos: Optional[float] = 0.0
    degrees: Optional[float] = 0.0
    fahrenheit: Optional[float] = 0.0
    celsius: Optional[float] = 0.0


@dataclass
class Timesery(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]
    interval: Interval
    timezone: str
    timestamp: str
    start_time: datetime
    end_time: datetime
    msec: int
    water_use_actual: Optional[WaterUsage] = None
    water_use: Optional[WaterUsage] = None
    rainfall: Optional[Rainfall] = None
    high_temp: Optional[Temperature] = None
    low_temp: Optional[Temperature] = None
    avg_temp: Optional[Temperature] = None


@dataclass
class Usage(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]
    success: bool
    message: str
    total: int
    timeseries: List[Timesery]
    first_time: datetime
    last_time: datetime
