import queue
from Kid import Kid
from ClientCom import ClientComm
from ParentProtocol import *
import threading
from gui import MyFrame
import wx
import setting
from pubsub import pub


# runs as a thread
def handle_message(comm, q):
    """
    handle messages from the server
    :param q: the messages queue from the server
    :return: None
    """
    while True:
        data = q.get()  # get the data
        print("data from server: ", data)
        data_tuple = unpack(data)  # unpack the data
        print(data_tuple)
        execute_command(data_tuple[0], data_tuple[1])  # execute command by command number


def execute_command(command_num, data):
    """
    execute command by a command number
    :param command_num: command number
    :param data: the data
    :return: None
    """
    # handle login approval
    if command_num == 1:
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage,"login_status", status = data)
    # handle registration status
    elif command_num == 2:
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage,"reg_status", status = data)
    # handle parent computer's data (nickname and mac address)
    elif command_num == 3:
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage,"parent_computers_status", status = data)
    # handle kid data to profile page
    elif command_num == 4:
        get_kid_data(data)
    # handle kid's history list
    elif command_num == 5:
        kid_id, history = data
        print(f"History: {history}")
        if "," in history:
            history = history.split(",")
        else:
            history = [history]
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "handle_history_status", status=history)
    # handle kid's remaining time data
    elif command_num == 6:
        kid_id, remaining_time = data
        print(f"kid_id: {kid_id} , remaining_time: {remaining_time}")
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage,"update_remaining_time_status", status = remaining_time)
    # handle kid time limit approval
    elif command_num == 7:
        approval, kid_id, time_limit = data
        update_time_limit(approval, kid_id, time_limit)
    # handle forbidden hours of kid to show
    elif command_num == 8:
        kid_id, forbidden_hours = data
        update_forbidden_hours(kid_id, forbidden_hours)
    # handle a set of hours approval
    elif command_num == 9:
        approval, kid_id, set = data
        if approval == "a":
            # add
            add_set_of_forbidden_hours(kid_id, set)
        elif approval == "d":
            # delete
            delete_set_of_forbidden_hours(kid_id, set)
    # handle forbidden addresses list to show
    elif command_num == 10:
        kid_id, forbidden_addresses = data
        update_forbidden_addresses(kid_id, forbidden_addresses)
    # handle a forbidden address approval
    elif command_num == 11:
        approval, kid_id, address = data
        if approval == "a":
            # add
            add_forbidden_address(kid_id, address)
        elif approval == "d":
            # delete
            delete_forbidden_address(kid_id, address)
    # handle kid's forbidden applications to show
    elif command_num == 12:
        kid_id, forbidden_applications = data
        update_forbidden_applications(kid_id, forbidden_applications)
    # handle kid's forbidden app approval
    elif command_num == 13:
        approval, kid_id, app = data
        if approval == "a":
            # add
            add_forbidden_application(kid_id, app)
        elif approval == "d":
            # delete
            delete_forbidden_application(kid_id, app)
    # handle kid's turn off approval
    elif command_num == 14:
        kid_id, approval = data
        print("TURNED OFF")
    # handle kid internet approval
    elif command_num == 17:
        kid_id, approval = data
        print("CHANGED INTERNET LIMITATION")
    # handle add new computer approval
    elif command_num == 19:
        print(f"the APPROVAL to add a new computer is: {data[0]}")
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "add_computer_status", status=data)
    # handle add new kid approval
    elif command_num == 20:
        print(f"the APPROVAL to add a new kid is: {data[0]}")
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "add_kid_status", status=data)
    # handle get all kids username
    elif command_num == 21:
        username_list = data
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "parent_kids_username_status", status=username_list)
        print(f" USERNAMES {username_list}")

        for kid in kids:
            print(f"Kids LIST --- {kid}")
    # handle a reached address of a kid
    elif command_num == 22:
        kid_id, address = data
        print(f"a kid tried to reach a prohibited address: {address}")


def update_time_limit(approval, kid_id, time_limit):
    """
    update the time limit only if the approval is allowed
    :param approval: allow - a
    :param kid_id: kid id
    :param time_limit: the time limit
    :return: None
    """
    # if the approval is allowed
    if approval == "a":
        kid = get_kid_by_kid_id(kid_id)  # get kid object
        # if the kid object exists
        if kid is not None:
            kid.set_time_limit(time_limit)
            print("KID OBJECT: " + str(vars(kid)))
            # handle showing the data in gui
            wx.CallAfter(pub.sendMessage, "handle_time_limit_status", status=time_limit)


