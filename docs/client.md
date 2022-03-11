### Client Class

You will use an instance of this class to interact with API.

Each instance of this class will have one connection to API, either QUOTE or TRADE.

The client class is driven from Twisted ClientService class, and it abstracts away all the connection / reconnection complexities from you.

### Creating a Client

Let's create an isntance of Client class:

```python

from ctrader_fix import *

client = Client(config["Host"], config["Port"], ssl = config["SSL"])

```

It's constructor has several parameters that you can use for controling it behavior:

* host: The API host endpoint, you can get it from your cTrader FIX settings

* port: The API host port number, you can get it from your cTrader FIX settings

* ssl: It't bool flag, if Yes client will use SSL for connection otherwise it will use plain TCP connection

***The SSL connection is not working for now***

There are three other optional parameters which are from Twisted client service, you can find their detail here: https://twistedmatrix.com/documents/current/api/twisted.application.internet.ClientService.html 

### Callbacks

To use your client you have to set it's call backs:

* ConnectedCallback(client): This callback will be called when client gets connected, use client setConnectedCallback method to assign a callback for it

* DisconnectedCallback(client, reason): This callback will be called when client gets disconnected, use client setDisconnectedCallback method to assign a callback for it

* MessageReceivedCallback(client, message): This callback will be called when a message is received, it's called for all message types, use setMessageReceivedCallback to assign a callback for it

Use the connected call back to send a logon message.

And after logon use your message received call back to continue your interaction with API.
