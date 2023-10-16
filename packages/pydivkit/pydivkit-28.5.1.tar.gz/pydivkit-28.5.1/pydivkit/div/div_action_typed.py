# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing
from typing import Union

from pydivkit.core import BaseDiv, Expr, Field

from . import (
    div_action_array_insert_value, div_action_array_remove_value,
    div_action_copy_to_clipboard, div_action_focus_element,
    div_action_set_variable,
)


DivActionTyped = Union[
    div_action_array_insert_value.DivActionArrayInsertValue,
    div_action_array_remove_value.DivActionArrayRemoveValue,
    div_action_set_variable.DivActionSetVariable,
    div_action_focus_element.DivActionFocusElement,
    div_action_copy_to_clipboard.DivActionCopyToClipboard,
]
