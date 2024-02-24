import queue
from CurrentKidInfo import CurrentKidInfo
from Limitations import Limitations
from ClientCom import ClientComm
from getMyMac import *
from KidProtocol import *
import os
import psutil
import threading
import time
from handleKeyboard import KeyHandle
import setting


# runs as a thread
def handle_message(q):
    """
    handle messages from the server
    :param q: the messages queue from the server
    :return: None
    """
    while True:
        data = q.get()
        print("data from server: ", data)
        data_tuple = unpack(data)
        print(data_tuple)

        # if the command number is 0, turn of the computer
        if data_tuple[0] == 1:
            #turn_off_computer()
            print("TURN OFF THE COMPUTER")

        elif data_tuple[0] == 2:
            # the server sent data about the current kid using the computer
            # save the data in CurrentKidInfo object and set the limitations
            # by what the data conclude:
            reset_CurrentKidInfo(data_tuple[1])

        elif data_tuple[0] == 7:
            print("ALLOW THE KID USING THE INTERNET")

        elif data_tuple[0] == 8:
            print("BLOCK THE KID USING THE INTERNET")
            block_internet()

        elif data_tuple[0] == 9:
            # add or delete an address to / from the prohibited list
            print(data_tuple[1])
            data_string = data_tuple[1][0]
            if str(data_string).startswith("a"):
                # add address
                address = str(data_string)[1:]
                current_kid.add_forbidden_address(address)
                print(f"ADDRESSES - {current_kid.get_forbidden_addresses()}")
            if str(data_string).startswith("d"):
                # delete address
                address = str(data_string)[1:]
                current_kid.delete_forbidden_address(address)
                print(f"ADDRESSES - {current_kid.get_forbidden_addresses()}")

        elif data_tuple[0] == 10:
            # add or delete application to / from the prohibited list
            print(data_tuple[1])
            data_string = data_tuple[1][0]
            if str(data_string).startswith("a"):
                # add app
                app = str(data_string)[1:]
                current_kid.add_forbidden_application(app)
                print(f"APPLICATIONS - {current_kid.get_forbidden_applications()}")
            if str(data_string).startswith("d"):
                # delete app
                app = str(data_string)[1:]
                current_kid.delete_forbidden_application(app)
                print(f"APPLICATIONS - {current_kid.get_forbidden_applications()}")


def reset_CurrentKidInfo(info):
    """
    reset the kid object when ther is a
    new kid that use the computer
    :param info: information
    :return:
    """
    current_kid.set_kid_id(info[0])  # set the kid_id
    if info[1] is not '':
        current_kid.set_forbidden_addresses(info[1].split(","))  # set the prohibited addresses
    if info[2] is not '':
        current_kid.set_forbidden_applications(info[2].split(","))   # set the prohibited applications

    limitations = list(info[-1])
    limitations.insert(0, False)
    print("LIMITATIONS TO SET IN INFO OBJECT ARE: " + str(limitations))
    current_kid.set_kid_blocks_limitations(limitations)
    print("INFO OBJECT: " + str(vars(current_kid)))


def send_mac_address():
    """
    sending the mac address of the current computer to the server
    :return:
    """
    mac_address = get_macAddress()
    msg = build_send_mac_address(mac_address)
    comm.send(msg)
    print("sent the mac address")


def send_kid_active(username):
    """
    send to the server when a new kid is active
    :param username: the kid username account name
    :return: None
    """
    msg = build_send_kid_active(username)
    comm.send(msg)


def send_kid_not_active(username):
    """
    send to the server when the last kid is not active anymore
    :param username: the kid username account name
    :return: None
    """
    msg = build_send_kid_not_active(username)
    comm.send(msg)


# runs as a thread
def get_current_activity():
    """
    a thread that always knows the active situation of the kid
    users of the current computer and send changes to the server
    :return: None
    """
    # get who is active on the computer:
    active_username = ""  # the active username account
    while True:
        last_username = active_username  # the last username
        active_username = os.getlogin()  # the current username
        # if the username changed
        if active_username != last_username:
            print(f"new user is active!\nusername account: {active_username}\n")

            # if there is an active kid before and now he is not,
            # send to the server that he is not active anymore:
            last_active_username = current_kid.get_kid_username()
            if last_active_username is not "":
                send_kid_not_active(last_active_username)

            # new user is active, reset CurrentKidInfo object:
            current_kid.reset()
            # set the username of the CurrentKidInfo object to be
            # the username of the new logged in user
            current_kid.set_kid_username(active_username)

            # send to the server that a new kid is using the computer:
            send_kid_active(active_username)
        time.sleep(2)


def turn_off_computer():
    """
    turning off the computer
    :return: None
    """
    print("Turning Off")
    os.system('shutdown /s /t 1')  # turn of the computer


def block_internet():
    """
    block the user browsing abilities by closing automatically the computer browsers
    every time the user tries to open them.
    :return:
    """
    # put 'chrome.exe' in the list of processes to kill
    current_kid.add_forbidden_application('chrome.exe')
    current_kid.add_forbidden_application('Google Chrome')
    print(vars(current_kid))



# runs as a thread
def handle_browsing():
    """
    Using a thread that runs and does - a key logger that captures every address that the
    user tries to access, sends it to the server, and if it is forbidden,
    it closes the browsers
    :return:
    """
    while True:
        address = keyHandle_queue.get()
        # send the address to the server
        send_address(current_kid.get_kid_id(), address)
        time.sleep(1)


def send_address(kid_id, address):
    """
    send a new address the kid tried to reach
    :param kid_id: the id address of the kid
    :param address: the address the kid tried to access
    :return:
    """
    msg = build_send_address(kid_id, address)
    comm.send(msg)


def BlockProcess():
    """
    blocking a prohibited processes (applications)
    :return: None
    """
    while True:
        time.sleep(2)  # wait
        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                process_name = proc.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

            else:
                # if the process name is in the forbidden applications, kill the process
                if process_name in current_kid.get_forbidden_applications():
                    # kill the process
                    try:
                        proc.kill()
                    except Exception as e:
                        print(e)


if __name__ == '__main__':
    # create the queue to handle messages

    q = queue.Queue()
    current_kid = CurrentKidInfo()  # init the CurrentKidInfo object

    # create the comm object:
    comm = ClientComm(setting.server_ip, 1500, q, "k")


    print("running kid's client")
    threading.Thread(target=handle_message, args=(q,)).start()

    send_mac_address()
    time.sleep(2)
    threading.Thread(target=get_current_activity).start()

    time.sleep(2)
    keyHandle_queue = queue.Queue()
    keyHandle = KeyHandle(keyHandle_queue)
    threading.Thread(target=keyHandle.start).start()
    threading.Thread(target=BlockProcess).start()
    threading.Thread(target=handle_browsing()).start()



