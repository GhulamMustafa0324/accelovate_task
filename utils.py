import re


def map_experience_level(exp_str):
    """
    Extracts the first number from exp_str and maps it to an allowed string value ("1" to "5").
    If the number is less than 1, returns "1". If greater than 5, returns "5".
    """
    match = re.search(r"(\d+(\.\d+)?)", exp_str)
    if match:
        exp = float(match.group(1))
        level = int(exp)
        if level < 1:
            level = 1
        elif level > 5:
            level = 5
        return str(level)
    else:
        return "1"  # Default if no number is found


def map_experience_level_indeed(self, exp_str: str) -> str:
    """
    Maps the experience value from the search request to an Indeed experience level.
    - 1 to 2 years: "entryLevel"
    - Greater than 2 up to 6 years: "midLevel"
    - Greater than 6 years: "seniorLevel"
    """
    import re

    match = re.search(r"(\d+(\.\d+)?)", exp_str)
    if match:
        exp = float(match.group(1))
        if exp <= 2:
            return "entryLevel"
        elif exp <= 6:
            return "midLevel"
        else:
            return "seniorLevel"
    else:
        return "entryLevel"  # Default if no number is found
