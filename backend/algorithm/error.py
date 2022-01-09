class client_capacity_error(Exception):
    "Raised when client demends more than max capacity of truck"

    def __str__(self) -> str:
        return "Demand"


class TWerror(Exception):
    def __str__(self) -> str:
        return "Time Window"
