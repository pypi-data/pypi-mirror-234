import re
from typing import Union


def prettyprint_number(number: int, n_significant_figures: int = 4) -> str:
    n_digits = len(f'{number:.0f}')
    return f'{round(number, n_significant_figures - n_digits):,}'


def _compute_hash(string: str) -> Union[int, str]:
    hash_value = 0
    if not string:
        return hash_value
    for c in string:
        hash_value = ((hash_value << 5) - hash_value) + ord(c)
        hash_value = hash_value & 0xFFFFFFFF  # Convert to 32bit integer
    return str(hash_value)


def sanitized_name(name: str) -> str:
    if name.isnumeric():
        name = f'_{name}'
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
    if len(name) > 63:
        suffix = f'_{_compute_hash(name)}'
        name = f'{name[0: 63 - len(suffix)]}{suffix}'
    return name


def validate_sanitized_names(
    columns: Union[list, str], sanitized_name_dict: dict
) -> None:
    if not columns:
        return
    if isinstance(columns, str):
        columns = [columns]
    for column in columns:
        sname = sanitized_name(column.name)
        if sname in sanitized_name_dict:
            other_name = sanitized_name_dict.get(sname)
            raise ValueError(
                f'Name conflict, {column.name} and {other_name} '
                f'both maps to {sname}'
            )
        else:
            sanitized_name_dict[sname] = column.name
