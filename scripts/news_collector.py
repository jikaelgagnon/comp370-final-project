import os
import requests
from datetime import datetime, timedelta
from argparse import ArgumentParser
import json


BASE_URL = 'https://newsapi.org/v2/everything?'

def keyword_list_to_query(news_keywords):
    return " OR ".join(news_keywords)

def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    end_date = datetime.today()
    lookback_days = timedelta(days=lookback_days)
    start_date = end_date - lookback_days
    keywords = keyword_list_to_query(news_keywords)
    query = {'apiKey': api_key,
             'q': keywords, 
             'from': start_date.strftime('%Y-%m-%d'), 
             'to': end_date.strftime('%Y-%m-%d'),
             'language':'fr',
             'sort_by': 'popularity',
             'searchIn':'title,description'}
    response = requests.get(BASE_URL, params=query)
    response.raise_for_status() # returns error code if failed
    data = response.json() # parse data as JSON

    return data['articles'] # dictionary of JSON

def main():
    parser = ArgumentParser()
    parser.add_argument('-k', help='NewsAPI API key', type=str)
    parser.add_argument('-b', help='Number of days to look back', type=int)
    parser.add_argument('-i', help='Input JSON file containing a dictionary of named keyword lists.\n\
    Eg. { “trump_fiasco”: [“trump”, “trial”], “swift”: [“taylor”, “swift”, “movie”]}', type=str)
    parser.add_argument('-o', help='Output directory. Each query is saved to <output_dir>/<query>.json', type=str)

    args = parser.parse_args()

    API_KEY = args.k
    lookback_days = args.b
    keyword_dict = json.load(open(args.i, 'r'))
    output_dir = args.o

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for fname, keywords in keyword_dict.items():
        save_path = os.path.join(output_dir, f'{fname}.json')
        results = fetch_latest_news(api_key=API_KEY, news_keywords=keywords, lookback_days=lookback_days)
        json_str = json.dumps(results)
        f = open(save_path, "w+")
        f.write(json_str)
        f.close()

if __name__ == "__main__":
    main()