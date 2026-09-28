import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_tasks(user_input: str):

    prompt = f"""
You are a task extraction assistant.

Convert the user's request into a JSON array of tasks.

Each task must contain:

- name
- duration (number of hours)
- priority (1=High, 2=Medium, 3=Low)
- fixed_start (HH:MM or null)
- fixed_end (HH:MM or null)

Rules:

1. If the user does not specify a priority, choose a reasonable priority.
2. If a task has no fixed time, use null.
3. Duration must be a positive number.
4. Return ONLY valid JSON.
5. Do not add explanations or markdown.

User request:
{user_input}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        data = json.loads(response.text)

        return data

    except errors.ServerError as e:

        print("\n❌ Gemini server error.")
        print("The Gemini API is currently busy or unavailable.")
        print("Please try again later.")

        return []

    except errors.ClientError as e:

        print("\n❌ Gemini API error.")
        print("Please check your API key or request.")

        return []

    except json.JSONDecodeError:

        print("\n❌ Gemini returned invalid JSON.")

        return []

    except Exception as e:

        print("\n❌ Unexpected error:")
        print(e)

        return []


if __name__ == "__main__":

    user_input = input("Enter your schedule request: ")

    tasks = parse_tasks(user_input)

    print("\n=== Gemini Output ===")

    print(json.dumps(tasks, indent=2))