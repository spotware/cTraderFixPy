### Config

When you create a request message you have to pass a config, this config should be a dictionary like object with these keys:

* Host: The FIX host that will be used for client connection
* Port: The port number of host
* SSL: true/false, this can be used by client if SSL connected is required
* Username: Your cTrader trading account number
* Password: Your cTrader trading account password
* BeginString: Message begin string (FIX.4.4)
* SenderCompID: Your cTrader FIX SenderCompID 
* SenderSubID: Your cTrader FIX SenderSubID (QUOTE/TRADE)
* TargetCompID: Your cTrader FIX TargetCompID (cServer),
* TargetSubID: Your cTrader FIX TargetSubID (QUOTE),
* HeartBeat: The heartbeat seconds (30)

You can get the values for most of them from your cTrader FIX settings.

You can use a JSON file to save your configuration, check our samples.

### JSON Sample

```json
{
  "Host": "h51.p.ctrader.com",
  "Port": 5201,
  "SSL": false,
  "Username": "3279204",
  "Password": "3279204",
  "BeginString": "FIX.4.4",
  "SenderCompID": "demo.icmarkets.3279203",
  "SenderSubID": "QUOTE",
  "TargetCompID": "cServer",
  "TargetSubID": "QUOTE",
  "HeartBeat": "30"
}
```

You can use it like this:

```python
with open("config.json") as configFile:
    config = json.load(configFile)

# For client
client = Client(config["Host"], config["Port"], ssl = config["SSL"])

# For request messages
logonRequest = LogonRequest(config)
```
