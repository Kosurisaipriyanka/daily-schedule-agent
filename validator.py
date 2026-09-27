from datetime import datetime


def validate_schedule(schedule, tasks):
    errors = []

    # Tasks that were successfully scheduled
    scheduled_tasks = {
        item["task"]
        for item in schedule
        if item["task"] != "Break"
    }

    # Check for unscheduled tasks
    for task in tasks:
        if task.name not in scheduled_tasks:
            errors.append(
                f"Task not scheduled: {task.name}"
            )

    # Convert schedule times
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

    # Check overlaps
    items.sort(key=lambda x: x[0])

    for i in range(len(items) - 1):
        current_end = items[i][1]
        next_start = items[i + 1][0]

        if current_end > next_start:
            errors.append(
                f"Overlap: {items[i][2]} "
                f"and {items[i + 1][2]}"
            )

    return errors