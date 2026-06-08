import math
from typing import Any


def parse_boolean(
    value: Any,
    default: bool = False
) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.lower() in {
            "true",
            "1",
            "yes",
            "on"
        }

    if value is None:
        return default

    return bool(value)


def validate_requirements(
    data: dict[str, Any]
) -> tuple[bool, str]:

    required_fields = [
        "plot_width",
        "plot_length",
        "bedrooms",
        "bathrooms"
    ]

    for field in required_fields:
        if field not in data:
            return False, f"{field} is required."

    try:
        plot_width = float(data["plot_width"])
        plot_length = float(data["plot_length"])
        bedrooms = int(data["bedrooms"])
        bathrooms = int(data["bathrooms"])
        floors = int(data.get("floors", 1))

    except (ValueError, TypeError):
        return False, "Please enter valid numerical values."

    if plot_width < 10:
        return False, "Plot width must be at least 10 feet."

    if plot_length < 10:
        return False, "Plot length must be at least 10 feet."

    if bedrooms < 1 or bedrooms > 10:
        return False, "Bedrooms must be between 1 and 10."

    if bathrooms < 1 or bathrooms > 10:
        return False, "Bathrooms must be between 1 and 10."

    if floors < 1 or floors > 5:
        return False, "Floors must be between 1 and 5."

    return True, "Requirements are valid."


def create_room_names(
    data: dict[str, Any]
) -> list[str]:

    room_names: list[str] = []

    if parse_boolean(
        data.get("include_living_room"),
        True
    ):
        room_names.append("Living Room")

    if parse_boolean(
        data.get("include_kitchen"),
        True
    ):
        room_names.append("Kitchen")

    if parse_boolean(
        data.get("include_dining_room")
    ):
        room_names.append("Dining Room")

    if parse_boolean(
        data.get("include_study_room")
    ):
        room_names.append("Study Room")

    bedrooms = int(data["bedrooms"])
    bathrooms = int(data["bathrooms"])

    for number in range(1, bedrooms + 1):
        room_names.append(
            f"Bedroom {number}"
        )

    for number in range(1, bathrooms + 1):
        room_names.append(
            f"Bathroom {number}"
        )

    if parse_boolean(
        data.get("include_parking")
    ):
        room_names.append("Parking")

    if parse_boolean(
        data.get("include_balcony")
    ):
        room_names.append("Balcony")

    return room_names


def generate_blueprint(
    data: dict[str, Any]
) -> dict[str, Any]:

    plot_width = float(data["plot_width"])
    plot_length = float(data["plot_length"])

    room_names = create_room_names(data)

    total_rooms = len(room_names)

    if total_rooms == 0:
        raise ValueError(
            "At least one room must be selected."
        )

    plot_ratio = plot_width / plot_length

    columns = max(
        1,
        math.ceil(
            math.sqrt(
                total_rooms * plot_ratio
            )
        )
    )

    rows = math.ceil(
        total_rooms / columns
    )

    room_width = plot_width / columns
    room_length = plot_length / rows

    rooms: list[dict[str, Any]] = []

    for index, room_name in enumerate(
        room_names
    ):
        column = index % columns
        row = index // columns

        x_position = column * room_width
        y_position = row * room_length

        actual_width = room_width
        actual_length = room_length

        room = {
            "id": index + 1,
            "name": room_name,
            "x": round(x_position, 2),
            "y": round(y_position, 2),
            "width": round(actual_width, 2),
            "length": round(actual_length, 2),
            "area": round(
                actual_width * actual_length,
                2
            ),
            "door": {
                "position": (
                    "bottom"
                    if index % 2 == 0
                    else "left"
                )
            },
            "windows": 1
        }

        rooms.append(room)

    total_area = plot_width * plot_length

    return {
        "project_name": data.get(
            "project_name",
            "My Blueprint"
        ),
        "project_type": data.get(
            "project_type",
            "House"
        ),
        "floors": int(
            data.get("floors", 1)
        ),
        "plot": {
            "width": plot_width,
            "length": plot_length,
            "area": round(total_area, 2),
            "unit": "feet"
        },
        "layout": {
            "rows": rows,
            "columns": columns,
            "total_rooms": total_rooms
        },
        "rooms": rooms
    }