import math
from typing import Any


# Approximate minimum conceptual room areas in square feet.
MINIMUM_ROOM_AREAS = {
    "bedroom": 100,
    "bathroom": 35,
    "living_room": 140,
    "kitchen": 80,
    "parking": 140,
    "balcony": 40,
    "dining_room": 90,
    "study_room": 70
}

# Keep some space for walls, passages, ventilation and open areas.
MAXIMUM_SPACE_UTILISATION = 0.85


def parse_boolean(
    value: Any,
    default: bool = False
) -> bool:
    """
    Convert different input values into True or False.
    """

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "1",
            "yes",
            "on"
        }

    if value is None:
        return default

    return bool(value)


def get_positive_number(
    data: dict[str, Any],
    key: str,
    field_name: str
) -> float:
    """
    Read and validate a positive numerical value.
    """

    value = data.get(key)

    if value is None or value == "":
        raise ValueError(
            f"{field_name} is required."
        )

    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{field_name} must be a valid number."
        ) from error

    if number <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return number


def get_positive_integer(
    data: dict[str, Any],
    key: str,
    field_name: str,
    default: int | None = None
) -> int:
    """
    Read and validate a positive integer.
    """

    value = data.get(key, default)

    if value is None or value == "":
        raise ValueError(
            f"{field_name} is required."
        )

    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{field_name} must be a valid whole number."
        ) from error

    if number <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return number


def calculate_required_area(
    data: dict[str, Any]
) -> dict[str, Any]:
    """
    Estimate the minimum area required for all selected rooms.
    """

    bedrooms = int(data.get("bedrooms", 0))
    bathrooms = int(data.get("bathrooms", 0))

    room_areas = {
        "bedrooms": (
            bedrooms
            * MINIMUM_ROOM_AREAS["bedroom"]
        ),
        "bathrooms": (
            bathrooms
            * MINIMUM_ROOM_AREAS["bathroom"]
        ),
        "living_room": (
            MINIMUM_ROOM_AREAS["living_room"]
            if parse_boolean(
                data.get("include_living_room"),
                True
            )
            else 0
        ),
        "kitchen": (
            MINIMUM_ROOM_AREAS["kitchen"]
            if parse_boolean(
                data.get("include_kitchen"),
                True
            )
            else 0
        ),
        "parking": (
            MINIMUM_ROOM_AREAS["parking"]
            if parse_boolean(
                data.get("include_parking")
            )
            else 0
        ),
        "balcony": (
            MINIMUM_ROOM_AREAS["balcony"]
            if parse_boolean(
                data.get("include_balcony")
            )
            else 0
        ),
        "dining_room": (
            MINIMUM_ROOM_AREAS["dining_room"]
            if parse_boolean(
                data.get("include_dining_room")
            )
            else 0
        ),
        "study_room": (
            MINIMUM_ROOM_AREAS["study_room"]
            if parse_boolean(
                data.get("include_study_room")
            )
            else 0
        )
    }

    total_required_area = sum(
        room_areas.values()
    )

    return {
        "room_areas": room_areas,
        "total_required_area": (
            total_required_area
        )
    }


def calculate_project_statistics(
    data: dict[str, Any]
) -> dict[str, Any]:
    """
    Calculate project area and utilisation information.
    """

    plot_width = float(data["plot_width"])
    plot_length = float(data["plot_length"])
    floors = int(data.get("floors", 1))

    plot_area_per_floor = (
        plot_width * plot_length
    )

    total_available_area = (
        plot_area_per_floor * floors
    )

    area_information = (
        calculate_required_area(data)
    )

    required_area = area_information[
        "total_required_area"
    ]

    recommended_usable_area = (
        total_available_area
        * MAXIMUM_SPACE_UTILISATION
    )

    remaining_area = max(
        total_available_area - required_area,
        0
    )

    utilisation_percentage = (
        required_area
        / total_available_area
        * 100
        if total_available_area > 0
        else 0
    )

    recommended_utilisation = (
        required_area
        / recommended_usable_area
        * 100
        if recommended_usable_area > 0
        else 0
    )

    return {
        "plot_area_per_floor": round(
            plot_area_per_floor,
            2
        ),
        "total_available_area": round(
            total_available_area,
            2
        ),
        "recommended_usable_area": round(
            recommended_usable_area,
            2
        ),
        "estimated_required_area": round(
            required_area,
            2
        ),
        "remaining_area": round(
            remaining_area,
            2
        ),
        "space_utilisation": round(
            utilisation_percentage,
            2
        ),
        "recommended_space_used": round(
            recommended_utilisation,
            2
        ),
        "room_area_breakdown": (
            area_information["room_areas"]
        )
    }


