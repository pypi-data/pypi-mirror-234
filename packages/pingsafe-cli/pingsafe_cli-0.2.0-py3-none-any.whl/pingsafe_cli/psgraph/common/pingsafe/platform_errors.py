class PingSafeAuthError(Exception):
    def __init__(self, message: str = "Authorization error accessing PingSafe.com api. Please check bc-api-key") -> None:
        self.message = message

    def __str__(self) -> str:
        return f"BCAuthError, {self.message} "


class ModuleNotEnabledError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"ModuleNotEnabledError, {self.message} "
