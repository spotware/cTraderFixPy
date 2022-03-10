#!/usr/bin/env python

import requests
from twisted.internet import reactor
from inputimeout import inputimeout, TimeoutOccurred
import webbrowser
import datetime
import json
from client import Client
from messages import *

# you can have two separate config files for QUOTE and TRADE
with open("config-trade.json") as configFile:
    config = json.load(configFile)

client = Client(config["Host"], config["Port"], ssl = config["SSL"])

def showHelp():
    print("Commands (Parameters with an * are required)")
    print("You can't use QUOTE commands if your connection and session is TRADE and vice versa")
    print("Command and parameter names are case-sensitive")
    print("For date and time parameters please provide the value in '%Y%m%d-%H:%M:%S' Python format")
    print("To get valid values for parameters please check the cTrader FIX Engine, Rules of Engagement PDF document")
    print("\nCommon Commands (You can use on both TRADE and QUOTE):")
    print("* LogonRequest: ResetSeqNum")
    print("* LogoutRequest")
    print("* Heartbeat: TestReqId")
    print("* TestRequest: *TestReqId")
    print("* ResendRequest: *BeginSeqNo *EndSeqNo")
    print("* SequenceReset: *NewSeqNo GapFillFlag")
    print("* SecurityListRequest: *SecurityReqID *SecurityListRequestType Symbol ")
    print("\n")
    print("QUOTE Commands:")
    print("* MarketDataRequest: *MDReqID *SubscriptionRequestType *MarketDepth *NoMDEntryTypes *MDEntryType *NoRelatedSym *Symbol MDUpdateType")
    print("\n")
    print("TRADE Commands:")
    print("* NewOrderSingle: *ClOrdID *Symbol *Side *OrderQty *OrdType Price StopPx ExpireTime PosMaintRptID Designation")
    print("* OrderStatusRequest: *ClOrdID Side")
    print("* OrderMassStatusRequest: *MassStatusReqID *MassStatusReqType IssueDate")
    print("* RequestForPositions: *PosReqID PosMaintRptID")
    print("* OrderCancelRequest: *OrigClOrdID *ClOrdID OrderID")
    print("* OrderCancelReplaceRequest: *OrigClOrdID *ClOrdID *OrderQty OrderID Price StopPx ExpireTime")
    print("\n")
    print("Examples")
    print("LogonRequest ResetSeqNum=Y")
    print("SecurityListRequest SecurityReqID=a SecurityListRequestType=0")
    print("MarketDataRequest MDReqID=a SubscriptionRequestType=1 MarketDepth=0 NoMDEntryTypes=1 MDEntryType=0 NoRelatedSym=1 Symbol=1")
    print("NewOrderSingle ClOrdID=a Symbol=1 Side=2 OrderQty=10000 OrdType=1 Designation=Test")
    print("NewOrderSingle ClOrdID=a Symbol=1 Side=2 OrderQty=10000 OrdType=3 StopPx=1.102 ExpireTime=20220410-12:11:10.437 Designation=Test")
    print("OrderStatusRequest ClOrdID=a")
    print("OrderMassStatusRequest MassStatusReqID=1 MassStatusReqType=7")
    print("RequestForPositions PosReqID=a")
    print("OrderCancelRequest OrigClOrdID=a ClOrdID=b")
    print("OrderCancelReplaceRequest OrigClOrdID=a ClOrdID=c OrderQty=20000 Price=1.102")
    reactor.callLater(3, callable=executeUserCommand)

def setParameters(request, **kwargs):
    for name, value in kwargs.items():
        setattr(request, name, value)

def send(request):
    diferred = client.send(request)
    diferred.addCallback(lambda _: print("\nSent: ", request.getMessage(client.getMessageSequenceNumber()).replace("", "|")))

def logonRequest(**kwargs):
    request = LogonRequest(config)
    setParameters(request, **kwargs)
    send(request)

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

def executeUserCommand():
    try:
        print("\n")
        userInput = inputimeout("Command (ex: Help): ", timeout=30)
    except TimeoutOccurred:
        print("Command Input Timeout")
        reactor.callLater(3, callable=executeUserCommand)
        return
    if userInput.lower() == "help":
        showHelp()
        return
    userInputSplit = userInput.split(" ")
    if not userInputSplit:
        print("Command split error: ", userInput)
        reactor.callLater(3, callable=executeUserCommand)
        return
    command = userInputSplit[0]
    parameters = {}
    try:
        parameters = {parameter.split("=")[0]:parameter.split("=")[1] for parameter in userInputSplit[1:]}
    except:
        print("Invalid parameters: ", userInput)
        reactor.callLater(3, callable=executeUserCommand)
    if command in commands:
        request = commands[command](config)
        setParameters(request, **parameters)
        send(request)
    else:
        print("Invalid Command: ", userInput)
        reactor.callLater(3, callable=executeUserCommand)

def onMessageReceived(client, responseMessage): # Callback for receiving all messages
    print("\nReceived: ", responseMessage.getMessage().replace("", "|"))
    reactor.callLater(3, callable=executeUserCommand)

def disconnected(client, reason): # Callback for client disconnection
    print("\nDisconnected, reason: ", reason)

def connected(client):
    print("Connected")
    executeUserCommand()

# Setting client callbacks
client.setConnectedCallback(connected)
client.setDisconnectedCallback(disconnected)
client.setMessageReceivedCallback(onMessageReceived)
# Starting the client service
client.startService()
reactor.run()
