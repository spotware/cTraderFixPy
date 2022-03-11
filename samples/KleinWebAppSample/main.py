#!/usr/bin/env python

from klein import Klein
from templates import ClientAreaElement
import json
from twisted.internet import endpoints, reactor, defer
from twisted.web.server import Site
import sys
from twisted.python import log
from twisted.web.static import File
from ctrader_fix import *

host = "localhost"
port = 8080

# you can use two separate config files for QUOTE and TRADE
with open("config-trade.json") as configFile:
    config = json.load(configFile)

client = Client(config["Host"], config["Port"], ssl = config["SSL"])

app = Klein()

@app.route('/')
def root(request):
    return ClientAreaElement()

@app.route('/css/', branch=True)
def css(request):
    return File("./css")

@app.route('/js/', branch=True)
def js(request):
    return File("./js")

def connected(client):
    print("Client Connected") 

def disconnected(client, reason):
    print("Client Disconnected, reason: ", reason)

responseDeferred = None

def onMessageReceived(client, responseMessage):
    global responseDeferred
    lastReceivedMessage = responseMessage.getMessage().replace("", "|")
    if responseDeferred is not None:
        responseDeferred.callback(lastReceivedMessage)
    print("Received: ", lastReceivedMessage)
    responseDeferred= None

def setParameters(request, **kwargs):
    for name, value in kwargs.items():
        setattr(request, name, value)

def send(request):
    diferred = client.send(request)
    diferred.addCallback(lambda _: print("Sent: ", request.getMessage(client.getMessageSequenceNumber()).replace("", "|")))

commands = {
    "LogonRequest": LogonRequest,
    "LogoutRequest": LogoutRequest,
    "Heartbeat": Heartbeat,
    "TestRequest": TestRequest,
    "ResendRequest": ResendRequest,
    "SequenceReset": SequenceReset,
    "SecurityListRequest": SecurityListRequest,
    "MarketDataRequest": MarketDataRequest,
    "NewOrderSingle": NewOrderSingle,
    "OrderStatusRequest": OrderStatusRequest,
    "OrderMassStatusRequest": OrderMassStatusRequest,
    "RequestForPositions": RequestForPositions,
    "OrderCancelRequest": OrderCancelRequest,
    "OrderCancelReplaceRequest": OrderCancelReplaceRequest}

def encodeResult(result):
    return f'{{"result": "{result}"}}'.encode(encoding = 'UTF-8')

@app.route('/get-data')
def getData(request):
    request.responseHeaders.addRawHeader(b"content-type", b"application/json")
    result = ""
    userInput = request.args.get(b"command", [None])[0]
    if (userInput is None or userInput == b""):
        result = f"Invalid Command: {userInput}"
    else:
        userInputSplit = userInput.decode('UTF-8').split(" ")
        if not userInputSplit:
            result = f"Command split error: {userInput}"
        else:
            command = userInputSplit[0]
            parameters = {}
            try:
                parameters = {parameter.split("=")[0]:parameter.split("=")[1] for parameter in userInputSplit[1:]}
                if command in commands:
                    request = commands[command](config)
                    setParameters(request, **parameters)
                    global responseDeferred
                    responseDeferred = defer.Deferred()
                    responseDeferred.addTimeout(5, reactor)
                    responseDeferred.addCallback(encodeResult)
                    send(request)
                    return responseDeferred
                else:
                    result = f"Invalid Command: {userInput}"
            except:
                result = f"Invalid parameters: {userInput}"
    if type(result) is str:
        result = encodeResult(result)
    print(result)
    return result

log.startLogging(sys.stdout)

# Setting client callbacks
client.setConnectedCallback(connected)
client.setDisconnectedCallback(disconnected)
client.setMessageReceivedCallback(onMessageReceived)
# Starting the client service
client.startService()

endpoint_description = f"tcp6:port={port}:interface={host}"
endpoint = endpoints.serverFromString(reactor, endpoint_description)
site = Site(app.resource())
site.displayTracebacks = True

endpoint.listen(site)
reactor.run()
