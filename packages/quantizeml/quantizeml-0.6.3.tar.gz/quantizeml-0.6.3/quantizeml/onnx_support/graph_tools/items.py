#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
__all__ = ["find_by_name", "set_by_name"]


def find_by_name(item_name, item_list):
    """Helper function to find item by name in a list.

    Args:
        item_name (str): name of the item.
        item_list (list of Object): list of items.

    Returns:
        Object: item if found, None otherwise.
    """
    items = [item for item in item_list if item.name == item_name]
    assert len(items) < 2, "Duplicate elements found !"
    return items[0] if len(items) > 0 else None


def set_by_name(item_name, item_list, new_item):
    """Helper function to set an item into the list in the position
    which name matches.

    Args:
        item_name (str): name of the item.
        item_list (list of Object): list of items.
        new_item (Object): new item. the type must match with other items.
    """
    old_item = [(idx, item) for idx, item in enumerate(item_list) if item.name == item_name]
    if len(old_item) != 1:
        raise ValueError(f"Impossible to replace {item_name}: duplicated or missing in item list!")
    idx, old_item = old_item[0]
    assert type(old_item) == type(new_item), f"Incompatible type. Expected {type(old_item)}."
    # Update new element in list, avoiding direct assignment
    item_list.pop(idx)
    item_list.insert(idx, new_item)