def update_forbidden_hours(kid_id, forbidden_hours):
    """
    update forbidden hours of a kid
    :param kid_id: the id of the kid
    :param forbidden_hours: the list of forbidden hours
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.set_forbidden_hours(forbidden_hours)
        print("KID OBJECT listttttttt: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "handle_sets_of_hours_status", status=forbidden_hours)


def add_set_of_forbidden_hours(kid_id, set):
    """
    add a new set of forbidden hours
    :param kid_id: kid id
    :param set: a set of forbidden hours
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.add_set_of_forbidden_hours(set)
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "handle_add_set_of_hours_status", status=set)


def delete_set_of_forbidden_hours(kid_id, set):
    """
    delete a set of forbidden hours and show the change
    :param kid_id: the id of a kid
    :param set: a set of hours
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.delete_set_of_forbidden_hours(set)
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "handle_delete_set_of_hours_status", status=set)


def update_forbidden_addresses(kid_id, forbidden_addresses):
    """
    update a forbidden addresses ans show changes
    :param kid_id: the kid id
    :param forbidden_addresses: the addresses to update and show
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.set_forbidden_addresses(forbidden_addresses)
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "handle_prohibited_addresses_dialog_status", status=forbidden_addresses)


def add_forbidden_address(kid_id, address):
    """
    add a forbidden address and show changes
    :param kid_id: the kid's id
    :param address: the address to add
    :return:
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.add_forbidden_address(address)
        print(f"address - {address}")
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "on_add_button", status=address)


def delete_forbidden_address(kid_id, address):
    """
    delete a forbidden address and show changes
    :param kid_id: the kid id
    :param address: the address to delete
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.delete_forbidden_address(address)
        print("KID OBJECT: \n" + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "on_delete_button", status=address)


def update_forbidden_applications(kid_id, forbidden_applications):
    """
    update a forbidden applications and show changes
    :param kid_id: the kid id
    :param forbidden_applications: forbidden applications list to show
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.set_forbidden_applications(forbidden_applications)
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "handle_prohibited_apps_dialog_status", status=forbidden_applications)


def add_forbidden_application(kid_id, app):
    """
    add a forbidden application and show changes
    :param kid_id: the id of the ki0d
    :param app: the application
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.add_forbidden_application(app)
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "on_add_button", status=app)


def delete_forbidden_application(kid_id, app):
    """
    delete a forbidden application and show changes
    :param kid_id: the id of the ki0d
    :param app: the application
    :return: None
    """
    # get kid object by kid id
    kid = get_kid_by_kid_id(kid_id)
    # if the kid exist
    if kid is not None:
        kid.delete_forbidden_application(app)
        print("KID OBJECT: " + str(vars(kid)))
        # handle showing the data in gui
        wx.CallAfter(pub.sendMessage, "on_delete_button", status=app)


def get_kid_data(data):
    """
    handle the data about a kid that sent from the server
    :param data: a dict with
    username: the username  of the kid
    kid_id: the id of the kid
    remaining_time: the remaining time of the kid to use the computer for today
    active: answer if the kid is active right now or not
    computer_limit: if the computer is blocked or not
    internet_limit: if the internet use is blocked or not
    reached_addresses: a string of all the new prohibited addresses the user searched
    :return: None
    """
    username, kid_id, remaining_time, active, computer_limit, internet_limit, reached_addresses = data  # split the data
    # set the limitations as a boolean and not numbers
    limitations = from_digits_to_boolean_limitations_data(computer_limit, internet_limit)
    kid_id = int(kid_id)
    # set a new kid object for the kid by the data from the server:
    kid = Kid(username)
    kid.setKid(kid_id, remaining_time, active, limitations)
    last_kid = get_kid_by_username(username)
    if last_kid is None:
        kids.append(kid)
        print("NEW KID OBJECT: " + str(vars(kid)))
    else:
        index = kids.index(last_kid)
        kids[index] = kid
        print("UPDATE KID OBJECT: " + str(vars(kid)))

    wx.CallAfter(pub.sendMessage, "handle_kid_status", status=kid)

    print(f"reached_addresses ----> {reached_addresses}")


