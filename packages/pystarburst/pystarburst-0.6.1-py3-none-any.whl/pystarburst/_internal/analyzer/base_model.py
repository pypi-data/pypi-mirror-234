#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        validate_assignment = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
        frozen = True
