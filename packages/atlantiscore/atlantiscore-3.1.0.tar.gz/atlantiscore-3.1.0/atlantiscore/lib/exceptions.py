class InvalidEVMAddress(RuntimeError):
    def __init__(self, invalid_value: any) -> None:
        super().__init__(
            f"{invalid_value} is not transformable to a valid EVM address."
        )
