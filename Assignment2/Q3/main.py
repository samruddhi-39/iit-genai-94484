import requests

def fetch_and_save_json():
    try:
        url = "https://jsonplaceholder.typicode.com/posts"

        response = requests.get(url)
        print("status code:", response.status_code)

        print("response text:\n", response.text)

        data = response.json()
        print("resp data:\n", data)

        # Save to file
        with open("posts.json", "w") as f:
            import json
            json.dump(data, f, indent=4)

        print("posts.json saved successfully!")

    except Exception as e:
        print("Some error occurred:", e)
