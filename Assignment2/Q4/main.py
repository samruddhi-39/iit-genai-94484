import requests

city = input("Enter city: ")

API_KEY = "0be25e4af69121e8461244b2042c1010"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
print("status:", response.status_code)

weather = response.json()

if response.status_code == 200:
    print("Temperature:", weather["main"]["temp"])
    print("Humidity:", weather["main"]["humidity"])

    print("Wind:", weather["wind"]["speed"])
    print("Cloud:", weather["clouds"]["all"])
    print("Weather:", weather["weather"][0]["description"])
    
else:
    print("Error:", weather.get("message", "Something went wrong"))
