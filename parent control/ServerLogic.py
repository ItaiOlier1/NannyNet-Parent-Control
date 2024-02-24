import queue
import threading
import time
from Timer import Timer
from ServerCom import ServerComm
from ServerProtocol import *
from ActiveKid import ActiveKid
from ParentControlDatabase import MyDatabase


def execute_command(ip, DB, command_num, data):
    """
    gets a command num and data and execute
    the command by the command number
    :param ip: the ip address of the client
    :param DB: the database object
    :param command_num: the command number
    :param data: the data
    :return: None
    """
    if comm.find_kind_by_ip(ip) == "k":
        if command_num == 1:
            is_kid_computer_exists(ip, DB, data)
        elif command_num == 2:
            username = data[0]
            handle_new_active_kid(ip, DB, username)
        elif command_num == 4:
            handle_new_address_from_kid(ip, DB, data)

    elif comm.find_kind_by_ip(ip) == "p":
        if command_num == 1:
            handle_parent_signup(ip, DB, data)
        elif command_num == 2:
            handle_parent_login(ip, DB, data)
        elif command_num == 3:
            add_computer(ip, DB, data)
        elif command_num == 4:
            username = data[0]
            add_kid(ip, DB, username)
        elif command_num == 5:
            send_computers_to_parent(ip, DB)
        elif command_num == 6:
            username = data[0]
            send_kid_to_parent(ip, DB, username)
        elif command_num == 7:
            # the parent sent he is not active to a kid, update it
            active_parents[ip][1] = None
        elif command_num == 8:
            kid_id = data[0]
            send_kid_browsing_tracking_to_parent(ip, DB, kid_id)
        elif command_num == 9:
            kid_id = data[0]
            send_time_limit_to_parent(ip, DB, kid_id, "a")
        elif command_num == 10:
            kid_id, new_time_limit = data
            update_time_limit(ip, DB, kid_id, new_time_limit)
        elif command_num == 11:
            kid_id = data[0]
            send_prohibited_hours_to_parent(ip, DB, kid_id)
        elif command_num == 12:
            kid_id, set = data
            add_set_of_prohibited_hour(ip, DB, kid_id, set)
        elif command_num == 13:
            kid_id, set = data
            delete_set_of_prohibited_hour(ip, DB, kid_id, set)
        elif command_num == 14:
            kid_id = data[0]
            send_prohibited_addresses_to_parent(ip, DB, kid_id)
        elif command_num == 15:
            kid_id, address = data
            add_prohibited_address(ip, DB, kid_id, address)
        elif command_num == 16:
            kid_id, address = data
            delete_prohibited_address(ip, DB, kid_id, address)
        elif command_num == 17:
            kid_id = data[0]
            send_prohibited_applications_to_parent(ip, DB, kid_id)
        elif command_num == 18:
            kid_id, app = data
            add_prohibited_application(ip, DB, kid_id, app)
        elif command_num == 19:
            kid_id, app = data
            delete_prohibited_application(ip, DB, kid_id, app)
        elif command_num == 20:
            kid_id, update = data
            update_computer_change(ip, DB, kid_id, update)
        elif command_num == 23:
            kid_id, update = data
            update_internet_change(ip, DB, kid_id, update)
        elif command_num == 24:
            send_all_kids_username_to_parent(ip, DB)



# UPDATES AND CHANGES IN BOTH SIDES

def get_active_kid_by_kid_id(kid_id):
    """
    get the kid ActiveKid object of the kid by his kid_id
    from the active kids list
    :param kid_id: the id of the kid
    :return: ActiveKid object or None
    """
    ret = None
    for active_kid in active_kids:
        current_id = active_kid.get_kid_id()
        if str(current_id) == str(kid_id):
            ret = active_kid
            break
    return ret


def update_time_limit(parent_ip, DB : MyDatabase, kid_id, new_time_limit):
    """
    update the time limit of a kid
    (the thread of the Timer check the database once in a while to update itself)
    :param parent_ip: the ip address of the parent
    :param DB: the database
    :param kid_id: the id of a kid
    :param new_time_limit: the new time limit to update
    :return: None
    """
    # update the time limit in the server
    bool_approval = DB.setTimeLimit(kid_id, new_time_limit)

    approval = bool_to_digits_approval(bool_approval)
    print(f"aproval: {approval}")

    # send the update approval to the parent
    send_time_limit_to_parent(parent_ip, DB, kid_id, approval)


