import requests
import json
from .models import CarDealer, DealerReview
from .local_settings import *
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

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

def post_request(url, json_payload, **kwargs):
    json_obj = json_payload["review"]
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=json_obj, params=kwargs)
    except:
        print("Network exception occurred")
    
    json_data = json.loads(response.text)
    print(json_data)

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        if 'entries' in json_result:
            dealers = json_result['entries']
            results = [CarDealer(id=dealer['id'], 
                full_name=dealer['full_name'], short_name=dealer['short_name'],
                city=dealer['city'], address=dealer['address'], st=dealer['st'],
                zip=dealer['zip'], lat=dealer['lat'], long=dealer['long']
                ) for dealer in dealers]
    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        if 'entries' in json_result:
            reviews = json_result['entries']
            results = [DealerReview(id=review['id'], 
                car_make=(review['car_make'] if 'car_make' in review else None),
                car_model=(review['car_model'] if 'car_model' in review else None),
                car_year=(review['car_year'] if 'car_year' in review else None),
                dealership=review['dealership'], name=review['name'],
                purchase=(review['purchase'] if 'purchase' in review else None),
                purchase_date=(review['purchase_date'] if 'purchase_date' in review else None),
                review=review['review'], sentiment=analyze_review_sentiments(review['review'])
                ) for review in reviews]
    return results


def analyze_review_sentiments(review):
    api_key = NLU_API_KEY
    url = NLU_URL
    text = review
    version = '2020-08-01'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=version,
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features= Features(sentiment= SentimentOptions())
    ).get_result()
    sentiment_label = response["sentiment"]["document"]["label"]
    sentimentresult = sentiment_label
    
    return sentimentresult

def send_review_to_cf(url, json_payload):
    return post_request(url, json_payload)