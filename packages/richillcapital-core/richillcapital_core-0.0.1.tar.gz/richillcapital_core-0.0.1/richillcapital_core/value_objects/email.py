from dataclasses import dataclass

from .value_object import ValueObject


@dataclass(frozen=True)
class Email(ValueObject):
    """
    Represents an email address as a value object.

    Args:
        value (str): The email address value.

    Attributes:
        value (str): The email address value.

    """

    value: str

    @staticmethod
    def from_text(address: str) -> "Email":
        """
        Creates an Email object from a given email address string.

        Args:
            address (str): The email address string.

        Returns:
            Email: An Email object representing the provided email address.

        Raises:
            Exception: If the provided email address is invalid.

        """
        if not Email.is_valid_address(address):
            raise Exception("Invalid email.")

        return Email(address)

    @staticmethod
    def is_valid_address(address: str) -> bool:
        """
        Checks if the provided email address string is valid.

        Args:
            address (str): The email address string to validate.

        Returns:
            bool: True if the email address is valid, otherwise False.

        """
        return address is not None and "@" in address
