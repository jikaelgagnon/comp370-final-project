import requests
import json

url = "https://political-bias-database.p.rapidapi.com/MBFCdata"

headers = {
	"x-rapidapi-key": "c6ce10f28bmsh47220349b18f48cp1750a0jsn3f5aee38092b",
	"x-rapidapi-host": "political-bias-database.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

with open('api_response.json', 'w') as f:
    json.dump(f, response.json())
