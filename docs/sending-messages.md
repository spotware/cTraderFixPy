### Messages

The package has a class for each of the cTrader FIX API client side messages.

You have to use those classes to send request messages.

To set fields of a message you should use message instance attributes and use exact field names that are defined on cTrader FIX Engine, Rules of Engagement document.

### Examples

Let's create some messages:

```python
# All mesages contructors requires the config to be passes a parameter
logonRequests = LogonRequest(config)

securityListRequest = SecurityListRequest(config)
securityListRequest.SecurityReqID = "A"
securityListRequest.SecurityListRequestType = 0

newOrderSingle = NewOrderSingle(config)
newOrderSingle.ClOrdID = "B"
newOrderSingle.Symbol = 1
newOrderSingle.Side = 1
newOrderSingle.OrderQty = 1000
newOrderSingle.OrdType = 1
newOrderSingle.Designation = "From FIX"
```

### Sending

To send a message you must use the client send method:

```python
# It returns a Twisted diferred
diferred = client.send(request)
diferred.addCallback(lambda _: print("\nSent: ", request.getMessage(client.getMessageSequenceNumber()).replace("", "|")))
```

You can only call the client send method from OnMessageReceived call back or connected callback.
