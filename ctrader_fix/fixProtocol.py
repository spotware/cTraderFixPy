#!/usr/bin/env python

from twisted.internet.protocol import Protocol
from ctrader_fix.messages import ResponseMessage

class FixProtocol(Protocol):
    _currentMessage = ''
    def connectionMade(self):
        self.factory.messageSequenceNumber = 0
        super().connectionMade()
        self.factory.connected()

    def connectionLost(self, reason):
        super().connectionLost(reason)
        self.factory.disconnected(reason)

    def dataReceived(self, data):
        dataString = data.decode("ascii")
        self._currentMessage += dataString
        if f"{self.factory.delimiter}10=" in dataString and dataString.endswith(self.factory.delimiter):         
            responseMessage = ResponseMessage(self._currentMessage, self.factory.delimiter)
            self._currentMessage = ''
            self.factory.received(responseMessage)

    def send(self, requestMessage):
        self.factory.messageSequenceNumber += 1
        messageString = requestMessage.getMessage(self.factory.messageSequenceNumber)
        return self.transport.write(messageString.encode("ascii"))
