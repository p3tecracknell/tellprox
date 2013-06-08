class MSensor(object):
    def __init__(self, protocol, model, id, datatypes):
        super(MSensor, self).__init__()
        self.protocol = protocol
        self.model = model
        self.id = id
        self.datatypes = datatypes

    def value(self, datatype):
        return MSensorValue(5, 1369347055)

    def has_temperature(self):
        return self.datatypes & TELLSTICK_TEMPERATURE != 0

    def has_humidity(self):
        return self.datatypes & TELLSTICK_HUMIDITY != 0

    def temperature(self):
        return self.value(TELLSTICK_TEMPERATURE)

    def humidity(self):
        return self.value(TELLSTICK_HUMIDITY)

class MSensorValue(object):
    __slots__ = ["value", "timestamp"]

    def __init__(self, value, timestamp):
        super(MSensorValue, self).__init__()
        self.value = value
        self.timestamp = timestamp
