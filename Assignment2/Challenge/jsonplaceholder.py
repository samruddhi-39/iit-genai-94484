import requests
import json

def fetch_json_data():
    url = "https://jsonplaceholder.typicode.com/posts"

    print("Fetching data...")
    response = requests.get(url)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        # Print JSON data
        print("Data fetched successfully!")
        print(json.dumps(data, indent=4))

        # Save to a file
        with open("posts.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Saved: posts.json")

    else:
        print("Error:", response.text)