def from_digits_to_boolean_limitations_data(computer_limit, internet_limit):
    """
    replace the data (numbers => 0/1) to boolean (boolean => True/False)
    :param computer_limit: computer limitation
    :param internet_limit: internet limitation
    :return: list (bool)
    """
    limitations_string = f"{computer_limit, internet_limit}" # create the limitations string
    limitations_numbers = ""
    # run over the limitations string
    for char in limitations_string:
        if char.isdigit():
            limitations_numbers += char
    return [x == '1' for x in limitations_numbers]


def get_kid_by_username(username):
    """
    get a kid object by his username
    :param username: the username of the kid
    :return: the kid object or None
    """
    print("get_kid_by_username --- here")
    ret = None
    # run all over the kids
    for kid in kids:
        # if the username exist, return the kid
        if kid.get_username() == username:
            ret = kid
            break
    return ret


def get_kid_by_kid_id(kid_id):
    """
    get a kid object by his id
    :param kid_id: the id of the kid
    :return: the kid object or None
    """
    ret = None
    # run all over the kids
    for kid in kids:
        # if the kid id is in the kids list
        if str(kid.get_kid_id()) == str(kid_id):
            ret = kid
            break
    return ret


def send_sign_up(username, password):
    """
    send the username and password input of the user
    to signup
    :param username: the username input
    :param password: the password input
    :return: None
    """
    msg = build_send_sign_up(username, password)  # build the message
    comm.send(msg)  # send the message


def send_login(username, password):
    """
    send the username and password input of the user
    to login
    :param username: the username input
    :param password: the password input
    :return: None
    """
    msg = build_send_login(username, password)  # build the message
    comm.send(msg)  # send the message


def add_computer(mac_address, computer_name):
    """
    send the mac address and a nickname of the computer the parent wants to add
    to the system
    :param mac_address: the mac address of the computer to add
    :param computer_name: the nickname of the computer to add
    :return: None
    """
    msg = build_add_computer(mac_address, computer_name)  # build the message
    comm.send(msg)  # send the message


def add_kid(kid_username):
    """
    send the  kid's username to add a new kid to the system
    :param kid_username: the username account of a kid
    :return: None
    """
    msg = build_add_kid(kid_username)  # build the message
    comm.send(msg)  # send the message


def ask_all_computers():
    """
    ask from the server to get all the computers data
    (when the user reached to the main screen)
    :return: None
    """
    msg = build_ask_all_parent_computers_data()  # build the message
    comm.send(msg)  # send the message


def ask_all_kids_username():
    """
    ask from the server the username of all the parent's kids
    :return: None
    """
    msg = build_ask_all_parent_kids_username()  # build the message
    comm.send(msg)  # send the message


def send_parent_active_to_kid(kid_username):
    """
    when a parent get into a kid page profile, send this
    update to the server to get updates about the kid
    :param kid_username: the username the parent reached to his profile page
    :return: None
    """
    msg = build_send_parent_active_to_kid(kid_username)  # build the message
    comm.send(msg)  # send the message


def ask_time_limit(username):
    """
    ask from the server the time limit of a kid when the parent is
    in the "change time limit" screen
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_ask_time_limit(kid.get_kid_id())
        comm.send(msg)


def ask_forbidden_URLs(username):
    """
    ask from the server the prohibited addresses of a kid when the parent is
    in the "add / delete prohibited addresses" screen
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_ask_forbidden_addresses(kid.get_kid_id())
        comm.send(msg)


def ask_forbidden_applications(username):
    """
    ask from the server the prohibited addresses of a kid when the parent is
    in the "add / delete prohibited applications" screen
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_ask_forbidden_applications(kid.get_kid_id())
        comm.send(msg)


def ask_forbidden_hours(username):
    """
    ask from the server the prohibited hours of a kid when the parent is
    in the "add / delete prohibited hours" screen
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_ask_forbidden_hours(kid.get_kid_id())
        comm.send(msg)


