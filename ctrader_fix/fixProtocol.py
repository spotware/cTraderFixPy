#!/usr/bin/env python

from twisted.internet.protocol import Protocol
from messages import ResponseMessage

class FixProtocol(Protocol):
    _messageSequenceNumber = 0
    def connectionMade(self):
        super().connectionMade()
        self.factory.connected()

    def connectionLost(self, reason):
        super().connectionLost(reason)
        self.factory.disconnected(reason)

    def dataReceived(self, data):
        responseMessage = ResponseMessage(data.decode("ascii"))
        self.factory.received(responseMessage)

    def send(self, requestMessage):
        self._messageSequenceNumber += 1
        messageString = requestMessage.getMessage(self._messageSequenceNumber)
        print("Sending: ", messageString)
        return self.transport.write(messageString.encode("ascii"))
