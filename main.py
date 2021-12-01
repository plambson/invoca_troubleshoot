import pandas as pd
import json
import validators
from requests.models import PreparedRequest
from bs4 import BeautifulSoup
from selenium import webdriver

# make distinct data frame
data = pd.read_json('revision140.json')
all_unique = data.drop_duplicates()
out = all_unique.to_json(orient='records')
out = json.loads(out)


def make_url(invoca_record):
    """function to create tracking url"""
    url = invoca_record['url']
    params = {'utm_campaign': invoca_record['utm_campaign'],
              'utm_source': invoca_record['utm_source'],
              'utm_medium': invoca_record['utm_medium']}
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url


# Loop through and add URL tracking
for count, value in enumerate(out):
    if validators.url(value['url']):
        out[count]['status'] = 'url valid'
        out[count]['tracking_link'] = make_url(value)
    else:
        out[count]['status'] = 'url invalid'

dr = webdriver.Chrome(executable_path='/Users/paul/PycharmProjects/invoca_troubleshoot/chromedriver')


def get_destination_numbers(out_dict):
    dr.get(out_dict['url'])
    bs = BeautifulSoup(dr.page_source, "html.parser")
    phone_numbers = bs.find_all(text=out_dict['destination'])
    divs = [number.parent for number in phone_numbers]
    out_dict['orig_attrs'] = divs
    dr.get(out_dict['tracking_link'])
    bs = BeautifulSoup(dr.page_source, "html.parser")
    for count, value in enumerate(out_dict['orig_attrs']):
        out_dict['orig_attrs'][count]['swapped_numbers'] = bs.find_all(attrs=value.attrs)
    return out_dict


test = get_destination_numbers(out[0])
