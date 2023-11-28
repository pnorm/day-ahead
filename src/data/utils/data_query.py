from datetime import date
from pydantic import BaseModel, field_validator, Field
from typing import ClassVar


class BaseDataQuery(BaseModel):
    current_date: date = Field(...)
    base_url: ClassVar[str]
    feature: str
    complete_url: str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.complete_url = self.generate_url()

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            v = date.fromisoformat(v)
        return v

    def to_str_date(self):
        raise NotImplementedError("to_str_date method must be implemented in subclasses")

    def generate_url(self) -> str:
        current_date_str = self.to_str_date()
        return f"{self.base_url}?dateShow={current_date_str}"


class PSEDataQuery(BaseDataQuery):
    base_url = "https://www.pse.pl/getcsv/-/export/csv"

    @field_validator("current_date")
    def validate_date_range(cls, v):
        min_allowed_date = date(2013, 1, 1)
        today = date.today()

        if v < min_allowed_date or v > today:
            raise ValueError(f"Date must be between {min_allowed_date} and {today}. Given date: {v}")

        return v
    
    @field_validator("feature")
    def validate_feature(cls, v):
        valid_features = ['PL_GEN_WIATR', 'PL_GEN_MOC_JW_EPS']
        if v not in valid_features:
            raise ValueError(f"Invalid feature. Valid features are: {valid_features}")

        return v

    def to_str_date(self):
        return self.current_date.strftime("%Y%m%d")

    def generate_url(self) -> str:
        current_date_str = self.to_str_date()
        return f"{self.base_url}/{self.feature}/data/{current_date_str}/unit/all"


class TGEDataQuery(BaseDataQuery):
    base_url = "https://tge.pl/energia-elektryczna-rdn"
    feature: str = 'TGE'

    @field_validator("current_date")
    def validate_date(cls, v):
        today = date.today()

        if v > today:
            raise ValueError(f"Date must not be greater than today. Given date: {v}")

        return v

    def to_str_date(self):
        return self.current_date.strftime("%d-%m-%Y")