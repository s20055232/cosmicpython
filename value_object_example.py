from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Money(NamedTuple):
    currency: str
    value: int

    def _is_money(self, that):
        if not isinstance(that, Money):
            raise ValueError("Money can only add Money.")

    def _same_currency(self, that):
        if self.currency != that.currency:
            raise ValueError("Currency can only add the same currency.")

    def _basic_check(self, that):
        self._is_money(that)
        self._same_currency(that)

    def __add__(self, that):
        self._basic_check(that)
        return Money(self.currency, self.value + that.value)

    def __sub__(self, that):
        self._basic_check(that)
        return Money(self.currency, self.value - that.value)

    def __mul__(self, that):
        if not isinstance(that, int):
            raise ValueError
        return Money(self.currency, self.value * that)


Line = namedtuple("Line", ["sku", "qty"])


def test_eqaulity():
    assert Money("gbp", 10) == Money("gbp", 10)
    assert Name("Allen", "Lai") != Name("Allen", "Hsu")
    assert Line("DOG", 4) == Line("DOG", 4)


Fiver = Money("gbp", 5)
Tenner = Money("gbp", 10)


def can_add_money_values_for_the_same_currency():
    tenner = Fiver + Fiver
    assert tenner == Tenner


def can_subtract_money_values():
    assert Tenner - Fiver == Fiver


def adding_differeny_currencies_fails():
    with pytest.raises(ValueError):
        _ = Money("usd", 10) + Money("gbp", 10)


def can_multiply_money_by_a_number():
    assert Fiver * 5 == Money("gbp", 25)


def multiplying_two_money_values_is_an_error():
    with pytest.raises(TypeError):
        _ = Tenner * Fiver


if __name__ == "__main__":
    test_eqaulity()
    can_add_money_values_for_the_same_currency()
    can_subtract_money_values()
    adding_differeny_currencies_fails()
    can_multiply_money_by_a_number()
