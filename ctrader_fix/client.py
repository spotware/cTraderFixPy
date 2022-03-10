#!/usr/bin/env python

from twisted.internet.endpoints import clientFromString
from twisted.application.internet import ClientService
from messages import *
from factory import Factory
from twisted.internet import reactor
from fixProtocol import FixProtocol
from twisted.internet import reactor

class Client(ClientService):
    def __init__(self, host, port, ssl=False, delimiter = "", retryPolicy=None, clock=None, prepareConnection=None, numberOfMessagesToSendPerSecond=5):
        self._runningReactor = reactor
        self.numberOfMessagesToSendPerSecond = numberOfMessagesToSendPerSecond
        self.delimiter = delimiter
        endpoint = clientFromString(self._runningReactor, f"ssl:{host}:{port}" if ssl else f"tcp:{host}:{port}")
        self._factory = Factory.forProtocol(FixProtocol, client=self)
        super().__init__(endpoint, self._factory, retryPolicy=retryPolicy, clock=clock, prepareConnection=prepareConnection)
        self._events = dict()
        self._responseDeferreds = dict()
        self.isConnected = False

    def startService(self):
        if self.running:
            return
        ClientService.startService(self)

    def stopService(self):
        if self.running and self.isConnected:
            ClientService.stopService(self)

    def _connected(self):
        self.isConnected = True
        if hasattr(self, "_connectedCallback"):
            self._connectedCallback(self)

    def _disconnected(self, reason):
        self.isConnected = False
        self._responseDeferreds.clear()
        if hasattr(self, "_disconnectedCallback"):
            self._disconnectedCallback(self, reason)

    def _received(self, responseMessage):
        if hasattr(self, "_messageReceivedCallback"):
            self._messageReceivedCallback(self, responseMessage)

    def send(self, requestMessage):
        requestMessage.delimiter = self.delimiter
        diferred = self.whenConnected(failAfterFailures=1)
        diferred.addCallback(lambda protocol: protocol.send(requestMessage))
        return diferred

    def changeMessageSequenceNumber(self, newMessageSequenceNumber):
        self._factory.messageSequenceNumber = newMessageSequenceNumber

    def getMessageSequenceNumber(self):
        return self._factory.messageSequenceNumber

    def setConnectedCallback(self, callback):
        self._connectedCallback = callback

    def setDisconnectedCallback(self, callback):
        self._disconnectedCallback = callback

    def setMessageReceivedCallback(self, callback):
        self._messageReceivedCallback = callback


if __name__ == "__main__":
    client = Client("h51.p.ctrader.com", 5202)
    quoteSessionInfo = {"Username": 3279203, "Password": 3279203, "BeginString": "FIX.4.4", "SenderCompID": "demo.icmarkets.3279203", "SenderSubID": "QUOTE", "TargetCompID": "cServer", "TargetSubID": "QUOTE", "HeartBeat": 30}
    tradeSessionInfo = {"Username": 3279203, "Password": 3279203, "BeginString": "FIX.4.4", "SenderCompID": "demo.icmarkets.3279203", "SenderSubID": "TRADE", "TargetCompID": "cServer", "TargetSubID": "TRADE", "HeartBeat": 30}
    isMessageSent = False

    def onConnected(client):
        logonMessage = LogonRequest(tradeSessionInfo)
        client.send(logonMessage)

    def onMessageReceived(client, responseMessage):
        print("Received: ", responseMessage.getMessage())
        global isMessageSent
        if isMessageSent is True:
            return
        isMessageSent = True
        request = SecurityListRequest(tradeSessionInfo)
        request.SecurityReqID = "A"
        request.SecurityListRequestType = 0
        client.send(request)

    client.setConnectedCallback(onConnected)
    client.setMessageReceivedCallback(onMessageReceived)
    client.startService()

    reactor.run()
