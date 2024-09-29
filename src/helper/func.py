from __future__ import annotations

import importlib
import inspect
import random
import string
from pathlib import Path
from typing import TypeVar

_T = TypeVar("_T")

SPECIAL_CHARACTERS = "!@#$%&"


def import_classes_from_directory(directory: Path | str, base_class: type[_T], package: str) -> list[type[_T]]:
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError(f"Directory {directory} not found or not a directory")

    classes = []
    directory = directory.resolve()
    for file in directory.rglob("*.py"):
        if file.stem.startswith("_"):
            continue

        module_name = file.stem
        module_path = [package]
        if file.parent != directory:
            module_path.append(file.parent.relative_to(directory).as_posix().replace("/", ".").strip("."))
        module_path.append(module_name)
        module_path = ".".join(module_path)
        module = importlib.import_module(module_path)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, base_class) and obj is not base_class and not name.startswith("_"):
                classes.append(obj)

    return classes


def is_strong_password(password: str, /, *, length: int = 8, special: str = SPECIAL_CHARACTERS) -> bool:
    if len(password) < length:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special:
            has_special = True

    return all([has_upper, has_lower, has_digit, has_special])


def generate_strong_password(length: int, /, *, special=SPECIAL_CHARACTERS) -> str:
    characters = string.ascii_letters + string.digits + special
    password = [
        *random.choices(string.ascii_lowercase),
        *random.choices(string.ascii_uppercase),
        *random.choices(string.digits),
        *random.choices(special),
        *random.choices(characters, k=length - 4),
    ]

    random.shuffle(password)
    password = "".join(password)

    return password
