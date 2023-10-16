from typing import Any, List


def get_first_element_or_null(lst: List[Any]) -> Any:
    return lst[0] if lst is not None and len(lst) > 0 else None