def add_set_of_prohibited_hour(parent_ip, DB, kid_id, set):
    """
    add a set of prohibited hour and send an approval to the parent
    :param parent_ip: the ip of the parent
    :param DB: the database object
    :param kid_id: id of a kid
    :param set: a set of prohibited hours
    :return: None
    """
    # update the set in the server
    bool_approval = DB.addProhibitedSetOfHours(kid_id, set)
    # send the update approval to the parent
    approval = bool_to_digits_approval(bool_approval)
    send_prohibited_hours_to_add_to_parent(parent_ip, kid_id, set, approval)


def delete_set_of_prohibited_hour(parent_ip, DB, kid_id, set):
    """
    delete a set of prohibited hours and send an approval to the parent
    :param parent_ip: ip address of a parent
    :param DB: the database object
    :param kid_id: id of a kid
    :param set: a set of prohibited hours
    :return: None
    """
    # update the set in the server
    DB.deleteProhibitedSetOfHours(kid_id, set)
    # send the update approval to the parent
    send_prohibited_hours_to_delete_to_parent(parent_ip, kid_id, set)


def send_prohibited_hours_to_add_to_parent(parent_ip, kid_id, set, approval):
    """
    send prohibited hours approval to the parent
    :param parent_ip: ip address of a parent
    :param kid_id: id of a kid
    :param set: a set of prohibited hours
    :param approval: the approval to add or not
    :return: None
    """
    msg = build_send_prohibited_hours_to_add_to_parent(kid_id, set, approval)
    comm.send(msg, parent_ip)


def send_prohibited_hours_to_delete_to_parent(parent_ip, kid_id, set):
    """
    send an approval to the parent to delete a prohibited hour
    :param parent_ip: ip address of a parent
    :param kid_id: id of a kid
    :param set: a set of prohibited hours
    :return: None
    """
    msg = build_send_prohibited_hours_to_delete_to_parent(kid_id, set)
    comm.send(msg, parent_ip)


def add_prohibited_address(parent_ip, DB, kid_id, address):
    """
    add a prohibited address and send an approval to the parent and to the kid's computer if he is active
    :param parent_ip: the ip address of the parent
    :param DB: the database object
    :param kid_id: kid id
    :param address: the address to add
    :return: None
    """
    # update the set in the server
    bool_approval = DB.addProhibitedURL(kid_id, address)
    # send the update approval to the parent
    approval = bool_to_digits_approval(bool_approval)
    send_prohibited_address_to_add_to_parent(parent_ip, kid_id, address, approval)
    # send the update to kid
    send_prohibited_address_change_to_kid(kid_id, address, "a")


def delete_prohibited_address(parent_ip, DB, kid_id, address):
    """
    delete a prohibited address from the prohibited addresses list in the dataa base and send an
    approval to the parent and to the kid's computer if he is active
    :param parent_ip: ip address of the parent
    :param DB: the database
    :param kid_id: the id of the kid
    :param address: the address to delete
    :return: None
    """
    # update the set in the server
    DB.deleteProhibitedURL(kid_id, address)
    # send the update approval to the parent
    send_prohibited_address_to_delete_to_parent(parent_ip, kid_id, address)
    # send the update to kid
    send_prohibited_address_change_to_kid(kid_id, address, "d")


def send_prohibited_address_to_add_to_parent(parent_ip, kid_id, address, approval):
    """
    send an approval of the address to add to the parent
    :param parent_ip: ip address of the parent
    :param kid_id:  id of the kid
    :param address: the address the parent sent add
    :param approval: the approval
    :return: None
    """
    msg = build_send_prohibited_URL_to_add_to_parent(kid_id, address, approval)
    comm.send(msg, parent_ip)


