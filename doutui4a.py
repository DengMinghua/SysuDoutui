#coding=utf-8
import sl4a
import urllib.parse
import urllib.request
import time

SERVER_ADDR = "http://127.0.0.1:5000/"
USER_NAME = "user1"
INTERVAL_SECONDS = 1
FAILED_SECONDS = 5

droid = sl4a.Android()
droid.startSensingTimed(1,500)
#droid.startLocating()

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
            r = {"name":name, "value":sensors[name]}
        sensors_data.append(r)


    sdata = {
            "timestamps":time.time(),
            "username": USER_NAME,
            "sensor":sensors_data
        }

    try:
        postdata = urllib.parse.urlencode(sdata).encode('utf-8')
        urllib.request.urlopen(SERVER_ADDR, postdata)
        time.sleep(INTERVAL_SECONDS)
    except:
        print ("Sending Failed")
        time.sleep(FAILED_SECONDS)

#droid.stopLocating()
droid.stopSensing()
