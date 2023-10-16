# -*- coding: utf-8 -*-
"""Robotics base model."""
from pydantic import BaseModel, Extra


class RoboticsBaseModel(BaseModel):
    """Robotics base model.

    Base model to be inherited by all generated data classes
    such that they have basic functionality for serializing and
    deserializing json.
    """

    class Config:
        """Config.

        Ignore, allow or forbid extra attributes during model
        initialization. `ignore` will silently ignore any extra
        attributes.
        """

        extra = Extra.ignore

    def dict(self, by_alias=True, **kwargs):
        """Get dict."""
        return super().dict(by_alias=by_alias, **kwargs)

    def json(self, by_alias=True, **kwargs):
        """Pydantic json.

        Pydantic dataclasses do not feature a .json() function.
        So we need to implement it to be able to serialize a to json.
        """
        return super().json(by_alias=by_alias, **kwargs)
