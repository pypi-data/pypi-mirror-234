# MODULES
import os

from pathlib import Path
from typing import Any

# LIBS
from ...libs.io_lib import archive_object, unarchive_object, read_json, save_as_json

# CORE
from core import core


def get_default_save_root() -> str:
    """
    Get the default root directory for saving test files.

    If the "directories/tests/saves" configuration value is set, it will be used as the default root directory.
    Otherwise, the "directories/tmp" configuration value is used with "tests/saves" appended to the end.

    Returns:
        A string representing the default root directory for saving test files.
    """
    default_root = core.config.get("directories/tests/saves", None)
    if default_root is None:
        default_root = (
            core.config.get("directories/tmp", "tmp")
            + os.sep
            + "tests"
            + os.sep
            + "saves"
        )
    return Path(default_root)


class AlphaSave:
    """
    Utility class for saving and loading objects to/from files.
    """

    def __init__(self, root: Path = None, ext: str = ".ast"):
        """
        Initializes a new AlphaSave object with the specified root directory and file extension.

        Args:
            root: The root directory to save files to.
            ext: The file extension to use for saved files.
        """

        self.root = root or self.get_default_save_root()
        self.ext = ext

    @property
    def is_ext_json(self):
        return self.ext == ".json"

    def get_default_save_root(self) -> str:
        """
        Get the default root directory for saving test files.

        If the "directories/tests/saves" configuration value is set, it will be used as the default root directory.
        Otherwise, the "directories/tmp" configuration value is used with "tests/saves" appended to the end.

        Returns:
            A string representing the default root directory for saving test files.
        """
        default_root = core.config.get("directories/tests/saves", None)
        if default_root is None:
            default_root = (
                core.config.get("directories/tmp", "tmp")
                + os.sep
                + "tests"
                + os.sep
                + "saves"
            )
        return Path(default_root)

    def set_root(self, root: str):
        """
        Set the root directory for saving files.

        Args:
            root: The new root directory to use for saving files.
        """
        self.root = root

    def get_file_path(self, filename: str, class_name: str | None = None) -> str:
        """
        Get the file path for a given filename and class name.

        Args:
            filename: The name of the file to get the path for.
            class_name: The name of the class to save the file under.

        Returns:
            The file path for the specified file and class names.
        """
        file_path = os.path.join(self.root, filename + self.ext)
        if class_name is not None:
            file_path = os.path.join(self.root, class_name, filename + self.ext)
        return file_path

    def save(self, object_to_save: Any, filename: str, class_name: str):
        """
        Save an object to a file.

        Args:
            object_to_save: The object to save.
            filename: The name of the file to save the object to.
            class_name: The name of the class to save the object under.
        """
        file_path = self.get_file_path(filename, class_name)
        if os.path.exists(file_path):
            return None

        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        if self.is_ext_json:
            return save_as_json(filename=file_path, data=object_to_save)

        return archive_object(object_to_save, file_path)

    def load(
        self,
        filename: str,
        class_name: str,
    ) -> Any:
        """
        Load an object from a file.

        The file path is constructed based on the root directory, the class name, and the filename.

        Args:
            filename: A string representing the name of the file to load.
            class_name: A string representing the name of the class to which the object belongs.

        Returns:
            The object loaded from the file.
        """
        file_path = self.get_file_path(filename, class_name)

        if self.is_ext_json:
            return read_json(file_path=file_path)

        return unarchive_object(file_path)
