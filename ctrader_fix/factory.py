#!/usr/bin/env python

from twisted.internet.protocol import ClientFactory

class Factory(ClientFactory):
    messageSequenceNumber = 0
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.client = kwargs['client']
        self.delimiter = self.client.delimiter
    def connected(self):
        self.client._connected()
    def disconnected(self, reason):
        self.client._disconnected(reason)
    def received(self, message):
        self.client._received(message)
