# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field


# The image is mirrored if the RTL (Right-to-Left) direction is specified in the
# system.
class DivFilterRtlMirror(BaseDiv):

    def __init__(
        self, *,
        type: str = "rtl_mirror",
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            **kwargs,
        )

    type: str = Field(default="rtl_mirror")


DivFilterRtlMirror.update_forward_refs()
