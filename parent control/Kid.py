
from Limitations import Limitations


class Kid:
    """
    an object of the server that contains information about the kids of the parent
    """

    def __init__(self, username):
        self.username = username

        self.forbidden_addresses = []  # list of forbidden addresses
        self.forbidden_applications = []  # list of forbidden applications
        self.forbidden_hours = []  # list of forbidden hours
        self.history = ""  # history of visited addresses
        self.time_limit = "24"  # time limit for usage

        self.kid_id = -1  # kid ID
        self.remaining_time = 24  # Remaining time in hours
        self.active = False  # Kid's activity status
        self.kid_blocks_limitations = Limitations(False, False)  # Kid's limitations


    def setKid(self, kid_id, remaining_time, active, limitations: Limitations):
        """
        set the kid from the server data
        :param kid_id: the id of a kid
        :param remaining_time: the remaining time
        :param active: activity status of a kid
        :param limitations: limitations
        :return:
        """
        self.kid_id = kid_id
        self.remaining_time = remaining_time
        self.active = active
        self.set_limitations(limitations)
        print(f"kid id: {kid_id}, remaining_time: {remaining_time}, active: {active}, limitations: {limitations}")

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_kid_id(self, kid_id):
        self.kid_id = kid_id

    def get_kid_id(self):
        return self.kid_id

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def get_time_limit(self):
        return self.time_limit

    def set_remaining_time(self, remaining_time):
        self.remaining_time = remaining_time

    def get_remaining_time(self):
        return self.remaining_time

    def set_active(self, active):
        self.active = active

    def is_active(self):
        return self.active

    def set_forbidden_addresses(self, forbidden_addresses):
        if forbidden_addresses is not "":
            self.forbidden_addresses = forbidden_addresses.split(",")

    def get_forbidden_addresses(self):
        return self.forbidden_addresses

    def set_forbidden_applications(self, forbidden_applications):
        if forbidden_applications is not "":
            self.forbidden_applications = forbidden_applications.split(",")

    def get_forbidden_applications(self):
        return self.forbidden_applications

    def set_forbidden_hours(self, forbidden_hours):
        if forbidden_hours is not "":
            self.forbidden_hours = forbidden_hours.split(",")

    def get_forbidden_hours(self):
        return self.forbidden_hours

    def set_history(self, history):
        self.history = history

    def get_history(self):
        return self.history

    def set_limitations(self, limitations):
        self.kid_blocks_limitations = limitations

    def get_limitations(self):
        return self.kid_blocks_limitations

    # add and delete methods
    def add_forbidden_address(self, forbidden_address):
        if forbidden_address not in self.forbidden_addresses:
            self.forbidden_addresses.append(forbidden_address)

    def delete_forbidden_address(self, forbidden_address):
        if forbidden_address in self.forbidden_addresses:
            self.forbidden_addresses.remove(forbidden_address)

    def add_forbidden_application(self, forbidden_application):
        if forbidden_application not in self.forbidden_applications:
            self.forbidden_applications.append(forbidden_application)

    def delete_forbidden_application(self, forbidden_application):
        if forbidden_application in self.forbidden_applications:
            self.forbidden_applications.remove(forbidden_application)

    def add_set_of_forbidden_hours(self, set):
        if set not in self.forbidden_hours:
            self.forbidden_hours.append(set)

    def delete_set_of_forbidden_hours(self, set):
        if set in self.forbidden_hours:
            self.forbidden_hours.remove(set)

    def add_address_to_history(self, address):
        self.history = address + "\n" + self.history









