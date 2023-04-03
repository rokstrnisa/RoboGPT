import io
import subprocess
import actions


def run(action: actions.Action) -> str:
    try:
        if isinstance(action, actions.ReadFileAction):
            with io.open(action.path, mode="r", encoding="utf-8") as file:
                contents = file.read()
                print(f"RESULT: Read file `{action.path}`.")
                return contents
        if isinstance(action, actions.WriteFileAction):
            with io.open(action.path, mode="w", encoding="utf-8") as file:
                file.write(action.content)
                print(f"RESULT: Wrote file `{action.path}`.")
                return "File successfully written."
        if isinstance(action, actions.RunPythonAction):
            with subprocess.Popen(
                f"python {action.path}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            ) as process:
                process.wait()
                output = process.stdout.read() if process.stdout else ""
                print(f"RESULT: Ran Python file `{action.path}`.")
                return output
        raise NotImplementedError(f"Failed to run action: {action}")
    except Exception as e:
        return f"Error: {e}"
