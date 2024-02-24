
def unpack(msg : str):
    """
    handle receiving data from the clients
    :type msg: the message to unpack
    :return: returns a tuple that contain the opcode ...
    """
    command_number = msg[:2]
    rest = msg[2:].split("@")
    data = (int(command_number), rest)
    return data
    

# SERVER PROTOCOL - PARENTS SIDE:
def build_send_parent_login_approval(approval):
    """
    build the message to send to the parent if his login input is correct (username and password)
    :param approval: boolean answer
    :return: the new massage to send by the protocol
    """
    return f"01{approval}"


def build_send_parent_sign_up_approval(approval):
    """
    build the message to send to the parent if his sign up input is
    correct(username and password) and the system created a new parent
    :param approval: boolean answer
    :return: the new massage to send by the protocol
    """
    return f"02{approval}"


def build_send_computers_to_parent(computers_list):
    """
    build the message that send the information
    (mac address and computer name) to a parent
    :param computers_list: the list of all the information
    :return: the new massage to send by the protocol
    """
    computer_strings_list = []
    for mac, name in computers_list:
        computer_string = f"{mac}${name}"
        computer_strings_list.append(computer_string)

    result_string = "#".join(computer_strings_list)
    print(f"result string: {result_string}")
    return f"03{result_string}"


def build_send_kids_username_to_parent(usernames):
    """
    build the message to send all kid's username to a parent
    :param usernames: usernames
    :return: the new massage to send by the protocol
    """
    return f"21{usernames}"


def build_send_kid_tried_to_reach_prohibited_address(kid_id, address):
    """
    build the message to send when a kid tried to reach a prohibited address (the parent is active to the kid's profile page)
    :param kid_id: the id of a kid
    :param address: the prohibited address
    :return: the new massage to send by the protocol
    """
    return f"22{kid_id}@{address}"


def build_send_kid_to_parent(username, kid_id, remaining_time, active, computer_limit, internet_limit, reached_addresses):
    """
    build the message that send the information of a kid (for the profile page) to a parent
    :param reached_addresses: the prohibited addresses the kid tried to reach
    :param username: the username of the kid
    :param kid_id: the id of a kid
    :param remaining_time: the time that left for the kid to use a computer
    :param active: kid situation, using the computer or not
    :param computer_limit: boolean answer if there is a limitation of using the computer or not
    :param internet_limit: boolean answer if there is a limitation of using the internet or not
    :return: the new massage to send by the protocol
    """
    return f"04{username}@{kid_id}@{remaining_time}@{active}@{computer_limit}@{internet_limit}@{reached_addresses}"


def build_send_kid_activity(kid_id, activity):
    """
    build the message to send to the parent if a kid is active or not
    :param kid_id: the id of the kid
    :param activity: his activity, connected or not (boolean)
    :return: the new massage to send by the protocol
    """
    return f"18{kid_id}@{activity}"


def build_send_kid_computer_change_to_parent(kid_id, approval):
    """
    build the message of the the approval if the change of the computer limit has made successfully
    :param kid_id: the id of the kid
    :param approval: the approval if the change has done (boolean)
    :return: the new massage to send by the protocol
    """
    return f"14{kid_id}@{approval}"


def build_send_kid_internet_change_to_parent(kid_id, approval):
    """
    build the message of the the approval if the change of the internet limit has made successfully
    :param kid_id: the id of the kid
    :param approval: the approval if the change has done (boolean)
    :return: the new massage to send by the protocol
    """
    return f"17{kid_id}@{approval}"


def build_send_kid_remaining_time_to_parent(kid_id, remaining_time):
    """
    build the message to send to the parent the remaining time of a kid
    :param kid_id: the id of a kid
    :param remaining_time: the remaining time
    :return: the new massage to send by the protocol
    """
    return f"06{kid_id}@{remaining_time}"


def build_send_time_limit_to_parent(kid_id, time_limit, approval):
    """
    build the message to send to a parent an approval for the change the
    parent did to the kid's time limit
    :param approval:
    :param time_limit: the time limit
    :param kid_id: the id of the kid
    :return: the new massage to send by the protocol
    """
    return f"07{approval}@{kid_id}@{time_limit}"


def build_send_kid_browsing_tracking_to_parent(kid_id, history):
    """
    build the message to send to the parent the browsing history of a kid
    :param kid_id: the id of a kid
    :param history: the browsing history list of the kid
    :return: the new massage to send by the protocol
    """
    return f"05{kid_id}@{history}"


def build_send_prohibited_hours_to_parent(kid_id, prohibited_hours):
    """
    build the message to send to the parent that include the prohibited hours list of a kid
    :param kid_id: the id of a kid
    :param prohibited_hours: the prohibited hours list of a kid
    :return: the new massage to send by the protocol
    """
    return f"08{kid_id}@{prohibited_hours}"


def build_send_prohibited_hours_to_add_to_parent(kid_id, set, approval):
    """
    build the message to send to the parent that include an approval if the server added or not the set of prohibited
     hours the parent sent to add to the server
    :param approval:
    :param kid_id: the id of the kid
    :param set: set of prohibited hours
    :return: the new massage to send by the protocol
    """
    return f"09{approval}@{kid_id}@{set}"


