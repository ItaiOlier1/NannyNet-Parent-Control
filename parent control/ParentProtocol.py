

def unpack(msg: str):
    """
    handle receiving data from the clients
    :type msg: the message to unpack
    :return: returns a tuple that contain the opcode ...
    """
    command_number = msg[:2]
    rest = msg[2:].split("@")

    if int(command_number) == 3 and msg != "03":
        print(f"msg: {msg}")
        rest = "".join(rest)
        print(f"\n\nrest: {rest}")
        if '#' in "".join(rest):
            pairs_list = str(rest).split('#')
        else:
            pairs_list = [rest]
        pairs_dict = {}

        for pair in pairs_list:
            print(f"\npair: {pair}\n")
            mac, nickname = pair.split('$')
            pairs_dict[mac] = nickname
        rest = pairs_dict

    if int(command_number) == 21 and rest != ['']:
        if ',' in rest[0]:
            rest = rest[0].split(",")
        else:
            rest = rest[0]

    data = (int(command_number), rest)
    return data


def build_send_sign_up(username, password):
    """
    build the message of sign up with the username and the password by the protocol
    :param username: the parent input username
    :param password: the parent input password
    :return: the new massage to send by the protocol
    """
    return f"01{username}@{password}"


def build_send_login(username, password):
    """
    build the message of log in with the username and the password by the protocol
    :param username: the parent input username
    :param password: the parent input password
    :return: the new massage to send by the protocol
    """
    return f"02{username}@{password}"


def build_add_computer(mac_address, computer_name):
    """
    build the massage of sending new computer details to the server
    :param mac_address: the local address of the computer to add
    :param computer_name: the nickname of the computer (the parent choose)
    :return: the new massage to send by the protocol
    """
    return f"03{mac_address}@{computer_name}"


def build_add_kid(kid_username):
    """
    build the message of adding a new kid to computer
    :param kid_username: the username of the kid
    :return: the new massage to send by the protocol
    """
    return f"04{kid_username}"


def build_ask_all_parent_computers_data():
    """
    send to the server a query to get all the parent's computers data
    (mac address and computer nickname)
    :return: the new massage to send by the protocol
    """
    return f"05"


def build_ask_all_parent_kids_username():
    """
    build ask all parent kid's username
    :return: the new massage to send by the protocol
    """
    return f"24"


def build_send_parent_active_to_kid(username):
    """
    build the message to the server that the parent is one of his kids profile page.
    it means the parent want to get the relevant data for this screen.
    :param username: the kid's username
    :return: the new massage to send by the protocol
    """
    return f"06{username}"


def build_send_parent_not_active_to_kid():
    """
    build the message to update the server that the parent is not active in the kid's profile page
    :return: the new massage to send by the protocol
    """
    return f"07"


def build_ask_browsing_tracking(kid_id):
    """
    build the message that ask the browsing tracking (history) of a kid
    :param kid_id: the id of a kid
    :return: the new massage to send by the protocol
    """
    return f"08{kid_id}"


def build_ask_time_limit(kid_id):
    """
    build the message that ask the time limit of a kid
    :param kid_id: the id of a kid
    :return: the new massage to send by the protocol
    """
    return f"09{kid_id}"


def build_send_new_time_limit(kid_id, time_limit):
    """
    build the message that send new time limit of a kid to the server to update
    :param kid_id: the id of a kid
    :param time_limit: the new time limit
    :return: the new massage to send by the protocol
    """
    return f"10{kid_id}@{time_limit}"


def build_ask_forbidden_hours(kid_id):
    """
    build the message that agk for the forbidden hours list of a kid
    :param kid_id: the id of a kid
    :return: the new massage to send by the protocol
    """
    return f"11{kid_id}"


def build_add_set_of_forbidden_hours(kid_id, set_of_hours):
    """
    build the message to send a new forbidden set of hours to add to the forbidden hours list at the server
    :param kid_id: the id of a kid
    :param set_of_hours: a set of hours to add to the forbidden hours list
    :return: the new massage to send by the protocol
    """
    return f"12{kid_id}@{set_of_hours}"


def build_delete_set_of_forbidden_hours(kid_id, set_of_hours):
    """
    build the message to send a forbidden set of hours to delete from the forbidden hours list at the server
    :param kid_id: the id of a kid
    :param set_of_hours: a set of hours to delete from the forbidden hours list
    :return: the new massage to send by the protocol
    """
    return f"13{kid_id}@{set_of_hours}"


def build_ask_forbidden_addresses(kid_id):
    """
    build the message that agk for the forbidden addresses list of a kid
    :param kid_id: the id of a kid
    :return: the new massage to send by the protocol
    """
    return f"14{kid_id}"


def build_add_forbidden_address(kid_id, URL):
    """
     build the message to send a new address to add to the forbidden addresses list at the server
    :param kid_id: the id of a kid
    :param URL: the address
    :return: the new massage to send by the protocol
    """
    return f"15{kid_id}@{URL}"


def build_delete_forbidden_address(kid_id, URL):
    """
    build the message to send a new address to delete from the forbidden addresses list at the server
    :param kid_id: the id of a kid
    :param URL: the address
    :return: the new massage to send by the protocol
    """
    return f"16{kid_id}@{URL}"


def build_ask_forbidden_applications(kid_id):
    """
    build the message that agk for the forbidden applications list of a kid
    :param kid_id: the id of a kid
    :return: the new massage to send by the protocol
    """
    return f"17{kid_id}"


def build_add_forbidden_application(kid_id, application):
    """
    build the message to send a new application to add to the forbidden applications list at the server
    :param kid_id: the id of a kid
    :param application: the application
    :return: the new massage to send by the protocol
    """
    return f"18{kid_id}@{application}"


def build_delete_forbidden_application(kid_id, application):
    """
    build the message to send a new application to delete from the forbidden applications list at the server
    :param kid_id: the id of a kid
    :param application: the application
    :return: the new massage to send by the protocol
    """
    return f"19{kid_id}@{application}"


def build_computer_approval(kid_id, approval):
    """
    build the computer use approval of a kid message to send to the server
    :param kid_id: the id of a kid
    :param approval: the approval
    :return: the new massage to send by the protocol
    """
    return f"20{kid_id}@{approval}"


def build_internet_approval(kid_id, approval):
    """
     build the internet use approval of a kid message to send to the server
    :param kid_id: the id of a kid
    :param approval: the approval
    :return: the new massage to send by the protocol
    """
    return f"23{kid_id}@{approval}"





