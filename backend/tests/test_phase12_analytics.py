from datetime import date, datetime, timedelta

from app.services.analytics_service import (
    _build_periods,
    _period_is_partial,
)


def test_iso_week_period_starts_on_monday():
    periods = _build_periods(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 10),
        granularity="weekly",
    )

    assert periods[0][0].weekday() == 0
    assert periods[0][0] == date(2025, 12, 29)


def test_iso_week_year_boundary():
    periods = _build_periods(
        start_date=date(2025, 12, 29),
        end_date=date(2026, 1, 4),
        granularity="weekly",
    )

    assert len(periods) == 1
    assert periods[0][0] == date(2025, 12, 29)
    assert periods[0][1] == date(2026, 1, 4)


def test_month_period():
    periods = _build_periods(
        start_date=date(2026, 2, 10),
        end_date=date(2026, 4, 5),
        granularity="monthly",
    )

    assert periods[0] == (
        date(2026, 2, 1),
        date(2026, 2, 28),
    )

    assert periods[1] == (
        date(2026, 3, 1),
        date(2026, 3, 31),
    )


def test_leap_year_month():
    periods = _build_periods(
        start_date=date(2028, 2, 1),
        end_date=date(2028, 2, 29),
        granularity="monthly",
    )

    assert periods == [
        (
            date(2028, 2, 1),
            date(2028, 2, 29),
        )
    ]


def test_partial_period_detection():
    assert _period_is_partial(
        period_start=date(2026, 10, 5),
        period_end=date(2026, 10, 11),
        selected_start=date(2026, 10, 7),
        selected_end=date(2026, 10, 10),
    ) is True


def test_complete_period_detection():
    assert _period_is_partial(
        period_start=date(2026, 10, 5),
        period_end=date(2026, 10, 11),
        selected_start=date(2026, 10, 5),
        selected_end=date(2026, 10, 11),
    ) is False