def validate_requirements(
    data: dict[str, Any]
) -> tuple[bool, str]:
    """
    Validate user inputs and check whether rooms
    can fit inside the available plot area.
    """

    required_fields = [
        "plot_width",
        "plot_length",
        "bedrooms",
        "bathrooms"
    ]

    for field in required_fields:
        if field not in data:
            return False, (
                f"{field.replace('_', ' ').title()} "
                "is required."
            )

    try:
        plot_width = get_positive_number(
            data,
            "plot_width",
            "Plot width"
        )

        plot_length = get_positive_number(
            data,
            "plot_length",
            "Plot length"
        )

        bedrooms = get_positive_integer(
            data,
            "bedrooms",
            "Bedrooms"
        )

        bathrooms = get_positive_integer(
            data,
            "bathrooms",
            "Bathrooms"
        )

        floors = get_positive_integer(
            data,
            "floors",
            "Floors",
            default=1
        )

        if plot_width < 10:
            return False, (
                "Plot width must be at least "
                "10 feet."
            )

        if plot_length < 10:
            return False, (
                "Plot length must be at least "
                "10 feet."
            )

        if bedrooms > 20:
            return False, (
                "The maximum supported number "
                "of bedrooms is 20."
            )

        if bathrooms > 20:
            return False, (
                "The maximum supported number "
                "of bathrooms is 20."
            )

        if floors > 5:
            return False, (
                "The maximum supported number "
                "of floors is 5."
            )

        plot_area_per_floor = (
            plot_width * plot_length
        )

        total_available_area = (
            plot_area_per_floor * floors
        )

        recommended_usable_area = (
            total_available_area
            * MAXIMUM_SPACE_UTILISATION
        )

        area_information = (
            calculate_required_area(data)
        )

        required_area = area_information[
            "total_required_area"
        ]

        if required_area > recommended_usable_area:
            return False, (
                f"The selected rooms require approximately "
                f"{required_area:.0f} sq.ft, but this project "
                f"has only {recommended_usable_area:.0f} sq.ft "
                "of recommended usable space. Increase the plot "
                "size, add another floor, or reduce the number "
                "of rooms."
            )

        return True, (
            "Requirements are valid and the "
            "selected rooms can fit."
        )

    except ValueError as error:
        return False, str(error)

    except (
        TypeError,
        OverflowError,
        ZeroDivisionError
    ):
        return False, (
            "One or more input values are invalid."
        )


def create_room_names(
    data: dict[str, Any]
) -> list[str]:
    """
    Create a list of room names using user requirements.
    """

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

    for number in range(
        1,
        bedrooms + 1
    ):
        room_names.append(
            f"Bedroom {number}"
        )

    for number in range(
        1,
        bathrooms + 1
    ):
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
    """
    Generate the conceptual blueprint layout.
    """

    plot_width = float(
        data["plot_width"]
    )

    plot_length = float(
        data["plot_length"]
    )

    floors = int(
        data.get("floors", 1)
    )

    room_names = create_room_names(data)

    total_rooms = len(room_names)

    if total_rooms == 0:
        raise ValueError(
            "At least one room must be selected."
        )

    plot_ratio = (
        plot_width / plot_length
    )

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

    room_width = (
        plot_width / columns
    )

    room_length = (
        plot_length / rows
    )

    rooms: list[dict[str, Any]] = []

    for index, room_name in enumerate(
        room_names
    ):
        column = index % columns
        row = index // columns

        x_position = (
            column * room_width
        )

        y_position = (
            row * room_length
        )

        room = {
            "id": index + 1,
            "name": room_name,
            "x": round(
                x_position,
                2
            ),
            "y": round(
                y_position,
                2
            ),
            "width": round(
                room_width,
                2
            ),
            "length": round(
                room_length,
                2
            ),
            "area": round(
                room_width * room_length,
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

    plot_area = (
        plot_width * plot_length
    )

    statistics = (
        calculate_project_statistics(data)
    )

    return {
        "project_name": data.get(
            "project_name",
            "My Blueprint"
        ),
        "project_type": data.get(
            "project_type",
            "House"
        ),
        "floors": floors,
        "plot": {
            "width": plot_width,
            "length": plot_length,
            "area": round(
                plot_area,
                2
            ),
            "unit": "feet"
        },
        "layout": {
            "rows": rows,
            "columns": columns,
            "total_rooms": total_rooms
        },
        "statistics": statistics,
        "rooms": rooms
    }