def send_prohibited_address_to_delete_to_parent(parent_ip, kid_id, address):
    """
    send prohibited address to delete to the parent
    :param parent_ip: parent ip
    :param kid_id: kid id
    :param address: address
    :return: None
    """
    msg = build_send_prohibited_URL_to_delete_to_parent(kid_id, address)  # create the message
    comm.send(msg, parent_ip)  # send the message


def send_prohibited_address_change_to_kid(kid_id, address, command):
    """
    send a prohibited address to add or to delete to a kid to the
    prohibited addresses list
    :param kid_id: the kid's id
    :param address: the address to add or to delete
    :param command: a- add, d - delete
    :return: None
    """
    kid = get_active_kid_by_kid_id(kid_id)  # get the active kid object, or None
    # if the kid is active:
    if kid is not None:
        print("\nthe kid is active")
        # the kid is active, send the address to him:
        mac_address = kid.get_mac_address()  # get the mac address of the kid's computer
        ip = active_computers[mac_address]  # get the ip address of the kid's computer
        # send the message buy the command type
        if command == "a":
            send_prohibited_address_to_add_to_kid(ip, address)
        elif command == "d":
            send_prohibited_address_to_delete_to_kid(ip, address)


def send_prohibited_address_to_add_to_kid(ip, address):
    """
    send a prohibited address to add to the prohibited
    addresses list in the kid's computer client
    :param ip: the ip address of the kid's computer
    :param address: the address to add
    :return:
    """
    msg = build_send_prohibited_URL_to_add_to_kid_computer(address)  # create the message
    comm.send(msg, ip)  # send the message


def send_prohibited_address_to_delete_to_kid(ip, address):
    """
    send the prohibited address of a kid to delete from the prohibited addresses list in
    the kid's computer client
    :param ip: the ip address
    :param address: the address to delete
    :return: None
    """
    msg = build_send_prohibited_URL_to_delete_to_kid_computer(address)  # create the message
    comm.send(msg, ip)  # send the message


def add_prohibited_application(parent_ip, DB, kid_id, app):
    """
    add prohibited application of a kid to the data base and update
    the parent and the kid's computers
    :param parent_ip: the ip of the parent
    :param DB: the data base object
    :param kid_id: the id of the kid
    :param app: the application to add to the database
    :return: None
    """
    # update the set in the server
    bool_approval = DB.addProhibitedApplication(kid_id, app)
    # send the update approval to the parent
    approval = bool_to_digits_approval(bool_approval)
    send_prohibited_application_to_add_to_parent(parent_ip, kid_id, app, approval)
    # send the update to kid
    send_prohibited_application_change_to_kid(kid_id, app, "a")


def delete_prohibited_application(parent_ip, DB, kid_id, app):
    """
    delete a prohibited application of a kid from the data base and send the update to the parent and
    to the kid's computer
    :param parent_ip: the ip address of the parent
    :param DB: the database object
    :param kid_id: the id of the kid
    :param app: the application to delete
    :return: None
    """
    # update the set in the server
    DB.deleteProhibitedApplication(kid_id, app)
    # send the update approval to the parent
    send_prohibited_application_to_delete_to_parent(parent_ip, kid_id, app)
    # send the update to kid
    send_prohibited_application_change_to_kid(kid_id, app, "d")


def send_prohibited_application_to_add_to_parent(parent_ip, kid_id, app, approval):
    """
    send a prohibited application's approval of a kid to the parent
    :param parent_ip: the ip address of a parent
    :param kid_id: the id of the kid
    :param app: the application
    :param approval: the approval
    :return: None
    """
    msg = build_send_prohibited_application_to_add_to_parent(kid_id, app, approval)  # create the message
    comm.send(msg, parent_ip)  # send the message to the parent


def send_prohibited_application_to_delete_to_parent(parent_ip, kid_id, app):
    """
    send a prohibited application to delete of a kid to the parent
    :param parent_ip:  the ip address of a parent
    :param kid_id: the id of a kid
    :param app: the application to delete
    :return: None
    """
    msg = build_send_prohibited_application_to_delete_to_parent(kid_id, app)  # create the message
    comm.send(msg, parent_ip)  # send the message


