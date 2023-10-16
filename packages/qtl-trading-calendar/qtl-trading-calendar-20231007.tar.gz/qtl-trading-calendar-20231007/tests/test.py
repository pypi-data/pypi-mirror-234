from datetime import date

from qtl_trading_calendar import FuturesTradingCalendar
from qtl_trading_calendar import StockTradingCalendar


def test_futures():
    calendar = FuturesTradingCalendar()

    test_date1 = date(2022, 12, 13)
    print(f'{test_date1=}')

    print(f'{calendar.is_trading_day(test_date1)=}')
    assert calendar.is_trading_day(test_date1)

    print(f'{calendar.has_day_trading(test_date1)=}')
    assert calendar.has_day_trading(test_date1)

    print(f'{calendar.has_night_trading(test_date1)=}')
    assert calendar.has_night_trading(test_date1)

    print(f'{calendar.next_trading_day(test_date1)=}')
    assert calendar.next_trading_day(test_date1) == date(2022, 12, 14)

    print(f'{calendar.previous_trading_day(test_date1)=}')
    assert calendar.previous_trading_day(test_date1) == date(2022, 12, 12)

    test_date2 = date(2022, 12, 10)
    print(f'{test_date2=}')

    print(f'{calendar.is_trading_day(test_date2)=}')
    assert not calendar.is_trading_day(test_date2)

    print(f'{calendar.has_day_trading(test_date2)=}')
    assert not calendar.has_day_trading(test_date2)

    print(f'{calendar.has_night_trading(test_date2)=}')
    assert not calendar.has_night_trading(test_date2)

    print(f'{calendar.next_trading_day(test_date2)=}')
    assert calendar.next_trading_day(test_date2) == date(2022, 12, 12)

    print(f'{calendar.previous_trading_day(test_date2)=}')
    assert calendar.previous_trading_day(test_date2) == date(2022, 12, 9)

    test_date3 = date(2022, 10, 3)
    print(f'{test_date3=}')

    print(f'{calendar.is_trading_day(test_date3)=}')
    assert not calendar.is_trading_day(test_date3)

    print(f'{calendar.has_day_trading(test_date3)=}')
    assert not calendar.has_day_trading(test_date3)

    print(f'{calendar.has_night_trading(test_date3)=}')
    assert not calendar.has_night_trading(test_date3)

    print(f'{calendar.next_trading_day(test_date3)=}')
    assert calendar.next_trading_day(test_date3) == date(2022, 10, 10)

    print(f'{calendar.previous_trading_day(test_date3)=}')
    assert calendar.previous_trading_day(test_date3) == date(2022, 9, 30)


def test_stock():
    calendar = StockTradingCalendar()

    test_date1 = date(2022, 12, 13)
    print(f'{test_date1=}')

    print(f'{calendar.is_trading_day(test_date1)=}')
    assert calendar.is_trading_day(test_date1)

    print(f'{calendar.next_trading_day(test_date1)=}')
    assert calendar.next_trading_day(test_date1) == date(2022, 12, 14)

    print(f'{calendar.previous_trading_day(test_date1)=}')
    assert calendar.previous_trading_day(test_date1) == date(2022, 12, 12)

    test_date2 = date(2022, 12, 10)
    print(f'{test_date2=}')

    print(f'{calendar.is_trading_day(test_date2)=}')
    assert not calendar.is_trading_day(test_date2)

    print(f'{calendar.next_trading_day(test_date2)=}')
    assert calendar.next_trading_day(test_date2) == date(2022, 12, 12)

    print(f'{calendar.previous_trading_day(test_date2)=}')
    assert calendar.previous_trading_day(test_date2) == date(2022, 12, 9)

    test_date3 = date(2022, 10, 3)
    print(f'{test_date3=}')

    print(f'{calendar.is_trading_day(test_date3)=}')
    assert not calendar.is_trading_day(test_date3)

    print(f'{calendar.next_trading_day(test_date3)=}')
    assert calendar.next_trading_day(test_date3) == date(2022, 10, 10)

    print(f'{calendar.previous_trading_day(test_date3)=}')
    assert calendar.previous_trading_day(test_date3) == date(2022, 9, 30)


if __name__ == '__main__':
    test_futures()
    test_stock()
