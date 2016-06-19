from flask import Flask, render_template
from flask_restful import Resource, Api
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery

app = Flask(__name__)
api = Api(app)

@app.route("/freakybrew")
def freakybrew():
    bucket = Bucket('couchbase://46.101.11.33:8091/devices')
    temperature = bucket.get(1, quiet=True)
    return render_template('freakybrew.html', temperature = str(temperature))

class _temp(Resource):
    def get(self,device_id):
        bucket = Bucket('couchbase://46.101.11.33:8091/devices')
        res = bucket.get(device_id, quiet=True)
        if res.success:
            return res.value
        else:
            return {"errCode": "-1", "errMsg": "Could not find device %s" % device_id}
class _device(Resource):
    def get(self,info):
        device_id, temp, type, status = info.split(':')
        bucket = Bucket('couchbase://46.101.11.33:8091/devices')
        res = bucket.get(device_id, quiet=True)
        if res.success:
            bucket.n1ql_query('UPSERT INTO devices (KEY,VALUE) VALUES ("%s",{"device_id":"%s", "temp":"%s", "type":"%s", "status":"%s"})' % (device_id, device_id, temp, type, status)).execute()
            res = bucket.get(device_id, quiet=True)
            return res.value
        else:
            return {"errCode": "-1", "errMsg": "Could not find device %s" % device_id}

api.add_resource(_temp, '/freakybrew/_temp/<string:device_id>')
api.add_resource(_device, '/freakybrew/_device/<string:info>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')