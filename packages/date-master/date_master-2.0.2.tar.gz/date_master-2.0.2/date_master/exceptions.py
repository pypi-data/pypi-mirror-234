class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidDayError(Error):
    """Raised when the day is not valid"""
    pass


class InvalidMonthError(Error):
    """Raised when the month is not valid"""
    pass


class InvalidYearError(Error):
    """Raised when the year is not valid"""
    pass


class InvalidDateError(Error):
    """Raised when the date is not valid"""
    pass