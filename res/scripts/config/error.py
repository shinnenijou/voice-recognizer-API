from enum import Enum


class EResult(Enum):
    Success = 0
    UnknownError = 1


ErrorString = {
    EResult.Success: "Success",
    EResult.UnknownError: "Unknown error",
}

