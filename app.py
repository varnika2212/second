from datetime import datetime,timedelta
import time
from datetime import timezone
from flask import Flask,request, render_template
from helper import validate
from flask import jsonify
import json

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return render_template('index_two.html')

def tts(x):
    x = x % (24 * 3600)
    hrs = x // 3600
    mins = (x % 3600) // 60
    seconds = (x % 60)
    return "%dh:%02dm:%02ds" %(hrs, mins, seconds)

@app.route('/result_two',methods=['POST', 'GET'])
def result():
    if request.method=='POST':
        start_time=request.form.get('st')
        end_time=request.form.get('et')
        counter=0
        runtime=0
        downtime=0
        utilisation=0
        if(validate(start_time) and validate(end_time)):
            start=datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
            end=datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
            with open('json_2.json') as f:
                J = json.load(f)
                L = []

                for item in J:
                    r=int(item['runtime'])
                    d=int(item['downtime'])
                    t=datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
                    t=t.replace(tzinfo=timezone.utc)
                    L.append((t, min(r,1021), max(d, d + r - 1021)))

                for item in L:
                    t = item[0]
                    r = item[1]
                    d = item[2]
                    if t>=start and t<=end:
                        nt=t.time()
                        runtime += r
                        downtime += d
        utilisation= (runtime)/((runtime + downtime)) * 100
        ut = "%.2f" %(utilisation)
        utt = float(ut)
        dic={
                'runtime':tts(runtime),
                'downtime':tts(downtime),
                'utilisation':utt
            }
        # jo = json.dumps(dic)


    return jsonify(dic)
