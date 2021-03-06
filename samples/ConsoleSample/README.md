# Console Sample

This is the console sample for cTrader FIX API Python package.

It uses a single thread which is the Python main execution thread for both getting user inputs and sending/receiving messages to/from API.

Because it uses only the Python main execution thread the user input command has a time out, and if you don't enter your command on that specific time period it will block for few seconds and then it starts accepting user command again.

This sample uses [inputimeout](https://pypi.org/project/inputimeout/) Python package, you have to install it before running the sample. 

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
