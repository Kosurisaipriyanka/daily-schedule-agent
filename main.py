from models import Task
from planner import prioritize_tasks, create_schedule
from validator import validate_schedule

tasks = []

print("=== Daily Schedule Agent ===")

while True:
    name = input("\nEnter task name (or 'done' to finish): ")

    if name.lower() == "done":
        break

    duration = float(input("Enter duration in hours: "))
    priority = int(input("Enter priority (1=High, 2=Medium, 3=Low): "))
    fixed = input("Is this a fixed-time task? (y/n): ")

    if fixed.lower() == "y":
        fixed_start = input("Enter start time (HH:MM): ")
        fixed_end = input("Enter end time (HH:MM): ")
    else:
        fixed_start = None
        fixed_end = None

    task = Task(
        name=name,
        duration=duration,
        priority=priority,
        fixed_start=fixed_start,
        fixed_end=fixed_end
    )

    tasks.append(task)


print("\n=== Agent's Planned Order ===")

planned_tasks = prioritize_tasks(tasks)

for task in planned_tasks:
    print(
        f"{task.name} | "
        f"{task.duration} hours | "
        f"Priority: {task.priority}"
    )

print("\n=== Daily Schedule ===")

schedule = create_schedule(tasks)

errors = validate_schedule(schedule)

if errors:
    print("\n❌ Schedule has errors:")

    for error in errors:
        print("-", error)

else:
    print("\n✅ Schedule is valid!")

    for item in schedule:
        print(
            f"{item['start']} - "
            f"{item['end']} → "
            f"{item['task']}"
        )