import datetime as dt

from dataclasses import dataclass

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import dates
from hypothesis.strategies import integers

'''
Assume the following requirement:

    Each year every customer receives a notification on his/her birthday.

A method `is_birthday` is implemented to check if a customer has birthday in a given year.

The requirement cannot be fulfilled for customers born in leap years on February 29.

The lack of further specification is detected by the test below.

'''


@dataclass
class Customer:
    date_of_birth: dt.date

    def is_birthday(self, today):
        return self.date_of_birth.month == today.month \
            and self.date_of_birth.day == today.day


@given(dates(min_value=dt.date(1901, 1, 1),
             max_value=dt.date(2022, 2, 22)),
       integers(min_value=2023,
                max_value=2050))
@settings(max_examples=10000)
def test_has_birthday_in_given_year(date_of_birth, year):
    """Finds falsifying test: date_of_birth = datetime.date(2000, 2, 29), year = 2023

    """
    c = Customer(date_of_birth)
    assert (any(c.is_birthday(day) for day in days_of_year(year)))


def days_of_year(y):
    start = dt.date(y, 1, 1)
    end = dt.date(y, 12, 31)
    return (start + dt.timedelta(days=x) for x in range(0, (end - start).days + 1))
