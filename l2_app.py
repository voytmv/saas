#History weather API method returns historical weather for a date on 
#or after 1st Jan, 2010 (depending upon subscription level) as json.

import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

# create your API token, and set it up in Postman collection as part of the Body section
API_TOKEN = ""
# you can get API keys for free here - https://api-docs.pgamerx.com/


app = Flask(__name__)


def generate_weather(location: str,date: str):
    url = "https://weatherapi-com.p.rapidapi.com/history.json"
   
    params = {"q": location, "dt": date}
    
    headers = {
	"X-RapidAPI-Key": "0c3db47b54msh87bc3a7395ab524p1136eejsn1b1a0ae28ba3",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}


    response = requests.request("GET", url, headers=headers, params=params)
    return json.loads(response.text)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA L2: Python Saas.</h2></p>"


@app.route(
    "/content/api/v1/integration/generate",
    methods=["POST"],
)
def weather_endpoint():
    start_dt = dt.datetime.now()
    json_data = request.get_json()

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    location = ""
    if json_data.get("location"):
        location = json_data.get("location")
    
    date = ""
    if json_data.get("date"):
        date = json_data.get("date")
     
    
    weather = generate_weather(location,date)
    current_time = dt.datetime.utcnow()
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    result = {
        "reques_name": "Voitishyn Mykyta",
        "timestamp": formatted_time,
        "location": location,
        "date": date,
        "weather": weather
    }

    return result