def block_kid_computer(username):
    """
    send to the server to block the computer from a kid
    (when the kid will log in the computer will turn off)
    :param username: the username of a kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_computer_approval(kid.get_kid_id(), "b")
        comm.send(msg)


def allow_kid_computer(username):
    """
    send to the server to allow the computer to a kid
    (when the kid will log in the computer will no turn off)
    :param username: the username of a kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_computer_approval(kid.get_kid_id(), "a")
        comm.send(msg)


def block_kid_internet(username):
    """
    send to the server to block the internet to a kid
    (when the kid will log in the computer will block the ability to brows)
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_internet_approval(kid.get_kid_id(), "b")
        comm.send(msg)


def allow_kid_internet(username):
    """
    send to the server to allow the internet to a kid
    (when the kid will log in the computer will not block the ability to brows)
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_internet_approval(kid.get_kid_id(), "a")
        comm.send(msg)


def ask_browsing_tracking(username):
    """
    ask the browsing history list of a kid from the server
    :param username: the username of the kid
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_ask_browsing_tracking(kid.get_kid_id())
        comm.send(msg)
        print("asked history from the server")


def send_new_time_limitation(username, time_limit):
    """
    send a new time limit for a kid to update in the server
    :param username: the username of a kid
    :param time_limit: the new time limit
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        kid_id = kid.get_kid_id()
        msg = build_send_new_time_limit(kid_id, time_limit)
        comm.send(msg)


def add_set_of_forbidden_hours_to_server(username, set):
    """
    send a new set of hours for a kid to update in the server
    :param username: the username of a kid
    :param set: set of hours
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_add_set_of_forbidden_hours(kid.get_kid_id(), set)
        comm.send(msg)


def delete_set_of_forbidden_hours_to_server(username, set):
    """
    send a set of hours of a kid to delete from the server
    :param username: the username of a kid
    :param set: set of hours
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_delete_set_of_forbidden_hours(kid.get_kid_id(), set)
        comm.send(msg)


def add_new_forbidden_address_to_server(username, address):
    """
    send a new address to add to the forbidden addresses list in the server
    :param username: the username of the kid
    :param address: the forbidden address
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_add_forbidden_address(kid.get_kid_id(), address)
        comm.send(msg)


def delete_forbidden_address_to_server(username, address):
    """
    send an address to delete from the forbidden addresses list in the server
    :param username: the username of the kid
    :param address: the forbidden address
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_delete_forbidden_address(kid.get_kid_id(), address)
        comm.send(msg)


