
from uuid import getnode
import socket


def get_macAddress():
    """ returns  mac address"""
    return ':'.join(['{:02x}'.format((getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

