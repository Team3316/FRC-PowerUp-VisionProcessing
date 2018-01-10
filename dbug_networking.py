import socket
from dbug_result_object import DBugResult
from logger import logger
from constants import *

class DBugNetworking(object):
    """
    A class to send data to a UDP socket
    """

    ERROR_VALUE = DBugResult()

    def __init__(self, host, port):
        """
        :param host: The host name to be connected to.
        :param port: The port for the communication.
        """

        self._address = None
        self.host = host
        self.port = port
        self.find_network_addr()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def format_parameter(param):
        return '{0:.2f}'.format(float(param))

    def find_network_addr(self):
        """
        Setting self._address according to the ip retrieved using the given host(name) and the given port
        :return:
        """
        try:
            self._address = (socket.gethostbyname(self.host), self.port)
            logger.debug("Finally managed to get host: %r" % (self._address,))

        except Exception as e:
            logger.error("Couldn't find host, error: " + str(e))

            self._address = (FALLBACK_ROBORIO_IP, self.port)

    def format_data(self, result_obj):
        """
        :return: result_obj as a dictionary with the data in result_obj
        """
        if result_obj is not None:
            identified = 1
        else:
            identified = 0
            result_obj = self.ERROR_VALUE

        return dict(AA=DBugNetworking.format_parameter(result_obj.azimuth_angle),
                    IOD=DBugNetworking.format_parameter(identified))

    def send_data(self, result_obj=None):
        """
        Sending the given result_obj to the host of self
        If no previous address (ip, port) was found trying to reconnect
        :param result_obj: The DBugResult instance to send
        :return: None
        """
        if self._address is None:
            self.find_network_addr()

        formatted_data = str(self.format_data(result_obj))
        logger.info("Sending data: " + formatted_data)
        self.sock.sendto(formatted_data.replace(' ', '') + '\n', self._address)

    def send_no_data(self):
        self.send_data()
