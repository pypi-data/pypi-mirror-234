from typing import Dict, List
from loguru import logger
import json
import uuid

REFUEL_DATE_FORMAT = "%Y-%m-%d"

VALID_FILTER_OPERATORS = {
    ">",
    "<=",
    "=",
    "<",
    "IS NOT NULL",
    "IS NULL",
    "<>",
    ">=",
    "ILIKE",
    "NOT ILIKE",
    "NOT LIKE",
    "LIKE",
}


def normalize_sort_order(order_direction: str) -> str:
    if order_direction.lower() in ["desc", "descending"]:
        return "DESC"
    else:
        return "ASC"


def format_filters(filters: List[Dict]) -> List[str]:
    formatted_filters = []
    for f in filters:
        field = f.get("field")
        if not field:
            logger.error(f"Error: filter missing field!\nfilter = {f}")
            continue
        operator = f.get("operator")
        if not operator or operator not in VALID_FILTER_OPERATORS:
            logger.error(f"Error: invalid filter operator\nfilter = {f}")
            continue
        value = f.get("value", "")
        filter_type = "label" if field in ["llm_label", "confidence"] else "metadata"
        f_formatted = {
            "filter_type": filter_type,
            "field": field,
            "operator": operator,
            "value": value,
        }
        formatted_filters.append(json.dumps(f_formatted))
    return formatted_filters


def is_valid_uuid(input: str) -> bool:
    if not input:
        return False
    try:
        uuid.UUID(input, version=4)
        return True
    except ValueError:
        return False
