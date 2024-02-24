
class ActiveKid:
    """
    an object of the server that contains information about kids who are active
    """

    def __init__(self, kid_id, mac_address):
        """
        init
        :param kid_id: the id of a kid
        :param mac_address: the mac address of the kid's computer
        """
        self.kid_id = kid_id  # kid id
        self.mac_address = mac_address  # mac address

    def set_kid_id(self, kid_id):
        """
        setter
        :param kid_id: the kid id
        :return: None
        """
        self.kid_id = kid_id

    def get_kid_id(self):
        """
        getter
        :return: return kid id
        """
        return self.kid_id

    def set_mac_address(self, mac_address):
        """
        setter
        :param mac_address: mac address
        :return: None
        """
        self.mac_address = mac_address

    def get_mac_address(self):
        """
        getter
        :return: mac address
        """
        return self.mac_address


