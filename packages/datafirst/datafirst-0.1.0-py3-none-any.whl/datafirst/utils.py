import re
import unicodedata


def full_name_to_first_and_last_name(full_name: str) -> tuple[str, str]:
    """Convert a person's full name to a first and last name."""
    split_name = full_name.split(" ")
    if len(split_name) == 1:
        return split_name[0], ""
    elif len(split_name) == 2:
        return split_name[0], split_name[1]
    elif len(split_name) == 3:
        return split_name[0], " ".join(split_name[1:])
    else:
        return " ".join(split_name[:2]), " ".join(split_name[2:])


def sanitanize_name(name: str) -> str:
    """Sanitize a name for use in a directory name."""
    # remove non-alphanumeric characters ignore the - character
    name = unicodedata.normalize("NFD", name).encode("utf8", "strict").decode()
    name = re.sub(r"[^\w\s-]", "", name)
    name = name.replace(" ", "-")
    return name


def people_name_to_directory_name(full_name: str) -> str:
    """Convert a person's name to a directory name."""
    return sanitanize_name(full_name).lower()
