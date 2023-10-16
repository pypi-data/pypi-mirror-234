from enum import Enum


class ListQueueResponse200ItemJobKind(str, Enum):
    APPDEPENDENCIES = "appdependencies"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWDEPENDENCIES = "flowdependencies"
    FLOWPREVIEW = "flowpreview"
    IDENTITY = "identity"
    PREVIEW = "preview"
    SCRIPT = "script"
    SCRIPT_HUB = "script_hub"

    def __str__(self) -> str:
        return str(self.value)
