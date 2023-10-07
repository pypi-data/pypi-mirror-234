class AuthenticationError(Exception):
    """Exception raised for errors in Authentication class.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Check user email or password"):
        self.message = message
        super().__init__(self.message)


class MessagesError(Exception):
    """Exception raised for errors in Message class.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Returned not 200 code"):
        self.message = message
        super().__init__(self.message)
