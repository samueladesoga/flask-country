#!flask/bin/python
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

iso_codes = json.load(open('all.json'))

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/flask-country/api/v1.0/iso_codes', methods=['GET'])
def get_iso_codes():
    return jsonify({'iso_codes': iso_codes})

@app.route('/flask-country/api/v1.0/iso_code', methods=['POST'])
def get_iso_code():
	request_body = json.loads(request.data)
	country = request_body["country"]
	result = filter(lambda ic: ic['name'] == country, iso_codes)
	if (len(result) != 0):
		return jsonify(result[0]["alpha-2"])
	else:
		return not_found()

@app.route('/flask-country/api/v1.0/iso_code', methods=['GET'])
def query_iso_code():
	country = request.args.get("country")
	result = filter(lambda ic: ic['name'] == country, iso_codes)
	if (len(result) != 0):
		return jsonify(result[0]["alpha-2"])
	else:
		return not_found() 

if __name__ == '__main__':
    app.run(debug=True)
