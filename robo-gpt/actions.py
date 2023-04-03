from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    def key(self) -> str:
        raise NotImplementedError

    def short_string(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class ReadFileAction(Action):
    path: str

    def key(self) -> str:
        return "READ_FILE"

    def short_string(self) -> str:
        return f"Read file `{self.path}`."


@dataclass(frozen=True)
class WriteFileAction(Action):
    path: str
    content: str

    def key(self) -> str:
        return "WRITE_FILE"

    def short_string(self) -> str:
        return f"Write file `{self.path}`."


@dataclass(frozen=True)
class RunPythonAction(Action):
    path: str

    def key(self) -> str:
        return "RUN_PYTHON"

    def short_string(self) -> str:
        return f"Run Python file `{self.path}`."


@dataclass(frozen=True)
class ShutdownAction(Action):
    def key(self):
        return "SHUTDOWN"

    def short_string(self) -> str:
        return f"Shutdown."
