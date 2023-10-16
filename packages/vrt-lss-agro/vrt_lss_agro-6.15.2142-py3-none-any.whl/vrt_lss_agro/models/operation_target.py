# coding: utf-8

"""
    VRt.Agro [AG]

    Veeroute Agro API.  # Description  The service is designed to calculate the work plan of production facilities.  ## Objects overview  ![objects](../images/agro_objects.svg)  ### Field  - produces a certain crop of a certain moisture content - products from the field can only be moved to the Elevator or Factory  ### Elevator  - consists of Gates, Dryers, short-term and long-term storage areas - dries the grain (if the moisture content of the crop is more than acceptable) - stores dry grain in short-term storage places (warehouses), while unloading and loading grain is allowed within one day - stores dry grain in long-term storage places (sleeves, trenches, mounds) - when stored in one storage, only one type of culture can be located - sells surplus grain to the Market - production processes inside the facility: drying, loading / unloading to a storage location, storage  ### Factory  - consists of Gates, Dryers, Bunkers, Consumers - [if drying is present] dries the grain (if the moisture content of the crop is more than allowed) - stores dry grain in Bunkers (short-term storage tied to a specific crop) - maintains a minimum supply of grain for consumption in the Bunkers - Consumes grain from Bunkers - buys the missing grain from the Market - production processes inside the facility: drying, loading / unloading to a storage location, storage, consumption  ### Market  - buys grain from elevators - sells grain to factories  ## Project  The project reflects the planned sequence of operations on agricultural crops, the types of operations are described below.  ### HARVEST  Crop harvesting:  - between production facilities (Field and Elevator or Field) - the operation takes place within one day - on the Field there is a determination of grain moisture  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Field               | -                             | | Destination | Elevator or Factory | Gate                          |  ### DRY  Drying culture:  - inside the production facility (Elevator or Field) - duration of the operation - days - during the drying process, the mass and type of humidity changes (WET -> DRY) - the source indicates the mass of raw culture - in the appointment, the resulting mass of dry culture is indicated  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Elevator or Factory | Gate                          | | Destination | Elevator or Factory | Dryer                         |  ### LOAD  Loading culture from the Gate to the Storage Location (long-term, short-term, silo):  - between parts of one production facility (Elevator or Field) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key)                    | |-------------|---------------------|--------------------------------------------------| | Source      | Elevator or Factory | Gate or Dryer                                    | | Destination | Elevator or Factory | Storage location (long-term, short-term, bunker) |  ### UNLOAD  Unloading the culture from the storage place to the gate:  - between parts of one production facility (Elevator) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key)                    | |-------------|---------------------|--------------------------------------------------| | Source      | Elevator            | Storage location (long-term, short-term, bunker) | | Destination | Elevator            | Gate                                             |  ### STORE  Culture storage:  - the operation takes place within one day - storage location does not change  |             | Object (target_key) | Subobject (target_detail_key)                    | |-------------|---------------------|--------------------------------------------------| | Source      | Elevator or Factory | Storage location (long-term, short-term, bunker) | | Destination | Elevator or Factory | The same storage location                        |  ### RELOCATE  Transportation between production facilities:  - between production facilities (Elevator and Field) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Elevator            | Gate                          | | Destination | Factory             | Gate                          |  ### CONSUMPTION  Field crop consumption:  - between parts of one production facility (Field) - the operation takes place within one day - consumption comes from the Bunker - in addition, we can consume directly from the Gate or Dryer without laying in the Bunker  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Factory             | Hopper or Gate or Dryer       | | Destination | Factory             | Consumer                      |  ### SELL  Sale of culture:  - between production facilities (Elevator and Market) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Elevator            | Gate                          | | Destination | Market              | Contract                      |  ### BUY  Buying culture:  - between production facilities (Market and Factory) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Market              | Contract                      | | Destination | Factory             | Gate                          |  ## Entity relationship diagram  ![erd](../uml/agro.svg) 

    The version of the OpenAPI document: 6.15.2142
    Contact: servicedesk@veeroute.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import date
from typing import List, Optional, Union
from pydantic import BaseModel, Field, confloat, conint, conlist, constr
from vrt_lss_agro.models.attribute import Attribute
from vrt_lss_agro.models.crop_type import CropType
from vrt_lss_agro.models.object_type import ObjectType

class OperationTarget(BaseModel):
    """
    Operation target.   # noqa: E501
    """
    var_date: date = Field(..., alias="date", description="Date in the YYYY-MM-DD format.")
    target_key: constr(strict=True, max_length=1024, min_length=1) = Field(..., description="Target key.")
    target_type: ObjectType = Field(...)
    target_detail_key: Optional[constr(strict=True, max_length=1024, min_length=1)] = Field(None, description="The key of the object part, if it exists for this operation - [more](#section/Description/Project). ")
    crop_type: CropType = Field(...)
    humidity: conint(strict=True, le=999, ge=1) = Field(..., description="Humidity crop, in ppm (‰).")
    mass: Union[confloat(le=10000000.1, ge=0, strict=True), conint(le=10000000, ge=0, strict=True)] = Field(..., description="Weight, in tn.")
    attributes: Optional[conlist(Attribute, max_items=1000, min_items=0, unique_items=True)] = Field(None, description="Attributes. Used to add service information.")
    __properties = ["date", "target_key", "target_type", "target_detail_key", "crop_type", "humidity", "mass", "attributes"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationTarget:
        """Create an instance of OperationTarget from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in attributes (list)
        _items = []
        if self.attributes:
            for _item in self.attributes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['attributes'] = _items
        # set to None if target_detail_key (nullable) is None
        # and __fields_set__ contains the field
        if self.target_detail_key is None and "target_detail_key" in self.__fields_set__:
            _dict['target_detail_key'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OperationTarget:
        """Create an instance of OperationTarget from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OperationTarget.parse_obj(obj)

        _obj = OperationTarget.parse_obj({
            "var_date": obj.get("date"),
            "target_key": obj.get("target_key"),
            "target_type": obj.get("target_type"),
            "target_detail_key": obj.get("target_detail_key"),
            "crop_type": obj.get("crop_type"),
            "humidity": obj.get("humidity"),
            "mass": obj.get("mass"),
            "attributes": [Attribute.from_dict(_item) for _item in obj.get("attributes")] if obj.get("attributes") is not None else None
        })
        return _obj


