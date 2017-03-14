class WrongFormatException(Exception):
    """
    This class defines the a custom wrong format exception message
    """

    def __init__(self, arg):
        self.error = arg

    def __str__(self):
        return self.error


class MaximumCapacityException(Exception):
    """
        This class defines the a custom maximum capacity exception message
    """

    def __init__(self, arg):
        self.error = "Room {} is filled up, please input another room"\
            .format(arg)

    def __str__(self):
        return self.error


class EligibilityException(Exception):
    """
    This class defines the a custom eligibility exception message
    """

    def __init__(self, arg):
        self.error = arg

    def __str__(self):
        return self.error
