"""
This file is to hold and manage exceptions/exception handling for our project
"""


class MissingFormatSheetError(KeyError):
    """Exception raised if a format sheet is not present.

    Attributes:
        sheet -- The slide the format sheet was intended for
        message -- explanation of the error
    """
    def __init__(self, sheet='', message="No format sheet was found for the given data-sheet"
                                         "\nplease ensure one exists and try again"):
        self.message = message + ": data-sheet = " + sheet
        super().__init__(self.message)


class InvalidFormatSheetError(Exception):
    """Exception raised if a format sheet is invalid.
        e.g. - missing column
             - mis-spelt values

        Attributes:
            sheet -- The slide the format sheet was intended for
            message -- explanation of the error
        """

    def __init__(self, sheet='', message="An invalid format sheet was found for the given data-sheet"
                                         "\nplease check the format sheet and try again"):
        self.message = message + ": data-sheet = " + sheet
        super().__init__(self.message)


class InvalidInputDataError(ValueError):
    """Exception raised if a given input data is invalid.
        e.g. - no data present
             - data out of integer range

        Attributes:
            sheet -- The slide with the invalid data
            message -- explanation of the error
        """

    def __init__(self, sheet='', message="The requested sheet has Invalid data"
                                         "\nplease check the data and try again"):
        self.message = message + ": slide = " + sheet
        super().__init__(self.message)

