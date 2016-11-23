#coding=utf-8

class Sensor:
    sensors_name = ["light", "pitch", "roll", "azimuth", "xMag", "yMag", "zMag", "xforce", "yforce", "zforce", "accuracy"]
    @property
    def result(self):
        res = {}
        for name in Sensor.sensors_name:
            res[name] = 0.0
        return res

class Android:
    Android = 0
    def startSensingTimed(self, a, b):
        print ("START FAKE SL4A")
    def stopSensing(self):
        print ("STOP FAKE SL4A")
    def readSensors(self):
        return Sensor()
