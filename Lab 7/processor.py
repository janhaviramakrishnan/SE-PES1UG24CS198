
import math


def validate_height_and_fastpass(rider_spec):
    # Check whether input is a string
    if not isinstance(rider_spec, str):
        return "Invalid rider specification"

    # Split height and FastPass information
    parts = rider_spec.strip().split(':')

    if len(parts) != 2:
        return "Invalid rider specification"

    height_str, pass_str = parts

    # Validate height
    try:
        height = int(height_str.strip())
    except (ValueError, AttributeError):
        return "Invalid rider height"

    # Validate FastPass
    pass_str = pass_str.strip().upper()
    pass_map = {"YES": True, "NO": False}

    if pass_str not in pass_map or height < 0:
        return "Invalid rider specification"

    has_fastpass = pass_map[pass_str]
    eligible = height >= 120

    status = "FastPass Priority" if has_fastpass else "Standard Entry"

    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    # Check input type
    if not isinstance(ride_metric_str, str):
        return 0.0

    parts = ride_metric_str.split('/')

    if len(parts) != 2:
        return 0.0

    # Convert inputs to floating-point numbers
    try:
        riders = float(parts[0].strip())
        cycle_mins = float(parts[1].strip())
    except (ValueError, TypeError):
        return 0.0

    # Validate numeric values
    if not math.isfinite(riders) or riders < 0:
        return 0.0

    if not math.isfinite(cycle_mins) or cycle_mins <= 0:
        return 0.0

    # Calculate throughput
    try:
        rate = riders / cycle_mins
    except (ZeroDivisionError, OverflowError):
        return 0.0

    if not math.isfinite(rate):
        return 0.0

    return round(rate, 2)


def resolve_safety_restraint_code(zone_code):
    # Check input type
    if not isinstance(zone_code, str):
        return "Unknown restraint code"

    prefix = zone_code.strip().upper()[:3]

    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar"
    }

    return restraint_types.get(prefix, "Unknown restraint code")


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(t_input))

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()
