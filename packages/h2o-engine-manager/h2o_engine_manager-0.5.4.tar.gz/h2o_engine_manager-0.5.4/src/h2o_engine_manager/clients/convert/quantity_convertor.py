import re

suffix_values = {
    "Pi": 1 << 50,
    "P": 10**15,
    "Ti": 1 << 40,
    "T": 10**12,
    "Gi": 1 << 30,
    "G": 10**9,
    "Mi": 1 << 20,
    "M": 10**6,
    "Ki": 1 << 10,
    "k": 10**3,
}


def quantity_to_number(quantity: str) -> int:
    """
    Convert string quantity into number by applying the potential suffix.
    [quantity] = [number][suffix]
    [suffix] = [binarySI] | [decimalSI]
    [binarySI] = Ki | Mi | Gi | Ti | Pi
    [decimalSI] = k | M | G | T | P

    Args:
        quantity: string representation of a number with optional suffix.

    Returns:
        number equivalent to the quantity without suffix.

    Raises:
        ValueError: Invalid quantity value passed.

    Examples:
        - "1k" -> 1000
        - "1Ki" -> 1024
        - "1M" -> 1000000
        - "1Mi" -> 1048576
    """
    quantity_regex = re.compile("^[0-9]+(Pi|P|Ti|T|Gi|Mi|Ki|G|M|k)?$")
    if quantity_regex.match(quantity) is None:
        raise ValueError(f"invalid quantity format: {quantity}")

    num_regex = re.compile("^[0-9]+")

    num = int(num_regex.search(quantity).group())
    suffix = num_regex.split(quantity)[1]

    multiplier = 1

    if suffix:
        multiplier = suffix_values.get(suffix)

    return num * multiplier


def number_to_quantity(num: int) -> str:
    """
    Convert number to string quantity. The highest suffix possible will be
    applied. If no suffix can be applied, return the same number without suffix.

    Args:
        num: integer number

    Returns:
        string quantity equivalent to the number

    Examples:
        1000 -> "1k"
        1024 -> "1Ki"
        1000000 -> "1M"
        1048576 -> "1Mi"
        2000 -> "2k"
        2001 -> "2001"
        2048 -> "2Ki"
        2049 -> "2049"
    """
    for suffix in suffix_values.keys():
        multiplier = suffix_values.get(suffix)

        if num % multiplier == 0:
            return f"{int(num / multiplier)}{suffix}"

    return f"{num}"


def quantity_to_number_str(quantity: str) -> str:
    """Helper function to convert return value of `quantity_to_number()` to string representation."""
    return str(quantity_to_number(quantity))


def number_str_to_quantity(bytes_str: str) -> str:
    """Helper function to call `number_to_quantity()` function with a string type argument."""
    return number_to_quantity(int(bytes_str))
