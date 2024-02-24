from Limitations import *


class CurrentKidInfo:
    """
    an object of the computer kid client that contains the information
    of the current active kid on this computer
    """

    def __init__(self):
        self.kid_id = None
        self.kid_username = ""
        self.forbidden_addresses = []
        self.forbidden_applications = []
        self.kid_blocks_limitations = Limitations(False, False)

    def reset(self):
        """
        reset the object for the new kid
        :return:
        """
        self.kid_id = None
        self.kid_username = ""
        self.forbidden_addresses = []
        self.forbidden_applications = []
        self.kid_blocks_limitations = Limitations(False, False)

    # Getters
    def get_kid_id(self):
        """
        getter
        :return: kid id
        """
        return self.kid_id

    def get_kid_username(self):
        """
        getter
        :return: kid username
        """
        return self.kid_username

    def get_forbidden_addresses(self):
        """
        getter
        :return: forbidden addresses
        """
        return self.forbidden_addresses

    def get_forbidden_applications(self):
        """
        getter forbidden applications
        :return:
        """
        return self.forbidden_applications

    def get_kid_blocks_limitations(self):
        """
        getter
        :return: block limitations
        """
        return self.kid_blocks_limitations

    # Setters
    def set_kid_id(self, kid_id):
        """
        setter
        :param kid_id: the kid id
        :return: None
        """
        self.kid_id = kid_id

    def set_kid_username(self, kid_username):
        """
        setter
        :param kid_username: kid username
        :return: None
        """
        self.kid_username = kid_username

    def add_forbidden_address(self, forbidden_address):
        """
        add a forbidden address to the forbidden addresses list
        :param forbidden_address: forbidden address
        :return: None
        """
        self.forbidden_addresses.append(forbidden_address)

    def delete_forbidden_address(self, forbidden_address):
        """
        delete a forbidden address from the forbidden addresses list
        :param forbidden_address: forbidden address
        :return: None
        """
        self.forbidden_addresses.remove(forbidden_address)

    def add_forbidden_application(self, forbidden_application):
        """
        add a forbidden address to the forbidden addresses list
        :param forbidden_application: forbidden application
        :return: None
        """
        self.forbidden_applications.append(forbidden_application)

    def delete_forbidden_application(self, forbidden_application):
        """
        delete a forbidden address from the forbidden addresses list
        :param forbidden_application: forbidden application
        :return: None
        """
        self.forbidden_applications.remove(forbidden_application)

    def set_kid_blocks_limitations(self, kid_blocks_limitations : Limitations):
        """
        setter
        :param kid_blocks_limitations: a list with two boolean
        :return: None
        """
        self.kid_blocks_limitations = kid_blocks_limitations

    def set_forbidden_addresses(self, forbidden_addresses):
        """
        setter
        :param forbidden_addresses: forbidden addresses
        :return: None
        """
        self.forbidden_addresses = forbidden_addresses

    def set_forbidden_applications(self, forbidden_applications):
        """
        setter
        :param forbidden_applications: forbidden applications
        :return: None
        """
        self.forbidden_applications = forbidden_applications


