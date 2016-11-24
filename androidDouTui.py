#coding=utf-8
try:
    import sl4a
except:
    import fakesl4a as sl4a 
import urllib.parse
import urllib.request
import time
import json

SERVER_ADDR = "http://45.32.56.30/"
#SERVER_ADDR = "http://127.0.0.1:5000/"
USER_NAME = "user1"
INTERVAL_SECONDS = 1
FAILED_SECONDS = 5

droid = sl4a.Android()
droid.startSensingTimed(1,500)
#droid.startLocating()

UPLOAD_TIME = 5
DOUTUI_ASUM = 18
DOUTUI_INTERVAL_SECONDS = 0.1
doutuiCount = 0
doutuiNewCount = 0
doutuLastTime = time.time()

def DouTui():
    global doutuLastTime, doutuiCount, doutuiNewCount
    doutuiCount += 1
    doutuiNewCount += 1
    print ("DouTui Count: %d (+1)" % doutuiCount)
    doutuLastTime = time.time()

def SendData(name, data):
    headers = {'Content-Type': 'application/json'}
    jdata = json.dumps(data)
    bdata = bytes(jdata, "utf8")
    req = urllib.request.Request(url = SERVER_ADDR + name, data = bdata)
    req.add_header('Content-Type', 'application/json')
    urllib.request.urlopen(req)


while 1:
    #gpsdata = droid.readLocation().result
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

    start_count_time = time.time()
    while (time.time() - start_count_time < UPLOAD_TIME):
        if time.time() - doutuLastTime > DOUTUI_INTERVAL_SECONDS:
            sensors = droid.readSensors().result
            asum = abs(sensors["xforce"]) + abs(sensors["yforce"]) + abs(sensors["zforce"])
            if asum > DOUTUI_ASUM:
                DouTui()


    for name in sensors_name:
        if name in sensors:
            #r = {"name":name, "value":sensors[name]}
            r = (name, sensors[name])
        sensors_data.append(r)

    sdata = {
            "timestamps":time.time(),
            "username": USER_NAME,
            "sensor":sensors_data
        }

    dtdata = {
            "timestamps":time.time(),
            "username": USER_NAME,
            "count": doutuiNewCount
            }

    doutuiNewCount = 0

    #try:
    SendData("dt_data_sensor", sdata)
    SendData("dt_data_entry", dtdata)
    print ("Success %d" % time.time())
    #time.sleep(INTERVAL_SECONDS)
    #except:
    #    print ("Sending Failed")
    #    time.sleep(FAILED_SECONDS)

#droid.stopLocating()
droid.stopSensing()
