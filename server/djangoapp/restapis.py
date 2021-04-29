import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    try:
        api_key = None
        if 'api_key' in kwargs:
            params = {
                'text': kwargs['text'],
                'version': '2021-03-25',
                'features': 'sentiment',
                'return_analyzed_text': True
            }
            api_key = kwargs['api_key']
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        if 'entries' in json_result:
            dealers = json_result['entries']
            results = [CarDealer(id=dealer['id'], full_name=dealer['full_name'], short_name=dealer['short_name'], city=dealer['city'], address=dealer['address'], st=dealer['st'], zip=dealer['zip'], lat=dealer['lat'], long=dealer['long']) for dealer in dealers]
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



