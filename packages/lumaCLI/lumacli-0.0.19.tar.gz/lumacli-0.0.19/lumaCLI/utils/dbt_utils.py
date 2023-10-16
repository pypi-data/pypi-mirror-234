import json
import os
from pathlib import Path
from rich import print
from rich.panel import Panel


def validate_json(json_path: Path, endswith: str = ".json") -> bool:
    """
    Validates the provided file as a valid JSON file with the specified string suffix.

    Args:
        json_path (Path): Full path to the file to be validated.
        endswith (str, optional): Suffix that the file name should have. Defaults to ".json".

    Returns:
        bool: Returns True if validation is successful, False otherwise.
    """
    # Check if file exists
    if not json_path.is_file():
        error_message = (
            f"[red]Error[/red]: [yellow]{json_path.absolute()}[/yellow] "
            f"[blue]is not a file[/blue]"
        )
        print(Panel(error_message))
        return False

    # Check if file name ends with the specified suffix
    if not str(json_path).endswith(endswith):
        error_message = (
            f"[red]Error[/red]: [blue]File[/blue] "
            f"[yellow]{os.path.basename(json_path.absolute())}[/yellow] "
            f"[blue]does not have the required structure, it should end with "
            f"[/blue][yellow]'{endswith}'[/yellow]"
        )

        print(Panel(error_message))
        return False

    return True


def json_to_dict(json_path):
    """
    Converts the provided JSON file to a dictionary.

    Args:
        json_path (str): Full path to the JSON file.

    Returns:
        dict: Returns JSON data as a dictionary.
    """
    try:
        with open(json_path, "r") as json_file:
            # Load JSON data from file
            json_data: dict = json.load(json_file)
    except:
        json_data = None
    return json_data
