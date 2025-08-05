from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class SuperheroCreateDTO(BaseModel):
    name: str


class SuperheroBaseDTO(SuperheroCreateDTO):
    intelligence: int = 0
    strength: int = 0
    speed: int = 0
    power: int = 0
    durability: int = 0
    combat: int = 0


class SuperheroFullDTO(SuperheroBaseDTO):
    id: int


class SuperheroFilter(BaseModel):
    name: Optional[str] = Field(None, description="Exact name match")

    intelligence_eq: Optional[int] = Field(
        None,
        alias="intelligence_eq",
    )
    intelligence_ge: Optional[int] = Field(
        None,
        alias="intelligence_ge",
    )
    intelligence_le: Optional[int] = Field(
        None,
        alias="intelligence_le",
    )

    strength_eq: Optional[int] = Field(None, alias="strength_eq")
    strength_ge: Optional[int] = Field(None, alias="strength_ge")
    strength_le: Optional[int] = Field(None, alias="strength_le")

    speed_eq: Optional[int] = Field(None, alias="speed_eq")
    speed_ge: Optional[int] = Field(None, alias="speed_ge")
    speed_le: Optional[int] = Field(None, alias="speed_le")

    power_eq: Optional[int] = Field(None, alias="power_eq")
    power_ge: Optional[int] = Field(None, alias="power_ge")
    power_le: Optional[int] = Field(None, alias="power_le")

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"

    def to_filter_dict(self) -> Dict[str, Dict[str, Any]]:
        result = {}
        for field, value in self.model_dump(by_alias=True).items():
            if value is not None:
                if "_" in field:
                    field_name, op = field.split("_")
                    if field_name not in result:
                        result[field_name] = {}
                    result[field_name][op] = value
                else:
                    result[field] = value
        return result
