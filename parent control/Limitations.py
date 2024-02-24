

class Limitations:
    """
    a class that saves the limitations of a kid on the computer
    (used in CurrenKidInfo (of a computers kid client) and Kid (of a parent client))
    """

    def __init__(self, computer_limit, internet_limit):
        """

        :param computer_limit: the computer block limitation ,boolean
        :param internet_limit: the internet block limitation ,boolean
        """
        self._computer_limit = computer_limit
        self._internet_limit = internet_limit