def send_prohibited_application_change_to_kid(kid_id, application, command):
    """
    send a prohibited application to add or to delete to a kid from his
    prohibited applications list.
    :param kid_id: the id of a kid
    :param application: the application to add or to delete
    :param command: the command - a- add, d - delete
    :return: None
    """
    kid = get_active_kid_by_kid_id(kid_id)
    if kid is not None:
        # the kid is active, send the address to him:
        mac_address = kid.get_mac_address()
        ip = active_computers[mac_address]
        # send the message buy the command type
        if command == "a":
            send_prohibited_application_to_add_to_kid(ip, application)  # send add message
        elif command == "d":
            send_prohibited_application_to_delete_to_kid(ip, application)  # send delete message


def send_prohibited_application_to_add_to_kid(ip, address):
    """
    send a prohibited application the server added to a kid's computer to update
    :param ip: the ip of the kid's computer
    :param address: the address to add
    :return: None
    """
    msg = build_send_prohibited_app_to_add_to_kid_computer(address)  # build the message
    comm.send(msg, ip)  # sending the message


def send_prohibited_application_to_delete_to_kid(ip, address):
    """
     send a prohibited application the server delete to a kid's computer to update
    :param ip: the ip address of the kid's computer
    :param address: the address to delete
    :return: None
    """
    msg = build_send_prohibited_app_to_delete_to_kid_computer(address)
    comm.send(msg, ip)


def bool_to_digits_approval(bool_approval):
    """
    convert from a boolean approval to digits approval
    :param bool_approval:
    :return: the new digits approval
    """
    approval = 'f'
    # if the boolean approval is true , the digits approval will be 'a'
    if bool_approval:
        approval = 'a'
    return approval


def update_computer_change(parent_ip, DB, kid_id, update):
    """
    the server got a change to do to a computer limit to one of the kids, update the change in the database
    and, send an approval to the parent, and send the update to the kid's computer client
    if the kid is using the computer
    :param parent_ip: the ip address of the parent
    :param DB: the database
    :param kid_id: the id of the kid
    :param update: the update to change in the database
    :return: None
    """
    if update == 'a' or update == 'b':
        if update == 'a':
            DB.setComputerLimit(kid_id, False)
        elif update == 'b':
            DB.setComputerLimit(kid_id, True)
        # build the message to send the approval to the parent
        msg = build_send_kid_computer_change_to_parent(kid_id, 'a')

        # send to the kid's computer the update if the kid is active:
        if update == 'b':
            kid = get_active_kid_by_kid_id(kid_id)
            if kid is not None:
                # the kid is active, send the address to him:
                mac_address = kid.get_mac_address()
                ip = active_computers[mac_address]
                msg = build_turn_off_kid_computer()

                # delete kid's computer from active computers dict
                mac = get_key_by_value(active_computers, ip)
                if mac is not None:
                    del active_computers[mac]

                # delete the kid from the active kids object
                active_kids.remove(kid)
                comm.send(msg, ip)

    else:
        # build the message to send the approval (negative) to the parent
        msg = build_send_kid_computer_change_to_parent(kid_id, 'f')
    # send an approval to the parent:
    comm.send(msg, parent_ip)


def update_internet_change(parent_ip, DB, kid_id, update):
    """
    the server got a change to do to a internet limit to one of the kids, update the change in the database
    and, send an approval to the parent, and send the update to the kid's computer client
    if the kid is using the computer
    :param parent_ip: the ip address of the parent
    :param DB: the database
    :param kid_id: the id of the kid
    :param update: the update to change in the database
    :return: None
    """
    if update == 'a' or update == 'b':
        if update == 'a':
            DB.setInternetLimit(kid_id, False)  # set the internet limit as False
            msg_to_kid = build_allow_kid_internet()
        else:
            DB.setInternetLimit(kid_id, True)  # set the internet limit as True
            msg_to_kid = build_block_kid_internet()

        # build the message to send the approval to the parent
        msg = build_send_kid_internet_change_to_parent(kid_id, 'a')

        # send to the kid's computer the update if the kid is active:
        kid = get_active_kid_by_kid_id(kid_id)
        if kid is not None:
            # the kid is active, send the address to him:
            mac_address = kid.get_mac_address()
            ip = active_computers[mac_address]
            comm.send(msg_to_kid, ip)

    else:
        # build the message to send the approval (negative) to the parent
        msg = build_send_kid_internet_change_to_parent(kid_id, 'f')
    # send an approval to the parent:
    comm.send(msg, parent_ip)


