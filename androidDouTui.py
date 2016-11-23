#coding=utf-8
try:
    import sl4a
except:
    import fakesl4a as sl4a 
import urllib.parse
import urllib.request
import requests
import time
import json

#SERVER_ADDR = "http://45.32.56.30:5000/"
SERVER_ADDR = "http://127.0.0.1:5000/"
USER_NAME = "user1"
INTERVAL_SECONDS = 1
FAILED_SECONDS = 5

droid = sl4a.Android()
droid.startSensingTimed(1,500)
#droid.startLocating()

DOUTUI_ASUM = 18
DOUTUI_INTERVAL_SECONDS = 0.1
doutuiCount = 0
doutuLastTime = time.time()

def DouTui():
    global doutuLastTime, doutuiCount
    doutuiCount += 1
    print ("DouTui Count: %d (+1)" % doutuiCount)
    doutuLastTime = time.time()

def SendData(name, data):
    headers = {'Content-Type': 'application/json'}
    jdata = json.dumps(data)
    bdata = bytes(jdata, "utf8")
    '''
    req = urllib.request.Request(url = SERVER_ADDR + name, data = bdata)
    req.add_header('Content-Type', 'application/json')
    urllib.request.Rpost(req)
    '''
    url = SERVER_ADDR + name
    requests.post(url, data = bdata, headers = headers)


while 1:
    #gpsdata = droid.readLocation().result
    sensors = droid.readSensors().result
    '''
        sensors中的key解释:
        时间:
            time
        亮度:
            light
        陀螺仪:
            pitch, roll, azimuth
        磁力计:
            xMag, yMag, zMag
        加速度:
            xforce, yforce, zforce
        精度:
            accuracy
    '''

    sensors_data = [] 
    sensors_name = ["light", "pitch", "roll", "azimuth", "xMag", "yMag", "zMag", "xforce", "yforce", "zforce", "accuracy"]
    for name in sensors_name:
        if name in sensors:
            #r = {"name":name, "value":sensors[name]}
            r = (name, sensors[name])
        sensors_data.append(r)

    if time.time() - doutuLastTime > DOUTUI_INTERVAL_SECONDS:
        asum = sensors["xforce"] + sensors["yforce"] + sensors["zforce"]
        if asum > DOUTUI_ASUM:
            DouTui()


    sdata = {
            "timestamps":time.time(),
            "username": USER_NAME,
            "sensor":sensors_data
        }
    dtdata = {
            "timestamps":time.time(),
            "username": USER_NAME,
            "count": doutuiCount
            }

    #try:
    SendData("dt_data_sensor", sdata)
    SendData("dt_data_entry", dtdata)
    print ("Success %d" % time.time())
    time.sleep(INTERVAL_SECONDS)
    #except:
    #    print ("Sending Failed")
    #    time.sleep(FAILED_SECONDS)

#droid.stopLocating()
droid.stopSensing()
