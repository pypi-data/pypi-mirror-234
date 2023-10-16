import os
import sys

import pytest

sys.path.append(os.getcwd())

from richillcapital_core.value_objects.email import Email


class TestEmail:
    def test_from_text_valid_email(self):
        valid_email = "test@example.com"
        email = Email.from_text(valid_email)
        assert email.value == valid_email

    def test_from_text_invalid_email(self):
        with pytest.raises(Exception) as excinfo:
            Email.from_text("invalid.email")
        assert "Invalid email." in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            Email.from_text("noatsign.com")
        assert "Invalid email." in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            Email.from_text("")
        assert "Invalid email." in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            Email.from_text(None)  # type: ignore
        assert "Invalid email." in str(excinfo.value)

    def test_equals_two_equal_emails(self):
        address = "test@example.com"
        email1 = Email.from_text(address)
        email2 = Email.from_text(address)

        assert email1 == email2

    def test_equals_two_different_emails(self):
        email1 = Email.from_text("test@example.com")
        email2 = Email.from_text("another@example.com")

        assert email1 != email2
