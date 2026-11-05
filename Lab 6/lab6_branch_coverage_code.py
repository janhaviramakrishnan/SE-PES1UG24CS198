
import pytest

from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


def test_invalid_groups_type():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5.0)


def test_negative_express_fee():
    with pytest.raises(ValueError):
        process_ride_admissions([], -5.0)


def test_empty_and_closed_groups():
    result = process_ride_admissions([], 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"

    result = process_ride_admissions([{}], 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_roller_coaster_patron_branches():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 119, "health_warning": False},
                {"height_cm": 120, "is_child": True},
                {"height_cm": 160, "is_child": False}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "COMPLETED"
    assert result["total_revenue"] == 40.0


def test_roller_coaster_health_warning_break():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 160, "health_warning": True},
                {"height_cm": 180, "is_child": False}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_water_ride_branches():
    groups = [
        {
            "is_open": True,
            "ride_type": "water_ride",
            "patrons": [
                {"height_cm": 150, "health_warning": True},
                {"height_cm": 110, "health_warning": False},
                {"height_cm": 130, "is_child": True},
                {"height_cm": 170, "is_child": False}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "COMPLETED"
    assert result["total_revenue"] == 28.8


def test_family_ride_and_fast_lane():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "has_fast_lane": True,
            "patrons": [
                {"height_cm": 140, "is_child": True},
                {"height_cm": 160, "is_child": False}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 21.0
    assert result["status"] == "COMPLETED"


def test_unknown_ride_type():
    groups = [
        {
            "is_open": True,
            "ride_type": "haunted_ride",
            "patrons": [{"height_cm": 150}]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_safety_audit_threshold():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "SAFETY_AUDIT"


def test_four_rejections_do_not_trigger_audit():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 150}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "COMPLETED"
    assert result["total_revenue"] == 10.0


def test_no_restraint_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_safe_restraints():
    assert inspect_safety_restraints([[]]) == "SAFE"
    assert inspect_safety_restraints([[1, 0, 1, 0, 1]]) == "SAFE"


def test_emergency_lock():
    assert inspect_safety_restraints([[0, 0]]) == "EMERGENCY_LOCK"