# HANDLE KID SIDE
def is_kid_computer_exists(ip, DB: MyDatabase, mac_address):
    """
    check if the mac address is in the data base in the computers table,
    if it is not: disconnect the current client from the system.
    :param DB: the database object
    :param ip: the ip of the client
    :param mac_address: the mac address of the
    computer to check if it's one of my clients
    :return: None
    """
    # check if the mac address exists in the database
    # (by getting the parent id and not None in case it's exists)
    mac_address = ''.join(mac_address)
    print(f"MAC ADDRESS - {mac_address}")
    parent_id = DB.getParentIDByMac(mac_address)
    # if the parent id is not exist for this mac address, disconnect the client from the server
    if not parent_id:
        disconnect_kid_computer(ip)
    else:
        # add the computer to the active computers list
        active_computers[mac_address] = ip


def disconnect_kid_computer(ip):
    """
    disconnect a computer of a kid by the ip address
    :param ip: the address of the computer to disconnect
    :return: None
    """
    # delete the current computer from the active_computers dict
    mac = get_key_by_value(active_computers, ip)
    if mac is not None:
        del active_computers[mac]
    comm.disconnect_client_by_ip(ip)


def get_key_by_value(dictionary, value):
    """
    get a key by some value to check if it is in the dict
    :param dictionary: the dict to cover
    :param value: the value to check if it is in the dict as a value
    :return: the key or None
    """
    ret = None
    for k, v in dictionary.items():
        if v == value:
            ret = k
    return ret


def handle_new_active_kid(ip, DB: MyDatabase, username):
    """
    1. check the limitations of the current kid
    (if the kid is not in the database it means he has no limitations)
    2. add this kid to the list of "active_kids" (by his kid_id, mac_address and isParent_active)
    3.send the kid's data - send the data of the limitations with the kid_id
    or in case the kid is not allowed to use the computer send to his client a message
    to turn off the computer.
    :param ip: the ip address of the client
    :param DB: the database object
    :param username: the username of the client
    :return: None
    """
    # get the mac address of the computer of the client by his ip
    mac_address = get_key_by_value(active_computers, ip)
    parent_id = DB.getParentIDByMac(mac_address)

    # get the kid's limitations from the data base
    kid_limitations = DB.getKidCurrentLimitationsForKidComputer(username, parent_id)
    print(kid_limitations)
    if kid_limitations is not None:
        # if the data is not None, the kid is in the system and has limitations
        kid_id, prohibited_URLs, prohibited_applications, \
        computer_limit, internet_limit = kid_limitations
        new_active_kid_obj = ActiveKid(kid_id, mac_address)  # create a new ActiveKid object of the current kid
        active_kids.append(new_active_kid_obj)  # add the object of the kid to the active kids list

        # return to the client of the active kid the limitations
        # check if the kid needs to turn of the computer:
        if computer_limit == 1:
            # send the client to turn of the computer
            msg = build_turn_off_kid_computer()
        else:
            # the kid can use the computer, send to his client the limitations of the kid
            msg = build_send_kid_data(kid_id, prohibited_URLs, prohibited_applications,
                                      internet_limit)
            # send the parent the kid is active (only if the parent is active to this kid profile)
            send_kid_activity_to_parent(kid_id, "1")

            # start a new thread timer fot the new kid:
            new_timer = Timer(DB, kid_id, timer_q)
            timers[ip] = new_timer

        time.sleep(1)
        comm.send(msg, ip)


def send_kid_activity_to_parent(kid_id, activity):
    """
    send to a parent the activity condition of a kid by his kid_id
    :param kid_id: the id of a kid
    :param activity: the activity condition of the kid
    :return: None
    """
    # send the message only if the parent is active to the kid profile page:
    parent_ip = check_parent_active_to_kid(kid_id)
    if parent_ip is not None:
        print(f"the parent ip is: {parent_ip}")
        # send the message to the parent, he is active to the kid
        msg = build_send_kid_activity(kid_id, activity)
        comm.send(msg, parent_ip)


