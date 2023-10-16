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


from typing import List, Optional
from pydantic import BaseModel, Field, conlist
from vrt_lss_agro.models.crop import Crop
from vrt_lss_agro.models.elevator import Elevator
from vrt_lss_agro.models.factory import Factory
from vrt_lss_agro.models.field import Field
from vrt_lss_agro.models.leftover import Leftover
from vrt_lss_agro.models.market import Market
from vrt_lss_agro.models.movement_matrix_element import MovementMatrixElement
from vrt_lss_agro.models.plan_settings import PlanSettings

class PlanTask(BaseModel):
    """
    Initial task.  # noqa: E501
    """
    crops: conlist(Crop, max_items=501, min_items=1, unique_items=True) = Field(..., description="List of crops.")
    fields: conlist(Field, max_items=20001, min_items=1, unique_items=True) = Field(..., description="List of fields.")
    elevators: Optional[conlist(Elevator, max_items=501, min_items=1, unique_items=True)] = Field(None, description="List of elevators.")
    factories: conlist(Factory, max_items=501, min_items=1, unique_items=True) = Field(..., description="List of factories.")
    markets: conlist(Market, max_items=501, min_items=1, unique_items=True) = Field(..., description="List of markets.")
    movement_matrix: conlist(MovementMatrixElement, max_items=8040402, min_items=1, unique_items=True) = Field(..., description="Matrix describing the cost (in kilometers and monetary units) of moving grain between objects (in both directions). If there is no corresponding entry in the matrix between the objects, the movement of grain between them is considered impossible. ")
    leftovers: Optional[conlist(Leftover, max_items=25001, min_items=0)] = Field(None, description="List of leftovers.")
    plan_settings: PlanSettings = Field(...)
    __properties = ["crops", "fields", "elevators", "factories", "markets", "movement_matrix", "leftovers", "plan_settings"]

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
    def from_json(cls, json_str: str) -> PlanTask:
        """Create an instance of PlanTask from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in crops (list)
        _items = []
        if self.crops:
            for _item in self.crops:
                if _item:
                    _items.append(_item.to_dict())
            _dict['crops'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in fields (list)
        _items = []
        if self.fields:
            for _item in self.fields:
                if _item:
                    _items.append(_item.to_dict())
            _dict['fields'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in elevators (list)
        _items = []
        if self.elevators:
            for _item in self.elevators:
                if _item:
                    _items.append(_item.to_dict())
            _dict['elevators'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in factories (list)
        _items = []
        if self.factories:
            for _item in self.factories:
                if _item:
                    _items.append(_item.to_dict())
            _dict['factories'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in markets (list)
        _items = []
        if self.markets:
            for _item in self.markets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['markets'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in movement_matrix (list)
        _items = []
        if self.movement_matrix:
            for _item in self.movement_matrix:
                if _item:
                    _items.append(_item.to_dict())
            _dict['movement_matrix'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in leftovers (list)
        _items = []
        if self.leftovers:
            for _item in self.leftovers:
                if _item:
                    _items.append(_item.to_dict())
            _dict['leftovers'] = _items
        # override the default output from pydantic by calling `to_dict()` of plan_settings
        if self.plan_settings:
            _dict['plan_settings'] = self.plan_settings.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PlanTask:
        """Create an instance of PlanTask from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PlanTask.parse_obj(obj)

        _obj = PlanTask.parse_obj({
            "crops": [Crop.from_dict(_item) for _item in obj.get("crops")] if obj.get("crops") is not None else None,
            "fields": [Field.from_dict(_item) for _item in obj.get("fields")] if obj.get("fields") is not None else None,
            "elevators": [Elevator.from_dict(_item) for _item in obj.get("elevators")] if obj.get("elevators") is not None else None,
            "factories": [Factory.from_dict(_item) for _item in obj.get("factories")] if obj.get("factories") is not None else None,
            "markets": [Market.from_dict(_item) for _item in obj.get("markets")] if obj.get("markets") is not None else None,
            "movement_matrix": [MovementMatrixElement.from_dict(_item) for _item in obj.get("movement_matrix")] if obj.get("movement_matrix") is not None else None,
            "leftovers": [Leftover.from_dict(_item) for _item in obj.get("leftovers")] if obj.get("leftovers") is not None else None,
            "plan_settings": PlanSettings.from_dict(obj.get("plan_settings")) if obj.get("plan_settings") is not None else None
        })
        return _obj


