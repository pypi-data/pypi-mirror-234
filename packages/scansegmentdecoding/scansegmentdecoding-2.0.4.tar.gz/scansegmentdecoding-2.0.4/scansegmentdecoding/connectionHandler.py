#
# Copyright (c) 2023 SICK AG
# SPDX-License-Identifier: MIT
#

import socket


class UDPHandler:
    """This class receives UDP packages which arrive from a specified port.
    """

    def __init__(
        self,
        _localAddress: str,
        _localPort: int,
        _remoteAddress: str,
        _remotePort: int,
        _bufferSize: int
    ):
        """Opens a new socket.

        Args:
            _localAddress (str): IP adress of the receiver
            _localPort (int): Port to listen on
            _remoteAddress (str): IP adress of the device
            _remotePort (int): Port to send from
            _bufferSize (int): Size of the receive buffer
        """
        self.localIp = _localAddress
        self.localPort = _localPort
        self.remoteIp = _remoteAddress
        self.remotePort = _remotePort
        self.bufferSize = _bufferSize
        self.recTimeout = 3
        self.noErrorFlag = False

        self._openUDPSocket()
        self.counter = 0
        self.lastErrorCode = None
        self.lastErrorMessage = ""

    def __del__(self):
        """Closes the socket.
        """
        self.client.close()

    def _openUDPSocket(self):
        """Opens the scoket and binds it to the configured port
        """
        self.client = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.client.bind((self.localIp, self.localPort))

        self.client.settimeout(self.recTimeout)

    def receiveNewScanSegment(self):
        """Waits on a new scan segment on the configured UDP port.

        Returns:
            tuple[bytes, any]: Tuple of the received data and the retAdress
        """
        try:
            self.noErrorFlag = True
            data = self.client.recvfrom(self.bufferSize)
            self.counter += 1
            return data
        except TimeoutError as e:
            print(e)
        except socket.error as error:
            # print error code
            self.noErrorFlag = False
            self.lastErrorCode = error.errno
            self.lastErrorMessage = str(error)
            print("Error receiving udp packet. Error Code: {}".format(error.errno))

    def hasNoError(self):
        """Check whether the UDPHandler is in an error state

        Returns:
            boolean: True if there was no error, false otherwise
        """
        return self.noErrorFlag

    def getDataCounter(self):
        """Get the number of received UDP Datagrams

        Returns:
            int: The number of received UDP Datagrams
        """
        return self.counter

    def getLastErrorCode(self):
        """Get the last error code.

        Returns:
            int: The error code of the error that last occured
        """
        return self.lastErrorCode
