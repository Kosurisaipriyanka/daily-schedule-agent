from models import Task
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

    fixed_tasks.sort(key=lambda task: task.fixed_start)
    flexible_tasks = prioritize_tasks(flexible_tasks)

    schedule = []

    day_start = datetime.strptime(start_time, "%H:%M")

    # Create fixed-task schedule
    for task in fixed_tasks:
        schedule.append({
            "task": task.name,
            "start": task.fixed_start,
            "end": task.fixed_end,
            "fixed": True
        })

    # Find free slots
    free_slots = []
    current_time = day_start

    for task in fixed_tasks:
        fixed_start = datetime.strptime(task.fixed_start, "%H:%M")
        fixed_end = datetime.strptime(task.fixed_end, "%H:%M")

        if current_time < fixed_start:
            free_slots.append((current_time, fixed_start))

        current_time = max(current_time, fixed_end)

    # Add time after the last fixed task
    free_slots.append(
        (current_time, datetime.strptime("23:00", "%H:%M"))
    )

    # Place flexible tasks into free slots
    for task in flexible_tasks:

        duration = timedelta(hours=task.duration)
        placed = False

        for i, (slot_start, slot_end) in enumerate(free_slots):

            if slot_start + duration <= slot_end:

                task_start = slot_start
                task_end = slot_start + duration

                schedule.append({
                    "task": task.name,
                    "start": task_start.strftime("%H:%M"),
                    "end": task_end.strftime("%H:%M"),
                    "fixed": False
                })

                # Update remaining part of this free slot
                free_slots[i] = (task_end, slot_end)

                placed = True
                break

        if not placed:
            print(f"WARNING: Could not schedule '{task.name}'")

    # Add free-time slots
    schedule.sort(key=lambda item: item["start"])

    free_time = []

    for i in range(len(schedule) - 1):
        current_end = datetime.strptime(schedule[i]["end"], "%H:%M")
        next_start = datetime.strptime(schedule[i + 1]["start"], "%H:%M")

        if current_end < next_start:
            free_time.append({
                "task": "Free Time",
                "start": current_end.strftime("%H:%M"),
                "end": next_start.strftime("%H:%M"),
                "fixed": False
            })

    schedule.extend(free_time)

    schedule.sort(key=lambda item: item["start"])

    return schedule