def check_parent_active_to_kid(kid_id):
    """
    check if a parent is active to a kid using active_parents dict
    if the parent is active to the kid, return the ip address of the parent
    :param kid_id: the id of the kid
    :return: the ip address of the parent or None
    """
    print(f"active_parents - {active_parents}")
    ret = None
    for ip, (parent_id, current_kid_id) in active_parents.items():
        if current_kid_id == kid_id:  # if the kid is active
            ret = ip
    return ret


def handle_new_address_from_kid(ip, DB: MyDatabase, data):
    """
    we got a new address the kid tried to reach,
    add this address to the browsing history list in the data base
    :param DB: the database
    :param data: the id of the kid and the address to add
    :return:
    """
    kid_id, address = data
    print("the address to add is: " + str(address))
    # add the address to the browsing history list:
    DB.updateHistory(kid_id, address)

    # if the address is prohibited, send an update to the parent
    flag = DB.isAddressIsProhibited(kid_id, address)
    if flag:
        print("THE ADDRESS OF THE CLIENT IS PROHIBITED")
        # send to the parent that the user tried to reach a prohibited address:
        parent_ip = check_parent_active_to_kid(kid_id)
        if parent_ip is not None:
            msg = build_send_kid_tried_to_reach_prohibited_address(kid_id, address)
            comm.send(msg, parent_ip)
        else:
            # the parent is not active, add the prohibited address the user searched to the data base
            DB.addReachedAddress(kid_id, address)
            print(f"Reached Addresses: {DB.getReachedAddresses(kid_id)}")

        # send the user to block the internet:
        # set the internet limit
        DB.setInternetLimit(kid_id, 1)
        msg = build_block_kid_internet()
        comm.send(msg, ip)


# HANDLE PARENT SIDE
def handle_parent_signup(ip, DB: MyDatabase, data):
    """
    the user tried to sign up, add him to the system if
    the data is proper and send him an approval
    :param ip: the ip address of the user
    :param DB: the database object
    :param data: the data with the username and the password
    :return: None
    """
    username, password = data
    approval = DB.checkSignUp(username, password)
    # send the approval to the parent
    msg = build_send_parent_sign_up_approval(approval)
    comm.send(msg, ip)
    if approval is True:
        # add the parent to the active parents dict
        active_parents[ip] = [DB.getParentIDByUsernameAndPassword(username, password), None]
        print(f"active parents: {active_parents}")


def handle_parent_login(ip, DB: MyDatabase, data):
    """
    the user tried to log in send him an approval if the data his client sent is correct
    :param ip: the ip address of the user
    :param DB: the database object
    :param data: the data with the username and the password
    :return: None
    """
    username, password = data
    approval = DB.checkLogIn(username, password)
    # send the approval to the parent
    msg = build_send_parent_login_approval(approval)
    comm.send(msg, ip)
    if approval is True:
        # add the parent to the active parents dict
        active_parents[ip] = [DB.getParentIDByUsernameAndPassword(username, password), None]
        print(f"active parents: {active_parents}")


def add_computer(ip, DB: MyDatabase, data):
    """
    add a computer to the system
    :param ip: the ip address of the user
    :param DB: the database object
    :param data: the data with the username and the password
    :return: None
    """
    mac_address, computer_name = data
    print(f"mac: {mac_address} , name: {computer_name}")
    print(f"parent ip address: {ip}")
    parentID = active_parents[str(ip)][0]
    print(f"parent id {parentID}")
    approval = DB.addComputer(mac_address, computer_name, parentID)

    # send the approval to the parent:
    msg = build_send_add_computer_approval_to_parent(approval)
    comm.send(msg, ip)


def add_kid(ip, DB: MyDatabase, username):
    """
    add a new kid to the system
    :param ip: the ip address of the user
    :param DB: the database object
    :param username: the username
    :return: None
    """
    # get the parent id of the parent:
    parentID = active_parents[ip][0]
    approval = DB.addKid(parentID, username)

    # send an approval the kid was added
    msg = build_send_add_kid_approval_to_parent(approval)
    comm.send(msg, ip)


