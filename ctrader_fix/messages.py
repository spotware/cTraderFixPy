#!/usr/bin/env python

import datetime

class ResponseMessage:
    def __init__(self, message, delimiter = ""):
        self._message = message.replace(delimiter, "|")
        self._fields = {int(field.split("=")[0]):field.split("=")[1] for field in message.split(delimiter) if field != ""}

    def getFieldStr(self, fieldNumber):
        return self._fields[fieldNumber]

    def getFieldInt(self, fieldNumber):
        return int(self._fields[fieldNumber])

    def getFieldFloat(self, fieldNumber):
        return float(self._fields[fieldNumber])

    def getMessageType(self):
        return self._fields[35]

    def getMessage(self):
        return self._message

class RequestMessage:
    def __init__(self, messageType, sessionInfo, delimiter = ""):
        self._type = messageType
        self._sessionInfo = sessionInfo
        self._delimiter = delimiter

    def getMessage(self, sequenceNumber):
        body = self._getBody()
        if body is not None:
            header = self._getHeader(len(body), sequenceNumber)
            headerAndBody = f"{header}{self._delimiter}{body}{self._delimiter}"
        else:
            header = self._getHeader(0, sequenceNumber)
            headerAndBody = "{header}{self._delimiter}"
        trailer = self._getTrailer(headerAndBody)
        return f"{headerAndBody}{trailer}{self._delimiter}"

    def _getBody(self):
        return None

    def _getHeader(self, lenBody, sequenceNumber):
        fields = []
        fields.append(f"35={self._type}")
        fields.append(f"49={self._sessionInfo['SenderCompID']}")
        fields.append(f"56={self._sessionInfo['TargetCompID']}")
        fields.append(f"57={self._sessionInfo['TargetSubID']}")
        fields.append(f"50={self._sessionInfo['SenderSubID']}")
        fields.append(f"34={sequenceNumber}")
        fields.append(f"52={datetime.datetime.utcnow().strftime('%Y%m%d-%H:%M:%S')}")
        fieldsJoined = self._delimiter.join(fields)
        return f"8={self._sessionInfo['BeginString']}{self._delimiter}9={lenBody+len(fieldsJoined) + 2}{self._delimiter}{fieldsJoined}"

    def _getTrailer(self, headerAndBody):
        messageBytes = bytes(headerAndBody, "ascii")
        checksum = 0
        for byte in messageBytes:
            checksum += byte
        checksum = checksum % 256
        return f"10={str(checksum).zfill(3)}"

class LogonRequest(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("A", sessionInfo, delimiter)
        self.EncryptionScheme = 0

    def _getBody(self):
        fields = []
        fields.append(f"98={self.EncryptionScheme}")
        fields.append(f"108={self._sessionInfo['HeartBeat']}")
        if hasattr(self, "ResetSeqNum") and self.ResetSeqNum:
            fields.append(f"141=Y")
        fields.append(f"553={self._sessionInfo['Username']}")
        fields.append(f"554={self._sessionInfo['Password']}")
        return f"{self._delimiter.join(fields)}"


class Heartbeat(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("0", sessionInfo, delimiter)

    def _getBody(self):
        if hasattr(self, "TestReqId") is False:
            return None
        return f"112={self.TestReqId}"

class TestRequest(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("1", sessionInfo, delimiter)

    def _getBody(self):
        return f"112={self.TestReqId}"

class LogoutRequest(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("5", sessionInfo, delimiter)

class ResendRequest(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("2", sessionInfo, delimiter)

    def _getBody(self):
        fields = []
        fields.append(f"7={self.BeginSeqNo}")
        fields.append(f"16={self.EndSeqNo}")
        return f"{self._delimiter.join(fields)}"

class SequenceReset(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("4", sessionInfo, delimiter)

    def _getBody(self):
        fields = []
        if hasattr(self, "GapFillFlag"):
            fields.append(f"123={self.GapFillFlag}")
        fields.append(f"36={self.NewSeqNo}")
        return f"{self._delimiter.join(fields)}"

class MarketDataRequest(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("V", sessionInfo, delimiter)

    def _getBody(self):
        fields = []
        fields.append(f"262={self.MDReqID}")
        fields.append(f"263={self.SubscriptionRequestType}")
        fields.append(f"264={self.MarketDepth}")
        if hasattr(self, "MDUpdateType"):
            fields.append(f"265={self.MDUpdateType}")
        fields.append(f"267={self.NoMDEntryTypes}")
        fields.append(f"269={self.MDEntryType}")
        fields.append(f"146={self.NoRelatedSym}")
        fields.append(f"55={self.Symbol}")
        return f"{self._delimiter.join(fields)}"

class NewOrderSingle(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("D", sessionInfo, delimiter)

    def _getBody(self):
        fields = []
        fields.append(f"11={self.ClOrdID}")
        fields.append(f"55={self.Symbol}")
        fields.append(f"54={self.Side}")
        fields.append(f"60={self.TransactTime.strftime('%Y%m%d-%H:%M:%S')}")
        fields.append(f"38={self.OrderQty}")
        fields.append(f"40={self.OrdType}")
        if hasattr(self, "Price"):
            fields.append(f"44={self.Price}")
        if hasattr(self, "StopPx"):
            fields.append(f"99={self.StopPx}")
        if hasattr(self, "ExpireTime"):
            fields.append(f"126={self.ExpireTime.strftime('%Y%m%d-%H:%M:%S')}")
        if hasattr(self, "PosMaintRptID"):
            fields.append(f"721={self.PosMaintRptID}")
        if hasattr(self, "Designation"):
            fields.append(f"494={self.Designation}")
        return f"{self._delimiter.join(fields)}"

class OrderStatusRequest(RequestMessage):
    def __init__(self, sessionInfo, delimiter = ""):
        super().__init__("H", sessionInfo, delimiter)

    def _getBody(self):
        fields = []
        fields.append(f"11={self.ClOrdID}")
        if hasattr(self, "Side"):
            fields.append(f"54={self.Side}")
        return f"{self._delimiter.join(fields)}"

