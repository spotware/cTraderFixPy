# cTraderFixPy


[![PyPI version](https://badge.fury.io/py/ctrader-fix.svg)](https://badge.fury.io/py/ctrader-fix)
![versions](https://img.shields.io/pypi/pyversions/ctrader-fix.svg)
[![GitHub license](https://img.shields.io/github/license/spotware/cTraderFixPy.svg)](https://github.com/spotware/cTraderFixPy/blob/main/LICENSE)

A Python package for interacting with cTrader FIX API.

This package uses Twisted and it works asynchronously.

- Free software: MIT
- Documentation: https://spotware.github.io/cTraderFixPy/.


## Features

* Works asynchronously by using Twisted

* Allows you to easily interact with cTrader FIX API and it manages everything in background

* Generate FIX message by using Python objects

## Insallation

```
pip install ctrader-fix
```

# Config

Config file sample:

```json
{
  "Host": "",
  "Port": 0,
  "SSL": false,
  "Username": "",
  "Password": "",
  "BeginString": "FIX.4.4",
  "SenderCompID": "",
  "SenderSubID": "QUOTE",
  "TargetCompID": "cServer",
  "TargetSubID": "QUOTE",
  "HeartBeat": "30"
}
```

# Usage

```python
from twisted.internet import reactor
import json
from ctrader_fix import *

# Callback for receiving all messages
def onMessageReceived(client, responseMessage):
    print("Received: ", responseMessage.getMessage().replace("", "|"))
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

Please check documentation or samples for a complete example.

## Dependencies

* <a href="https://pypi.org/project/twisted/">Twisted</a>
