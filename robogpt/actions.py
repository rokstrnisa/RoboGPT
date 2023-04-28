from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    def key(self) -> str:
        raise NotImplementedError

    def short_string(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class TellUserAction(Action):
    message: str

    def key(self) -> str:
        return "TELL_USER"

    def short_string(self) -> str:
        return f'Tell user "{self.message}".'


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
class SearchOnlineAction(Action):
    query: str

    def key(self) -> str:
        return "SEARCH_ONLINE"

    def short_string(self) -> str:
        return f"Search online for `{self.query}`."


@dataclass(frozen=True)
class ExtractInfoAction(Action):
    url: str
    instructions: str

    def key(self) -> str:
        return "EXTRACT_INFO"

    def short_string(self) -> str:
        return f"Extract info from `{self.url}`: {self.instructions}."


@dataclass(frozen=True)
class ShutdownAction(Action):
    def key(self):
        return "SHUTDOWN"

    def short_string(self) -> str:
        return f"Shutdown."
