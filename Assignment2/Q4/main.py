import requests

api_key = "********************" 

city = input("Enter city: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
weather = response.json()

print("status:", response.status_code)
print("API Response:", weather)

if response.status_code == 200:
    print("Temperature:", weather["main"]["temp"])
    print("Humidity:", weather["main"]["humidity"])
    print("Wind Speed:", weather["wind"]["speed"], "m/s")
    
    # Wind Direction (in degrees)
    if "deg" in weather["wind"]:
        print("Wind Direction:", weather["wind"]["deg"], "°")
    
    # Cloud Percentage
    if "clouds" in weather:
        print("Cloudiness:", weather["clouds"]["all"], "%")
    
else:
    print("Error:", weather.get("message", "Unknown error"))
