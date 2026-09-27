from models import Task


def prioritize_tasks(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda task: task.priority)


def create_schedule(tasks: list[Task], start_hour: float = 8):
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

    # Add flexible tasks around fixed tasks
    current_hour = start_hour

    for task in flexible_tasks:

        placed = False

        for fixed in fixed_tasks:

            fixed_start = int(fixed.fixed_start[:2])
            fixed_end = int(fixed.fixed_end[:2])

            # If task would overlap fixed activity,
            # move it after the fixed activity
            if current_hour < fixed_end:
                if current_hour + task.duration > fixed_start:
                    current_hour = fixed_end

        start = current_hour
        end = current_hour + task.duration

        schedule.append({
            "task": task.name,
            "start": f"{int(start):02d}:00",
            "end": f"{int(end):02d}:00",
            "fixed": False
        })

        current_hour = end
    # Add a break after long tasks
    if task.duration >= 2:
        break_start = end
        break_end = end + 0.25

        schedule.append({
            "task": "Break",
            "start": f"{int(break_start):02d}:{int((break_start % 1) * 60):02d}",
            "end": f"{int(break_end):02d}:{int((break_end % 1) * 60):02d}",
            "fixed": False
        })

        current_hour = break_end
    else:
        current_hour = end
    # Add fixed tasks
    for task in fixed_tasks:
        schedule.append({
            "task": task.name,
            "start": task.fixed_start,
            "end": task.fixed_end,
            "fixed": True
        })

    # Sort final schedule by starting time
    schedule.sort(key=lambda item: item["start"])

    return schedule