def send_computers_to_parent(ip, DB: MyDatabase):
    """
    send the all the mac addresses and the
    computers names of the computers of a parent to a parent
    :param ip: the ip address of a parent
    :param DB: the database
    :return: None
    """
    parentID = active_parents[ip][0]  # get the parent id by the ip address
    computers_string = DB.getAllParentComputers(parentID)  # get the computers string of info from the database
    print(computers_string)
    msg = build_send_computers_to_parent(computers_string)  # build the message to send
    comm.send(msg, ip)  # send the message


def send_all_kids_username_to_parent(ip, DB: MyDatabase):
    """
    send the all the username of the kid's of a parent to a parent
    :param ip: the ip address of a parent
    :param DB: the database
    :return: None
    """
    parentID = active_parents[ip][0]  # get the parent id by the ip
    usernames = DB.getAllParentKidsUsername(parentID)  # get the usernames of the parent's kids from the database
    msg = build_send_kids_username_to_parent(usernames)  # build the message
    comm.send(msg, ip)  # send the message


def send_kid_to_parent(ip, DB: MyDatabase, username):
    """
    send to a parent a kid's data (username, kid_id, remaining_time,
    active, computer_limit, internet_limit, camera_limit, microphone_limit). it happens
    when the parent is active to a kid's profile page so update at the active_parents dict
     if the kid is active by his kidID
    :param ip: the ip address of a parent
    :param DB: the database
    :param username: the kid's username
    :return: None
    """
    parentID = active_parents[ip][0]  # get the parent id by the ip address
    kid_data = DB.getKidDataForActiveParentToKid(parentID, username)
    if kid_data is not None:
        kid_id, remaining_time, computer_limit, internet_limit, reached_addresses = kid_data
        # check if the kid is active:
        active = is_kid_active(kid_id)
        # send the message include the kid's data to the parent
        msg = build_send_kid_to_parent(username, kid_id, remaining_time, active, computer_limit, internet_limit, reached_addresses)
        comm.send(msg, ip)
        active_parents[ip][1] = kid_id  # update that the parent is active to the current kid

        # delete the reached addresses from the data base
        DB.deleteAllReachedAddress(kid_id)
    else:
        # disconnect the parent from the system
        disconnect_parent(ip)


def disconnect_parent(ip):
    """
    disconnect a computer of a parent by the ip address
    :param ip: the address of the computer to disconnect
    :return: None
    """
    del active_parents[ip]  # delete the parent from the active parents list
    comm.disconnect_client_by_ip(ip)  # disconnect the client


def is_kid_active(kidID):
    """
    check if a kid is active or not
    :param kidID: the id of a kid
    :return: boolean (True or False)
    """
    flag = False
    # check if a kid is active (in active kids list)
    for active_kid in active_kids:
        current_id = active_kid.get_kid_id()
        if current_id == kidID:
            flag = True
            break
    return flag


def send_kid_browsing_tracking_to_parent(ip, DB: MyDatabase, kid_id):
    """
    get the browsing tracking list (history) from the database and send it to the parent
    :param ip: the ip address of a parent
    :param DB: the database
    :param kid_id: the id of the kid
    :return: None
    """
    history = DB.getHistory(kid_id)  # get the history string
    print(history)
    msg = build_send_kid_browsing_tracking_to_parent(kid_id, history)  # build the message
    comm.send(msg, ip)  # send the message


def send_time_limit_to_parent(ip, DB: MyDatabase, kid_id, approval):
    """
    get the time limit from the database and send it to the parent
    :param approval: the approval ('a' / 'f')
    :param ip: the ip address of a parent
    :param DB: the database
    :param kid_id: the id of the kid
    :return: None
    """
    time_limit = DB.getTimeLimit(kid_id)  # get the time limit of a kid from the database
    print(time_limit)
    msg = build_send_time_limit_to_parent(kid_id, time_limit, approval)  # build the message
    comm.send(msg, ip)  # send the message


