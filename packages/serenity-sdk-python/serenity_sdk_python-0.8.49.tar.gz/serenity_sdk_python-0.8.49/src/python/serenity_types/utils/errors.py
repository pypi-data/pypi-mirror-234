class ValidationError(ValueError):
    pass


class UserInputException(ValidationError):
    """Exception raised for user input errors to API."""
    pass


class MissingDataException(ValidationError):
    """Exception raised for missing data errors to API."""
    pass
