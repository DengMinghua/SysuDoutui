from flask import Flask, request, jsonify, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/dt_data_entry', methods = ['POST'])
def postInfo():
    client = MongoClient()
    db = client['doutuiDb']
    jsonInfo = request.json
    # print (jsonInfo)
    doutuiCol = db.doutuiCol
    doutuiCol.insert_one({"timestamps":jsonInfo['timestamps'],
                         "username":jsonInfo["username"],
                         "count":jsonInfo['count']})
    return "Successed"

@app.route('/dt_data_sensor', methods = ['POST'])
def postSensorInfo():
    client = MongoClient()
    db = client['doutuiDb']
    jsonInfo = request.json
    doutuiColSensorCol = db.doutuiSensorCol
    doutuiColSensorCol.insert_one({"timestamps":jsonInfo['timestamps'],
                         "username":jsonInfo["username"],
                         "sensor":jsonInfo['sensor']})
    return "Successed"

@app.route('/get_dt_data', methods=['GET'])
def getInfo():
    client = MongoClient()
    db = client['doutuiDb']
    limits = int(request.args.get('timeLimits'))
    interval = int(request.args.get('timeInterval'))
    # print(limits, interval)
    startTime = limits - interval
    endTime = limits
    doutuiCol = db.doutuiCol
    cnt = 0
    doutuiColSensorCol = db.doutuiSensorCol
    for item in doutuiCol.find({'timestamps':{'$gt':startTime, '$lte':endTime}}):
        cnt = cnt + item['count']
    return str(cnt)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False, port = 80, host = '45.32.56.30')
