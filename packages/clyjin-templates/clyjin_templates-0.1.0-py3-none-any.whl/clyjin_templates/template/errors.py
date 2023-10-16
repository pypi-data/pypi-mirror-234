class IncorrectTemplateGroupNameError(Exception):
    def __init__(self, name: str, reason: str) -> None:
        super().__init__(
            f"template group name <{name}> is incorrect: {reason}",
        )