def build_send_prohibited_hours_to_delete_to_parent(kid_id, set):
    """
    build the message to send to the parent that include an approval if the server deleted or not the set of prohibited
     hours the parent sent to delete from the server
    :param kid_id: the id of the kid
    :param set: set of prohibited hours
    :return: the new massage to send by the protocol
    """
    return f"09d@{kid_id}@{set}"


def build_send_prohibited_URLs_to_parent(kid_id, prohibited_addresses):
    """
    build the message to send to the parent that include the prohibited addresses list of a kid
    :param kid_id: the id of a kid
    :param prohibited_addresses: the list of prohibited addresses
    :return: the new massage to send by the protocol
    """
    return f"10{kid_id}@{prohibited_addresses}"


def build_send_prohibited_URL_to_add_to_parent(kid_id, address, approval):
    """
    build the message to send to the parent that include an approval if the server added or not the set of prohibited
     address the parent sent to add to the server
    :param approval:
    :param kid_id: the id of the kid
    :param address: prohibited address
    :return: the new massage to send by the protocol
    """
    return f"11{approval}@{kid_id}@{address}"


def build_send_prohibited_URL_to_delete_to_parent(kid_id, address):
    """
    build the message to send to the parent that include an approval if the server deleted or not the set of prohibited
     address the parent sent to delete from the server
    :param kid_id: the id of the kid
    :param address: prohibited address
    :return: the new massage to send by the protocol
    """
    return f"11d@{kid_id}@{address}"


def build_send_prohibited_applications_to_parent(kid_id, prohibited_applications):
    """
    build the message to send to the parent that include the prohibited applications list of a kid
    :param kid_id: the id of a kid
    :param prohibited_applications: the list of prohibited applications
    :return: the new massage to send by the protocol
    """
    return f"12{kid_id}@{prohibited_applications}"


def build_send_prohibited_application_to_add_to_parent(kid_id, app, approval):
    """
    build the message to send to the parent that include an approval if the server added or not the set of prohibited
     app the parent sent to add to the server
    :param approval:
    :param kid_id: the id of the kid
    :param app: prohibited app
    :return: the new massage to send by the protocol
    """
    return f"13{approval}@{kid_id}@{app}"


def build_send_prohibited_application_to_delete_to_parent(kid_id, app):
    """
    build the message to send to the parent that include an approval if the server deleted or not the set of prohibited
     app the parent sent to delete from the server
    :param kid_id: the id of the kid
    :param app: prohibited app
    :return: the new massage to send by the protocol
    """
    return f"13d@{kid_id}@{app}"


def build_send_add_computer_approval_to_parent(approval):
    """
    build send add computer approval to a parent
    :param approval: True or False
    :return: the new massage to send by the protocol
    """
    return f"19{approval}"


def build_send_add_kid_approval_to_parent(approval):
    """
    build send add a kid approval to the parent
    :param approval: True or False
    :return: the new massage to send by the protocol
    """
    return f"20{approval}"


# SERVER PROTOCOL - KID'S COMPUTERS SIDE:
def build_send_kid_data(kid_id, prohibited_URLs, prohibited_applications, internet_limit):
    """
    build the message to send to a computer of an active kid included the kid's basic data for communication (kid_id)
    and for setting limitations in the computer
    :param kid_id: the id of the kid
    :param prohibited_URLs: the list of the prohibited addresses the kid is not allowed to get to
    :param prohibited_applications: the list of the prohibited applications the kid is not allowed to get to
    :param internet_limit: a boolean flag sets if the computer has to block the internet usage from the kid or not
    :return: the new massage to send by the protocol
    """
    return f"02{kid_id}@{prohibited_URLs}@{prohibited_applications}@i{internet_limit}"


def build_turn_off_kid_computer():
    """
    set a message to turn of a kid's computer
    :return: the new massage to send by the protocol
    """
    return "01"


def build_allow_kid_internet():
    """
    set a message to send to kid's computer that the kid is allowed
    to use the internet
    :return: the new massage to send by the protocol
    """
    return "07"


def build_block_kid_internet():
    """
    set a message to send to kid's computer that the kid is not allowed
    to use the internet
    :return: the new massage to send by the protocol
    """
    return "08"


def build_send_prohibited_URL_to_add_to_kid_computer(address):
    """
    build a message that send an update to a kid's computer to add a
    prohibited address to the prohibited addresses list
    :param address: a new prohibited address
    :return: the new massage to send by the protocol
    """
    return f"09a{address}"


def build_send_prohibited_URL_to_delete_to_kid_computer(address):
    """
    build a message that send an update to a kid's computer to delete a
    prohibited address from the prohibited addresses list
    :param address: a prohibited address to delete
    :return: the new massage to send by the protocol
    """
    return f"09d{address}"


def build_send_prohibited_app_to_add_to_kid_computer(app):
    """
    build a message that send an update to a kid's computer to add a
    prohibited application to the prohibited applications list
    :param app: a new prohibited application
    :return: the new massage to send by the protocol
    """
    return f"10a{app}"


def build_send_prohibited_app_to_delete_to_kid_computer(app):
    """
    build a message that send an update to a kid's computer to delete a
    prohibited application from the prohibited applications list
    :param app: a prohibited application to delete
    :return: the new massage to send by the protocol
    """
    return f"10d{app}"






