
import pytest
from hypothesis import given, strategies as st

from processor import (
    validate_height_and_fastpass,
    compute_dispatch_throughput,
    resolve_safety_restraint_code
)


# Test 1: validate_height_and_fastpass
@given(st.one_of(st.text(), st.none()))
def test_validate_height_and_fastpass_no_crash(s):

    try:
        result = validate_height_and_fastpass(s)

        assert isinstance(result, str)

    except Exception as e:
        pytest.fail(
            f"validate_height_and_fastpass crashed with input {s!r}: {e}"
        )


# Test 2: compute_dispatch_throughput
@given(st.one_of(st.text(), st.none()))
def test_compute_dispatch_throughput_safe(s):

    try:
        result = compute_dispatch_throughput(s)

        assert isinstance(result, float)
        assert result >= 0

    except Exception as e:
        pytest.fail(
            f"compute_dispatch_throughput crashed with input {s!r}: {e}"
        )


# Test 3: resolve_safety_restraint_code
@given(st.one_of(st.text(), st.none()))
def test_resolve_safety_restraint_code_safe(s):

    try:
        result = resolve_safety_restraint_code(s)

        assert isinstance(result, str)

    except Exception as e:
        pytest.fail(
            f"resolve_safety_restraint_code crashed with input {s!r}: {e}"
        )


# Additional tests for valid inputs
def test_valid_height_and_fastpass():
    assert validate_height_and_fastpass("140:YES") == \
        "Height 140cm: Approved (FastPass Priority)"


def test_valid_throughput():
    assert compute_dispatch_throughput("48/2.5") == 19.2


def test_valid_restraint_code():
    assert resolve_safety_restraint_code("CST_01") == \
        "Over-the-Shoulder Harness"
