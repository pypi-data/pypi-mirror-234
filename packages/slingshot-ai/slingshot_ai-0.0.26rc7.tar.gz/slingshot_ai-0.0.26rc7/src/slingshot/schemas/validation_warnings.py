import warnings
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import cast


class SlingshotValidationWarning(UserWarning):
    pass


class SlingshotDeprecationWarning(SlingshotValidationWarning):
    pass


@dataclass
class SlingshotValidationWarningMessage:
    message: str
    category: type[SlingshotValidationWarning]


def record_validation_warning(warning: SlingshotValidationWarning) -> None:
    """
    Record a warning during validaiton of a schema. This leverages the Python "warnings" framework to record a warning,
    while continuing on with validation, capturing all other potential errors and warnings. The code that triggers the
    validation of a schema can decide how to handle these warnings, using the other helpers in this file, either
    ignoring them, or capturing them explicitly for more structured reporting.
    """
    warnings.warn(warning)


@contextmanager
def catch_validation_warnings() -> Generator[list[SlingshotValidationWarningMessage], None, None]:
    captured_validation_warnings: list[SlingshotValidationWarningMessage] = []
    try:
        with warnings.catch_warnings(record=True) as captured_warnings:
            # Ignore any other warnings that may have been generated during the run (such as from third party code),
            # we're interested only in the validation ones from our code.
            yield captured_validation_warnings
    finally:
        captured_validation_warnings.extend(
            [
                SlingshotValidationWarningMessage(cast(str, warning.message), warning.category)
                for warning in captured_warnings
                if issubclass(warning.category, SlingshotValidationWarning)
            ]
        )
