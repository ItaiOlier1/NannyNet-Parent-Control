
def unpack(msg: str):
    """
    handle receiving data from the clients
    :type msg: the message to unpack
    :return: returns a tuple that contain the opcode ...
    """
    command_number = msg[:2]
    rest = msg[2:].split("@")

    if command_number == "02":
        rest[-1] = unpack_limitations_data(rest[-1])

    data = (int(command_number), rest)
    return data


def unpack_limitations_data(limitations_string):
    """
    unpack the limitations data from string to numbers
    :param limitations_string: the limitations string
    :return: unpacked limitations
    """
    limitations_numbers = ""
    for char in limitations_string:
        if char.isdigit():
            limitations_numbers += char
    return [x == '1' for x in limitations_numbers]


def build_send_mac_address(mac_address):
    """
    build the message that send the mac address of the current computer to the server
    :param mac_address: the physical address of the computer
    :return: the new massage to send by the protocol
    """
    return f"01{mac_address}"


def build_send_kid_active(username):
    """
    build the message that sent to the server when a new kid is active (using the computer)
    :param username: the kid username account
    :return: the new massage to send by the protocol
    """
    return f"02{username}"


def build_send_kid_not_active(username):
    """
    build the message that sent to the server when the kid isn't active anymore (if the kid stopped using the computer)
    :param username: the kid username account
    :return: the new massage to send by the protocol
    """
    return f"03{username}"


def build_send_address(kid_id, address):
    """
    build the message that update the server every time a kid browsed an address while he is browsing
    :param kid_id: the id of a kid
    :param address: the address the kid browsed to (or tried to)
    :return: the new massage to send by the protocol
    """
    return f"04{kid_id}@{address}"








