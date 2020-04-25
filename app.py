from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from api import getAPIOutput
from api import getHeaderResponse

state_list = ['Andra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
              'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
              'Mizoram', 'Nagaland', 'Orissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telagana', 'Tripura', 'Uttaranchal',
              'Uttar Pradesh', 'West Bengal', 'Chandigarh', 'Delhi', 'Lakshadeep', 'Pondicherry', 'Andaman and Nicobar', 'Dadar and Nagar Haveli', 'Daman and Diu']

state_list = map(str.lower, state_list)
app = Flask(__name__)


@app.route('/')
@cross_origin()
def home():
    return 'Hi, How are you?'


@app.route('/covid', methods=['GET'])
@cross_origin()
def covid_data(state='Telangana'):
    print('Covid Data operation invoked')
    api_url = getAPIOutput.covidDataURL()
    resp = getHeaderResponse.response(api_url)
    return getAPIOutput.getCovidDataForState(resp, state)


@app.route('/zip/<pin_code>', methods=['GET'])
@cross_origin()
def findByPinCode(pin_code):
    # print('Given pin code : ', pin_code)
    api_url = getAPIOutput.stateByZipAPIURL(pin_code)
    resp = getHeaderResponse.response(api_url)
    errorMessage, state = getAPIOutput.getStateByZipCode(resp)
    # print('Pin code is ' + pin_code + '\t' + state)
    if state is None:
        return {"fulfillmentText": errorMessage}
    else:
        return covid_data(state)


@app.route('/city/<city_name>', methods=['GET'])
@cross_origin()
def findByCityName(city_name):
    # print('City Name : ', city_name)
    if city_name in state_list:
        state = city_name
    else:
        api_url = getAPIOutput.stateByCity(city_name)
        resp = getHeaderResponse.response(api_url)
        errorMessage, state = getAPIOutput.getStateByCity(resp)
    # print('City Name is : ' + city_name + '\tState : ' + state)
    if state is None:
        return errorMessage
    else:
        return covid_data(state)


@app.route('/covid', methods=['POST'])
@cross_origin()
def getCovidData():
    req = request.get_json(silent=True, force=True)
    intent_name = req['queryResult']['intent']['displayName']
    if intent_name == 'pin-code':
        pin_code = req['queryResult']['parameters']['zip_code']
        print('Given Pin Code is : ' + pin_code)
        return findByPinCode(pin_code)
    elif intent_name == 'state-info':
        city_name = req['queryResult']['parameters']['geo_city']
        print('Given city is : ' + city_name)
        return findByCityName(city_name)


if __name__ == '__main__':
    app.run(debug=True)