def send_prohibited_hours_to_parent(ip, DB: MyDatabase, kid_id):
    """
    get the prohibited hours list from the database and send it to the parent
    :param ip: the ip address of a parent
    :param DB: the database
    :param kid_id: the id of the kid
    :return: None
    """
    prohibited_hours = DB.getProhibitedHours(kid_id)  # get the prohibited hours of a kid from the database
    print(prohibited_hours)
    msg = build_send_prohibited_hours_to_parent(kid_id, prohibited_hours)  # create the message
    comm.send(msg, ip)  # send the message


def send_prohibited_addresses_to_parent(ip, DB: MyDatabase, kid_id):
    """
    get the prohibited addresses list from the database and send it to the parent
    :param ip: the ip address of a parent
    :param DB: the database
    :param kid_id: the id of the kid
    :return: None
    """
    prohibited_addresses = DB.getProhibitedURLs(kid_id)  # get  the prohibited addresses of a kid
    print(prohibited_addresses)
    msg = build_send_prohibited_URLs_to_parent(kid_id, prohibited_addresses)  # create the message to send
    comm.send(msg, ip)  # send the message


def send_prohibited_applications_to_parent(ip, DB: MyDatabase, kid_id):
    """
    get the prohibited applications list from the database and send it to the parent
    :param ip: the ip address of a parent
    :param DB: the database
    :param kid_id: the id of the kid
    :return: None
    """
    prohibited_applications = DB.getProhibitedApplications(kid_id)  # get the prohibited applications of a kid
    print(prohibited_applications)
    msg = build_send_prohibited_applications_to_parent(kid_id, prohibited_applications)  # create a message
    comm.send(msg, ip)  # send the message


def handle_message(q, comm):
    """
    handle messages from the server
    :param q: the messages queue from the server
    :param comm: the communication object
    :return: None
    """
    DB = MyDatabase("myDataBase")  # create the database object
    threading.Thread(target=handle_timer_messages, args=(timer_q, comm,)).start()  # start the handle timers msg thread
    while True:
        data, ip = q.get()  # get the data and the ip address of a client
        print(f"data from, {ip}, {data}")

        # if the data is "close timer", the user has disconnected so close the timer and delete his timer from the timers list
        if data == "close timer":
            if ip in timers.keys():
                # get the Timer object for the IP address
                timer = timers[ip]

                # stop the thread
                timer.kill()
                del timers[ip]  # remove the IP address and thread mapping from the dictionary

            print(f"Timers: {timers}")
        else:
            # comm.send(data, ip)
            data_tuple = unpack(data)  # unpack the data using the protocol
            print(f"the tuple of the client's data is: {data_tuple}")
            execute_command(ip, DB, data_tuple[0], data_tuple[1])  # execute the methods by the command number


def handle_timer_messages(q, comm):
    """
    handle timer messages from the communication object
    :param q: the queue with the messages
    :param comm: the communication object
    :return: None
    """
    while True:
        kid_id, remaining_time = q.get()  # get the kid id and the remaining time of a kid
        print(f"timer data: id: {kid_id}, remaining time: {remaining_time}")

        # get the ip of the parent by his id:
        parent_ip = check_parent_active_to_kid(kid_id)
        # if the parent is active, send the update to the parent
        if parent_ip is not None:
            msg = build_send_kid_remaining_time_to_parent(kid_id, remaining_time)
            comm.send(msg, parent_ip)

        # if the remaining time is 0, send to the kid's computer to shout down
        if remaining_time == "00:00:00":
            active_kid = get_active_kid_by_kid_id(kid_id)  # get the active kid object
            # if the kid is active, send him the message
            if active_kid is not None:
                mac = active_kid.get_mac_address()  # ge tthe kid's computer's mac address
                ip = active_computers[mac]  # get the ip of the kid's computer
                msg = build_turn_off_kid_computer()  # create the message
                comm.send(msg, ip)  # send the message


if __name__ == '__main__':
    # create the queue to handle messages
    q = queue.Queue()

    timer_q = queue.Queue()

    # create the comm object:
    comm = ServerComm(1500, q)

    active_computers = {}  # {mac address : ip}
    active_kids = []  # [ActiveKid]
    active_parents = {}  # {ip : parent_id, active_to_kids}

    timers = {}  # {ip : Timer}

    threading.Thread(target=handle_message, args=(q, comm,)).start()  # start the handle messages thread
