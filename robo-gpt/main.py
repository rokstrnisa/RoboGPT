import os
from dotenv import load_dotenv
from spinner import Spinner
import actions
import response_parser
import action_runner
import speech
import gpt


message_history = []
result = None


general_directions = """
Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications.


CONSTRAINTS:
1. No user assistance.
2. Cannot run Python code that requires user input.


ACTIONS:

1. "READ_FILE": read the current state of a file. The schema for the action is:

READ_FILE: <PATH>

2. "WRITE_FILE": write a block of text to a file. The schema for the action is:

WRITE_FILE: <PATH>
```
<TEXT>
```

3. "RUN_PYTHON": run a Python file. The schema for the action is:

RUN_PYTHON: <PATH>

4. "SHUTDOWN": shut down the program. The schema for the action is:

SHUTDOWN


RESOURCES:
1. File contents after reading file.
2. Code evaluation results.
3. Improved code.
4. Output of running a Python file.


PERFORMANCE EVALUATION:
1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities. 
2. Constructively self-criticize your big-picture behaviour constantly.
3. Reflect on past decisions and strategies to refine your approach.
4. Every action has a cost, so be smart and efficent. Aim to complete tasks in the least number of steps.


Write only one action. The action must one of the actions specified above and must be written according to the schema specified above.

After the action, also write the following metadata JSON object, which must be parsable by Python's json.loads():
{
    "criticism": "<constructive self-criticism of actions performed so far, if any>",
    "reason": "<a sentence explaining the action above>",
    "plan": "<a short high-level plan in plain English>",
    "speak": "<a short summary of thoughts to say to the user>"
}

Do not write anything else.
"""

user_input = "Determine which next action to use, and write one valid action, a newline, and one valid metadata JSON object, both according to the specified schema:"


def main():
    user_directions = input("What would you like me to do:\n")
    load_dotenv()
    os.chdir("workspace")
    while True:
        print("========================")
        with Spinner("Thinking... "):
            assistant_response = gpt.chat(user_directions, general_directions, user_input, message_history)
        action, metadata = response_parser.parse(assistant_response)
        print(f"ACTION: {action.short_string()}")
        # Comment out below if you don't want to use speech.
        speech.say_async(metadata.speak)
        if isinstance(action, actions.ShutdownAction):
            print("Shutting down...")
            break
        else:
            print(f"REASON: {metadata.reason}")
            print(f"PLAN: {metadata.plan}")
            if metadata.criticism.strip() != "":
                print(f"SELF-CRITICISM: {metadata.criticism}")
        # Comment out the 3 lines below to remove the confirmation step before running the action.
        # run_action = input("Run the action? [Y/n]")
        # if run_action.lower() != "y" and run_action != "":
        #     break
        action_output = action_runner.run(action)
        message_content = f"Action {action.key()} returned:\n{action_output}"
        message_history.append({"role": "system", "content": message_content})


if __name__ == "__main__":
    main()
