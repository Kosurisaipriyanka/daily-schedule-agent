from datetime import datetime


def validate_schedule(schedule, tasks):

    errors = []

    # ------------------------------------------------
    # Check which tasks were successfully scheduled
    # ------------------------------------------------

    scheduled_tasks = {
        item["task"]
        for item in schedule
        if item["task"] != "Break"
        and not item.get("unscheduled", False)
    }

    # ------------------------------------------------
    # Check whether every task was scheduled
    # ------------------------------------------------

    for task in tasks:

        if task.name not in scheduled_tasks:

            errors.append(
                f"Task not scheduled: {task.name}"
            )

    items = []

    # ------------------------------------------------
    # Validate each schedule item
    # ------------------------------------------------

    for item in schedule:

        # Unscheduled task
        if item.get("unscheduled", False):

            errors.append(
                f"Could not schedule "
                f"'{item['task']}': "
                f"{item.get('reason', 'Unknown reason')}"
            )

            continue

        try:

            start = datetime.strptime(
                item["start"],
                "%H:%M"
            )

            end = datetime.strptime(
                item["end"],
                "%H:%M"
            )

        except (ValueError, TypeError):

            errors.append(
                f"Invalid time for {item['task']}"
            )

            continue

        # ------------------------------------------------
        # Start must be before end
        # ------------------------------------------------

        if start >= end:

            errors.append(
                f"Invalid time for "
                f"{item['task']}: "
                f"{item['start']} - "
                f"{item['end']}"
            )

        items.append(
            (
                start,
                end,
                item["task"]
            )
        )

    # ------------------------------------------------
    # Check overlapping tasks
    # ------------------------------------------------

    items.sort(
        key=lambda x: x[0]
    )

    for i in range(len(items) - 1):

        current_end = items[i][1]

        next_start = items[i + 1][0]

        if current_end > next_start:

            errors.append(
                f"Overlap: "
                f"{items[i][2]} "
                f"and "
                f"{items[i + 1][2]}"
            )

    return errors