from typing import Any


def pydantic_loc_to_xpath(location_path: Any) -> Any:
    result = ""
    for loc in location_path:
        if loc == "__root__":
            continue
        if isinstance(loc, int):
            result += f"[{loc}]"
        else:
            result += f"/f:{loc}"

    return result


def pydantic_error_to_operation_issue(error: Any) -> Any:
    loc = pydantic_loc_to_xpath(error["loc"])
    code = "required" if error["type"] == "value_error.missing" else "invalid"
    return {
        "severity": "error",
        "code": code,
        "location": [loc],
        "diagnostics": error["msg"],
    }
