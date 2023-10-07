def format_number(value: float, *, format_spec: str = ".1f", parenthesized_negative: bool = True) -> str:
    def format_value(value: float) -> str:
        return format(value, format_spec)

    if parenthesized_negative and value < 0:
        value_str = format_value(abs(value))
        return f"({value_str})"
    return format_value(value)
