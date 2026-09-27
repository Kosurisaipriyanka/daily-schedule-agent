from datetime import datetime


def validate_schedule(schedule):
    errors = []

    # Convert schedule times into datetime objects
    items = []

    for item in schedule:
        start = datetime.strptime(item["start"], "%H:%M")
        end = datetime.strptime(item["end"], "%H:%M")

        if start >= end:
            errors.append(
                f"Invalid time for {item['task']}: "
                f"{item['start']} - {item['end']}"
            )

        items.append((start, end, item["task"]))

    # Check for overlaps
    items.sort(key=lambda x: x[0])

    for i in range(len(items) - 1):
        current_end = items[i][1]
        next_start = items[i + 1][0]

        if current_end > next_start:
            errors.append(
                f"Overlap: {items[i][2]} and {items[i + 1][2]}"
            )

    return errors