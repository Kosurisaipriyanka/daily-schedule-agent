from datetime import datetime, timedelta
from models import Task


def prioritize_tasks(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda task: task.priority)


def create_schedule(tasks: list[Task], start_time: str = "08:00"):
    fixed_tasks = [
        task for task in tasks
        if task.fixed_start is not None
    ]

    flexible_tasks = [
        task for task in tasks
        if task.fixed_start is None
    ]

    # Sort fixed tasks by start time
    fixed_tasks.sort(key=lambda task: task.fixed_start)

    # Sort flexible tasks by priority
    flexible_tasks = prioritize_tasks(flexible_tasks)

    schedule = []

    # Starting time of the day
    day_start = datetime.strptime(start_time, "%H:%M")

    # Add fixed tasks
    for task in fixed_tasks:
        schedule.append({
            "task": task.name,
            "start": task.fixed_start,
            "end": task.fixed_end,
            "fixed": True
        })

    # Find free time slots
    free_slots = []
    current_time = day_start

    for task in fixed_tasks:

        fixed_start = datetime.strptime(
            task.fixed_start, "%H:%M"
        )

        fixed_end = datetime.strptime(
            task.fixed_end, "%H:%M"
        )

        # Free time before fixed task
        if current_time < fixed_start:
            free_slots.append(
                (current_time, fixed_start)
            )

        current_time = max(current_time, fixed_end)

    # Free time after last fixed task
    day_end = datetime.strptime("23:00", "%H:%M")

    if current_time < day_end:
        free_slots.append(
            (current_time, day_end)
        )

    # Place flexible tasks into free slots
    for task in flexible_tasks:

        duration = timedelta(hours=task.duration)
        placed = False

        for i, (slot_start, slot_end) in enumerate(free_slots):

            # Check if task fits
            if slot_start + duration <= slot_end:

                task_start = slot_start
                task_end = task_start + duration

                # Add task
                schedule.append({
                    "task": task.name,
                    "start": task_start.strftime("%H:%M"),
                    "end": task_end.strftime("%H:%M"),
                    "fixed": False
                })

                # Add 15-minute break after long tasks
                if task.duration >= 2:

                    break_start = task_end
                    break_end = break_start + timedelta(minutes=15)

                    # Make sure break fits
                    if break_end <= slot_end:

                        schedule.append({
                            "task": "Break",
                            "start": break_start.strftime("%H:%M"),
                            "end": break_end.strftime("%H:%M"),
                            "fixed": False
                        })

                        free_slots[i] = (
                            break_end,
                            slot_end
                        )

                    else:
                        free_slots[i] = (
                            task_end,
                            slot_end
                        )

                else:
                    free_slots[i] = (
                        task_end,
                        slot_end
                    )

                placed = True
                break

        # Task couldn't fit anywhere
        if not placed:
            print(
                f"WARNING: Could not schedule "
                f"'{task.name}'"
            )

    # Sort final schedule by start time
    schedule.sort(
        key=lambda item: item["start"]
    )

    return schedule