def add_new_forbidden_app_to_server(username, app):
    """
    send a new address to add to the forbidden applications list in the server
    :param username: the username of the kid
    :param app: the forbidden application
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_add_forbidden_application(kid.get_kid_id(), app)
        comm.send(msg)


def delete_forbidden_app_to_server(username, app):
    """
    send an address to delete from the forbidden applications list in the server
    :param username: the username of the kid
    :param app: the forbidden application
    :return: None
    """
    kid = get_kid_by_username(username)  # get a kid by the kid's username
    # if the kid exists
    if kid is not None:
        msg = build_delete_forbidden_application(kid.get_kid_id(), app)  # build the message
        comm.send(msg)  # send the message


def handle_gui_message(q):
    """
    handle message from the gui
    :param q: the queue of the messages
    :return: None
    """
    while True:
        msg = q.get()
        # login
        if msg[0] == "login":
            username, password = msg[1:]
            send_login(username,password)
        # registration
        if msg[0] == "registration":
            username, password = msg[1:]
            send_sign_up(username,password)
        # get all parent's computers (mac and nickname)
        if msg == "get parent's computers":
            ask_all_computers()
        # add a new computer to the system
        if msg[0] == "add new computer":
            add_computer(msg[1], msg[2])
        # add a new kid to the system
        if msg[0] == "add new kid":
            add_kid(msg[1])
        # get all the kid's username
        if msg == "get kids username":
            ask_all_kids_username()
        # send that the parent is active to a kid's profile page
        if msg[0] == "send parent active to kid":
            send_parent_active_to_kid(msg[1])
        # ass forbidden addresses of a kid
        if msg[0] == "ask forbidden URLs":
            ask_forbidden_URLs(msg[1])
        # add a new forbidden address to a kid
        if msg[0] == "add_new_forbidden_address_to_server":
            add_new_forbidden_address_to_server(msg[1], msg[2])
        # delete a forbidden address from a kid
        if msg[0] == "delete_forbidden_address_to_server":
            delete_forbidden_address_to_server(msg[1], msg[2])
        # ask forbidden applications of a kid
        if msg[0] == "ask_forbidden_applications":
            ask_forbidden_applications(msg[1])
        # add a new forbidden application to a kid
        if msg[0] == "add_new_forbidden_app_to_server":
            add_new_forbidden_app_to_server(msg[1], msg[2])
        # delete a forbidden application from a kid
        if msg[0] == "delete_forbidden_app_to_server":
            delete_forbidden_app_to_server(msg[1], msg[2])
        # ask history list of a kid
        if msg[0] == "ask_browsing_tracking":
            ask_browsing_tracking(msg[1])
        # send a new time limitation of a kid
        if msg[0] == "send_new_time_limitation":
            send_new_time_limitation(msg[1], msg[2])
        # ask forbidden hours of a kid
        if msg[0] == "ask_forbidden_hours":
            ask_forbidden_hours(msg[1])
        # add a new forbidden set of hours to a kid
        if msg[0] == "add_set_of_forbidden_hours_to_server":
            add_set_of_forbidden_hours_to_server(msg[1], msg[2])
        # delete a set of forbidden hours from a kid
        if msg[0] == "delete_set_of_forbidden_hours_to_server":
            delete_set_of_forbidden_hours_to_server(msg[1], msg[2])
        # allow kid computer
        if msg[0] == "allow_kid_computer":
            allow_kid_computer(msg[1])
        # block kid computer
        if msg[0] == "block_kid_computer":
            block_kid_computer(msg[1])


if __name__ == '__main__':
    # create the queue to handle messages
    q = queue.Queue()
    gui_q = queue.Queue()

    kids = []  # a list that contains an information about all the kids of the parent -> [Kid, Kid....]

    # create the comm object:
    comm = ClientComm(setting.server_ip, 1500, q, "p")

    threading.Thread(target=handle_message, args=(comm, q,)).start()  # run the handle message thread
    threading.Thread(target=handle_gui_message, args=(gui_q,)).start()  # run the handle gui message thread

    # run the gui
    app = wx.App()  # create the application
    frame = MyFrame(gui_q)  # create the frame
    frame.Show()  # show the frame
    app.MainLoop()  # run


# Logic checks:

# send_sign_up("carl", 1111)
# send_login("carl", 1111)
# add_computer("00-B0-D0-63-C2-26", "meni computer")
# add_computer("08:71:90:27:99:61", "itai computer")
# #add_computer("64:00:6a:42:4b:c8", "talmid computer")
# #add_computer("64:00:6a:42:4a:dc", "talmid computer") 64:00:6a:42:50:5e
# add_computer("64:00:6a:42:4a:b1", "talmid computer")
# ask_all_computers()
# add_kid("meni")
# time.sleep(2)
# add_kid("itai")
# add_kid("talmid")
# # time.sleep(1)
# #send_parent_active_to_kid("itai")
# send_parent_active_to_kid("talmid")
# time.sleep(1)
# # time.sleep(1)
# # print("heeeeeeeeeeerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
# # ask_browsing_tracking("itai")
# # ask_time_limit("itai")
# send_new_time_limitation("talmid", "00:07:30")
# # ask_forbidden_hours("itai")
# # time.sleep(1)
# # ask_forbidden_URLs("itai")
# # time.sleep(1)
# # ask_forbidden_applications("itai")
# time.sleep(1)
# print("\n---------------------CHANGES---------------------\n")
# # add_set_of_forbidden_hours_to_server("itai", "18:00-20:00")
# # delete_set_of_forbidden_hours_to_server("itai", "18:00-20:00")
# # time.sleep(1)
# # add_new_forbidden_address_to_server("talmid", "www.nba2.com")
# # time.sleep(2)
# # add_new_forbidden_app_to_server("talmid", "RoyalRumble2.exe")
#
# #block_kid_computer("talmid")
# allow_kid_computer("talmid")
# # allow_kid_internet("talmid")
# # block_kid_internet("talmid")
# add_new_forbidden_address_to_server("talmid", "coco.co.il")













