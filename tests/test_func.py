from __future__ import annotations

from pathlib import Path

from helper import func
from tests.mock.commands._base import Command


def test_import_classes_from_directory():
    directory = Path(__file__).parent / "mock" / "commands"
    classes = func.import_classes_from_directory(directory, Command, "tests.mock.commands")
    assert len(classes) == 4
    assert all(issubclass(cls, Command) for cls in classes)


def test_import_classes_from_directory_not_found():
    directory = Path(__file__).parent / "mock" / "not_found"
    try:
        func.import_classes_from_directory(directory, Command, "tests.mock.commands")
    except ValueError as e:
        assert str(e) == f"Directory {directory} not found or not a directory"
    else:
        raise AssertionError("Expected ValueError")


def test_is_strong_password():
    assert func.is_strong_password("Password1!", length=8)
    assert not func.is_strong_password("password1!", length=8)
    assert not func.is_strong_password("Password!", length=8)
    assert not func.is_strong_password("Password1", length=10)
    assert not func.is_strong_password("password1!", length=8)
    assert not func.is_strong_password("Password!", length=8)
    assert not func.is_strong_password("Password1", length=8, special="")
    assert not func.is_strong_password("Password1!", length=8, special="")
    assert not func.is_strong_password("password1!", length=8, special="")
    assert not func.is_strong_password("Password!", length=8, special="")
    assert not func.is_strong_password("Password1", length=10, special="")
    assert not func.is_strong_password("password1!", length=8, special="")
    assert not func.is_strong_password("Password!", length=8, special="")
    assert not func.is_strong_password("Password1", length=8, special="!@#$%&")
    assert not func.is_strong_password("Password1*", length=8, special="!@#$%&")
    assert not func.is_strong_password("Password!", length=8, special="!@#$%&")
    assert not func.is_strong_password("Password1", length=10, special="!@#$%&")
    assert not func.is_strong_password("password1!", length=8, special="!@#$%&")
    assert not func.is_strong_password("Password!", length=8, special="!@#$%&")


def test_generate_strong_password():
    password = func.generate_strong_password(8)
    assert func.is_strong_password(password)
    assert len(password) == 8
    password = func.generate_strong_password(16)
    assert func.is_strong_password(password)
    assert len(password) == 16
    password = func.generate_strong_password(12, special="!@#$%&*")
    assert func.is_strong_password(password, special="!@#$%&*")
    assert len(password) == 12
    password = func.generate_strong_password(16, special="!@#$%&*")
    assert func.is_strong_password(password, special="!@#$%&*")
    assert len(password) == 16
