from dataclasses import dataclass
from typing import Tuple
import actions
import json


@dataclass(frozen=True)
class Metadata:
    criticism: str
    reason: str
    plan: list[str]
    speak: str


def parse(text: str) -> Tuple[actions.Action, Metadata]:
    lines = text.splitlines()
    first_line = lines[0]
    if first_line.startswith("READ_FILE:"):
        action = actions.ReadFileAction(first_line[10:].strip())
        metadata = parse_metadata(lines[1:])
        return action, metadata
    if text.startswith("WRITE_FILE:"):
        path = lines[0][11:].strip()
        assert len(lines) >= 3
        assert lines[1] == "```"
        line_index = 2
        content = ""
        for line in lines[2:]:
            if line == "```":
                break
            line_index += 1
            content += line + "\n"
        # print(content)
        action = actions.WriteFileAction(path=path, content=content)
        metadata = parse_metadata(lines[line_index + 1 :])
        return action, metadata
    if first_line.startswith("RUN_PYTHON:"):
        action = actions.RunPythonAction(first_line[11:].strip())
        metadata = parse_metadata(lines[1:])
        return action, metadata
    if first_line.startswith("SHUTDOWN"):
        action = actions.ShutdownAction()
        metadata = parse_metadata(lines[1:])
        return action, metadata
    raise NotImplementedError(f"Failed to parse response: {text}")


def parse_metadata(lines: list[str]) -> Metadata:
    last_line_index = 1
    for line in lines:
        if line.startswith("}"):
            break
        last_line_index += 1
    metadata_text = "\n".join(lines[:last_line_index]).strip()
    metadata_json = json.loads(metadata_text)
    return Metadata(
        criticism=metadata_json["criticism"],
        reason=metadata_json["reason"],
        plan=metadata_json["plan"],
        speak=metadata_json["speak"],
    )
