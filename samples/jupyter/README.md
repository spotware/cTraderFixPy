# Jupyter Sample

This is sample that will show you how to use the cTraderFix Python package on a Jupyter notebook.

In the notebook we logon, retrive account securities/symbols, and then we execute a market order.

Before running the sample you have to create a config file and fill it with your trading account FIX API credentials.

Then replace the config file name on sample main file to your config file name.

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
