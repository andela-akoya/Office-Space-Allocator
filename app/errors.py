class WrongFormatException(Exception):

    def __init__(self, arg):
        self.error = arg

    def __str__(self):
        return self.error


class MaximumCapacityException(Exception):

    def __init__(self, arg):
        self.error = "Room {} is filled up, please input another room"\
            .format(arg)

    def __str__(self):
        return self.error


class EligibilityException(Exception):

    def __init__(self, arg):
        self.error = arg

    def __str__(self):
        return self.error
