from enum import Enum


class Months(Enum):
    January = 0
    February = 1
    March = 2
    April = 3
    May = 4
    June = 5
    July = 6
    August = 7
    September = 8
    October = 9
    November = 10
    December = 11

    # Sums two int values returning the correspondent Month, taking care of the
    # months' loop between December (12) and January (1)
    @staticmethod
    def sum(first, second):
        result = first + second
        return Months(result % 12)
