# -*- coding: utf-8 -*-
"""
Yelp API v2.0 code sample.

This program demonstrates the capability of the Yelp API version 2.0
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/documentation for the API documentation.

This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import re
import string

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'Pittsburgh, PA'
# SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# Future: save these as class variables in a different file and do a gitignore
CONSUMER_KEY = 'cLF0gnnGM5WTYppZxyXw9A'
CONSUMER_SECRET = 'E6cqb3ZZU3ernn7lWWR5CZkBnoM'
TOKEN = '8ay4eNyR7bdGG6rIqif-vgfNUEoauTeb'
TOKEN_SECRET = 'MDgY6EnC11tbBjbsff17r15kWGY'


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response



def search(term, location, offset):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
        offset (int): How many results to offset the search by (e.g. an offset of 20 will return results 21-40)

    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'offset': offset,
        'sort': 2 # Highest Rated
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location, offset):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location, offset)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        # If there are no remaining results, return an empty list
        return []

    responses = []
    # Return a list of businesses instead of just a single one
    for business in businesses:
        business_id = business['id']
        response = get_business(business_id)
        # sometimes results are from nearby cities, but not the city proper
        city = response['location']['city']
        state = response['location']['state_code']
        city_state = '%s, %s' % (city, state)
        # make passed location and returned location same case
        location, city_state = location.lower(), city_state.lower()
        # only include response if locations are the same
        if location == city_state:
            responses.append(response)

    return responses


def find_restaurants(term, location, offset):
    try:
        return query_api(term, location, offset)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

# This method writes the highest rated restaurants for a city to a JSON file.
def write_restaurants_to_json(city, state, term):
    city_state = '%s, %s' % (city, state)
    # set a default dict
    highest_rated = {city_state: []}
    # increment offset by 20
    for offset in range(0,100,20): # this will return a maximum of 100 (see query_api for reasons why it would return fewer)
        # find 20 restaurants
        restaurants = find_restaurants(term, city_state, offset)
        # add restaurants to highest_rated
        highest_rated[city_state] += restaurants
    # format highest_rated into human-readable JSON
    highest_rated = str(json.dumps(highest_rated, indent=2))
    # write JSON to file
    with open("highest_rated.json","w") as f:
        f.write(highest_rated)

def get_rating_and_review_count(): # right now this is just using a default file
    with open("highest_rated.json","r") as f:
        highest_rated = f.read()
    highest_rated = json.loads(highest_rated)
    # find out how many businesses were found
    print len(highest_rated.itervalues().next())
    # total rating * review_count
    total_weight = 0
    total_review_count = 0
    # since we don't know the city, state, iterate through businesses this way:
    for b in highest_rated.itervalues().next():
        review_count = b['review_count']
        rating = b['rating']
        weight = review_count * rating
        # add to totals
        total_weight += weight
        total_review_count += review_count

    adjusted_rating = total_weight / total_review_count
    return adjusted_rating, total_review_count

# Right now this isn't looping through the CSV file. When it does we will need to re-evaluate our data storage. It's probably worth changing it so that one JSON file is used
# per search term, instead of per state like it is now
write_restaurants_to_json('charleston','wv','cupcake')

adjusted_rating, total_review_count = get_rating_and_review_count()
print adjusted_rating, total_review_count



# UNICODE --> ASCII: .encode('ascii','ignore')