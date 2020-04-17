from urllib.parse import quote
errorMessage = 'Sorry! We didn\'t find any record with this input. Please try with other criteria. Thank you.'


def spaceRemoveFromParam(param):
    return quote(param)


def stateByZipAPIURL(zip_code):
    api_url = api_url = f'https://api.postalpincode.in/pincode/{spaceRemoveFromParam(zip_code)}'
    return api_url


def stateByCity(city_name):
    # api_url = f'https://api.postalpincode.in/postoffice/{spaceRemoveFromParam(city_name)}'
    api_url = f'https://api.postalpincode.in/postoffice/{city_name}'
    return api_url


def covidDataURL():
    api_url = 'https://api.covid19india.org/data.json'
    return api_url


def getStateByZipCode(json):
    data = json[0]
    # print(data)
    if data['Status']!= 'Success':
        return errorMessage, None
    else:
        postoffice = data['PostOffice'][0]
        # print('postoffice : ', postoffice)
        state = postoffice['State']
        print('State : ', state)
        return None, state


def getStateByCity(json):
    data = json[0]
    # print(data)
    if data['Status'] != 'Success':
        return errorMessage, None
    else:
        postoffice = data['PostOffice'][0]
        # print('PostOffice : ', postoffice)
        state = postoffice['State']
        print('State : ', state)
        return None, state


def getCovidDataForState(json, state_name):
    statewise_data = json['statewise']
    if state_name is not None:
        state_record = [state for state in statewise_data if (state['state']).upper() == state_name.upper()][0]
        string = 'State : \t' + state_name + '\nTotal Case : \t' + str(
            state_record['confirmed']) + '\nActive Case : \t' + str(state_record['active']) + \
                 '\nDeath : \t' + str(state_record['deaths']) + '\nRecovered : \t' + str(state_record['recovered'])
        print(string)
        return string
