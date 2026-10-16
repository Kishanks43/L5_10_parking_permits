"""Campus parking permit management system."""

import json
import random
from datetime import datetime, timedelta


permits = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a parking permit for a vehicle."""
    if zone_records is None:
        zone_records = []

    permit_no = "P" + str(random.randint(10000, 99999))
    expiry = datetime.now() + timedelta(days=180)

    permits[vehicle_plate] = {
        "zone": zone_id,
        "permit": permit_no,
        "expiry": expiry.strftime("%Y-%m-%d"),
    }

    zone_records.append((vehicle_plate, zone_id))
    return permit_no


def revoke_permit(vehicle_plate):
    """Revoke a parking permit for a vehicle."""
    try:
        del permits[vehicle_plate]
    except KeyError:
        return None

    return True


def is_expired(vehicle_plate):
    """Check whether a vehicle's parking permit has expired."""
    try:
        expiry = datetime.strptime(
            permits[vehicle_plate]["expiry"], "%Y-%m-%d"
        )
        return expiry < datetime.now()
    except (KeyError, ValueError):
        return False


def scan_zone(zone_id, plates_seen):
    """Return plates that should be flagged in a parking zone."""
    flagged = []

    for plate in plates_seen:
        if (
            plate not in permits
            or permits[plate]["zone"] != zone_id
            or is_expired(plate)
        ):
            flagged.append(plate)

    return flagged


def load_permit_database(file="permits.json"):
    """Load permit data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as permit_file:
            data = json.load(permit_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    permits.clear()
    permits.update(data)


def save_permit_database(file="permits.json"):
    """Save permit data to a JSON file."""
    with open(file, "w", encoding="utf-8") as permit_file:
        json.dump(permits, permit_file)


def set_expiry(vehicle_plate, date_text):
    """Update the expiry date for a vehicle's permit."""
    permits[vehicle_plate]["expiry"] = date_text


def main():
    """Run the parking permit manager."""
    load_permit_database()

    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")
    register_permit("", "B")
    register_permit(None, "C")

    set_expiry("KA01AB1234", "01/01/2020")

    revoke_permit("MH12ZZ0000")

    print(
        "Flagged in zone A:",
        scan_zone(
            "A",
            ["KA01AB1234", "KA05XY9999", "TN09QQ1111"],
        ),
    )

    plate = input("Plate to revoke (Enter to skip): ")
    revoke_permit(plate)

    save_permit_database()

    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
