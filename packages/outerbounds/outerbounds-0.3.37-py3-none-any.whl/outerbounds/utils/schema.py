from enum import Enum


class OuterboundsCommandStatus(Enum):
    OK = "OK"
    FAIL = "FAIL"
    WARN = "WARN"


class CommandStatus:
    def __init__(
        self, name, status=OuterboundsCommandStatus.OK, reason="", mitigation=""
    ):
        self.name = name
        self.status = status
        self.reason = reason
        self.mitigation = mitigation

    def as_dict(self):
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.reason,
            "help": self.mitigation,
        }

    def update(self, status: OuterboundsCommandStatus, reason: str, mitigation: str):
        self.status = status
        self.reason = reason
        self.mitigation = mitigation


class OuterboundsCommandResponse:
    def __init__(self):
        self.status = OuterboundsCommandStatus.OK
        self._code = 200
        self._message = ""
        self._steps = []
        self.metadata = {}

    def add_or_update_metadata(self, key, value):
        self.metadata[key] = value

    def add_step(self, step: CommandStatus):
        self._steps.append(step)
        self._process_step_status(step)

    def _process_step_status(self, step: CommandStatus):
        if step.status == OuterboundsCommandStatus.FAIL:
            self.status = OuterboundsCommandStatus.FAIL
            self._code = 500
            self._message = "We found one or more errors with your installation."
        elif (
            step.status == OuterboundsCommandStatus.WARN
            and self.status != OuterboundsCommandStatus.FAIL
        ):
            self.status = OuterboundsCommandStatus.WARN
            self._code = 200
            self._message = "We found one or more warnings with your installation."

    def as_dict(self):
        return {
            "status": self.status.value,
            "code": self._code,
            "message": self._message,
            "steps": [step.as_dict() for step in self._steps],
            "metadata": self.metadata,
        }
