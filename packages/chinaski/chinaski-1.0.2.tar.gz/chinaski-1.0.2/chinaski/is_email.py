import re
from dataclasses import dataclass
from typing import Optional

email_regex = re.compile(
    r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]{2,}(?:[a-z0-9-]*[a-z0-9])?"  # noqa: E501
)


@dataclass
class Result:
    """Consists of a result after finding (or not) and email."""

    is_email: bool
    email: str
    line_number: int
    file_name: str

    def __str__(self):
        return f"{self.line_number} - {self.email} - {self.file_name}"


def is_email(line: str, line_number: int, file_name: str) -> Optional[Result]:
    """Detects if a given text is an email or not and returns a Result if so,
    None otherwise.

    :param line: text that might be an email
    :param line_number: line number where the email is at
    :param file_name: name of the file the email is at
    :return: Result object if line is email, None otherwise
    """
    if re.fullmatch(email_regex, line):
        return Result(is_email=True, email=line, line_number=line_number, file_name=file_name)
    return None
