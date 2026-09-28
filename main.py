from pydantic import ValidationError

from models import Task
from llm_parser import parse_tasks
from planner import prioritize_tasks, create_schedule
from validator import validate_schedule


print("=== Daily Schedule Agent ===")


# ------------------------------------------------
# 1. Get user input
# ------------------------------------------------

user_input = input(
    "\nDescribe your day: "
)


# ------------------------------------------------
# 2. Gemini extracts tasks
# ------------------------------------------------

task_data = parse_tasks(
    user_input
)


# ------------------------------------------------
# 3. Handle Gemini/API failure
# ------------------------------------------------

if not task_data:

    print(
        "\n❌ Could not create the schedule."
    )

    print(
        "Gemini did not return valid task data."
    )

    exit()


# ------------------------------------------------
# 4. Convert Gemini JSON → Pydantic objects
# ------------------------------------------------

try:

    tasks = [
        Task(**task)
        for task in task_data
    ]

except ValidationError as e:

    print(
        "\n❌ Invalid task data received "
        "from Gemini."
    )

    print(e)

    exit()


# ------------------------------------------------
# 5. Show extracted tasks
# ------------------------------------------------

print(
    "\n=== Tasks Extracted by Gemini ==="
)


for task in tasks:

    print(
        f"{task.name} | "
        f"{task.duration} hours | "
        f"Priority: {task.priority}"
    )


# ------------------------------------------------
# 6. Planning / prioritization
# ------------------------------------------------

print(
    "\n=== Agent's Planned Order ==="
)


planned_tasks = prioritize_tasks(
    tasks
)


for task in planned_tasks:

    print(
        f"{task.name} | "
        f"{task.duration} hours | "
        f"Priority: {task.priority}"
    )


# ------------------------------------------------
# 7. Create schedule
# ------------------------------------------------

print(
    "\n=== Daily Schedule ==="
)


schedule = create_schedule(
    tasks
)


# ------------------------------------------------
# 8. Validate schedule
# ------------------------------------------------

errors = validate_schedule(
    schedule,
    tasks
)


# ------------------------------------------------
# 9. Show errors if any
# ------------------------------------------------

if errors:

    print(
        "\n⚠️ Schedule has issues:"
    )

    for error in errors:

        print(
            "-",
            error
        )


# ------------------------------------------------
# 10. Show schedule
# ------------------------------------------------

print(
    "\n=== Final Schedule ==="
)


for item in schedule:

    if item.get("unscheduled", False):

        print(
            f"❌ {item['task']} → "
            f"NOT SCHEDULED "
            f"({item['reason']})"
        )

    else:

        print(
            f"{item['start']} - "
            f"{item['end']} → "
            f"{item['task']}"
        )