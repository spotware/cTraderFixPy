### Introduction

A Python package for interacting with cTrader FIX API.

This package is developed and maintained by Spotware.

You can use cTraderFix on all kinds of Python apps, it uses Twisted to send and receive messages asynchronously.

Github Repository: https://github.com/spotware/cTraderFixPy

### Installation

You can install cTraderFix from pip:

```
pip install ctrader-fix
```

### Usage

```python

from twisted.internet import reactor
from inputimeout import inputimeout, TimeoutOccurred
import json
from ctrader_fix import *

# Callback for receiving all messages
def onMessageReceived(client, responseMessage):
    print("Received: ", responseMessage.getMessage().replace("�", "|"))
    messageType = responseMessage.getFieldValue(35)
    if messageType == "A":
        print("We are logged in")

# Callback for client disconnection
def disconnected(client, reason): 
    print("Disconnected, reason: ", reason)

# Callback for client connection
def connected(client):
    print("Connected")
    logonRequest = LogonRequest(config)
    send(logonRequest)

# you can use two separate config files for QUOTE and TRADE
with open("config-trade.json") as configFile:
    config = json.load(configFile)

client = Client(config["Host"], config["Port"], ssl = config["SSL"])

# Setting client callbacks
client.setConnectedCallback(connected)
client.setDisconnectedCallback(disconnected)
client.setMessageReceivedCallback(onMessageReceived)
# Starting the client service
client.startService()
reactor.run()

```

