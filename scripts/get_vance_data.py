import requests
import json

FROM = "2024-10-31"
TO = "2024-10-31"

url = "https://newsapi.org/v2/everything?" + "q=\"jd%20vance\"&" + f"from={FROM}&"+ f"to={TO}&" + "sortBy=popularity&" + "language=en&" + "apiKey=09ca8c4ca1f44c9d80454f89143864ad&" + "searchIn=title,description"
response = requests.get(url)

# Check the status code
if response.status_code == 200:
    print("Request was successful!")
    with open(f'{FROM}_{TO}.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
