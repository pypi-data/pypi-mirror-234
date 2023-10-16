import pytest

from .validation import validate_to, validate_tos


def test_validate_tos_none() -> None:
    assert validate_tos(None)


def test_validate_tos() -> None:
    assert validate_tos(["alysssa@ben.de"])


@pytest.mark.parametrize(
    "recipient", ["https://chatty.example.com/alyssa", "alyssa@chatty.com"]
)
def test_validate_to_true(recipient: str) -> None:
    assert validate_to(recipient)


@pytest.mark.parametrize(
    "recipient", ["http://chatty.example.com/alyssa", "alyssachatty.com"]
)
def test_validate_to_false(recipient: str) -> None:
    assert not validate_to(recipient)
