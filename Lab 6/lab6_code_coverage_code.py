
import pytest

from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


def test_invalid_groups():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5.0)


def test_negative_express_fee():
    with pytest.raises(ValueError):
        process_ride_admissions([], -5.0)


def test_closed_ride():
    groups = [{"is_open": False, "ride_type": "family"}]
    result = process_ride_admissions(groups, 5.0)
    assert result["status"] == "ZERO_ADMISSIONS"


def test_all_ride_types_and_patron_conditions():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 150, "health_warning": True},
                {"height_cm": 160, "is_child": False}
            ]
        },
        {
            "is_open": True,
            "ride_type": "water_ride",
            "patrons": [
                {"height_cm": 150, "health_warning": True},
                {"height_cm": 100},
                {"height_cm": 130, "is_child": True},
                {"height_cm": 170, "is_child": False}
            ]
        },
        {
            "is_open": True,
            "ride_type": "family",
            "has_fast_lane": True,
            "patrons": [
                {"height_cm": 140, "is_child": True},
                {"height_cm": 160, "is_child": False}
            ]
        },
        {
            "is_open": True,
            "patrons": [
                {"height_cm": 150}
            ]
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["status"] == "COMPLETED"
    assert result["total_revenue"] > 0


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


def test_safety_audit():
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


def test_zero_admissions():
    result = process_ride_admissions([], 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_no_restraint_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_emergency_lock():
    readings = [[1, 0, 0, 1]]
    assert inspect_safety_restraints(readings) == "EMERGENCY_LOCK"


def test_safe_restraints():
    readings = [
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1]
    ]

    assert inspect_safety_restraints(readings) == "SAFE"
