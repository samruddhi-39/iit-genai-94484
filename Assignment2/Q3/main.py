import requests

try:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    print("status code:", response.status_code)
    print("response text:", response.text)

    # Convert response to JSON
    data = response.json()
    print("resp data:", data)

except Exception as e:
    print("Some error occurred:", e)
