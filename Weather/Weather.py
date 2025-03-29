
from flask import Flask
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)



@app.route("/")
def home():
  city = "Bangalore"
  api_key = "0f671a46ce00201b5cfa17ff2e13cbb9"

  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
  session = requests.Session()
  retry = Retry(connect=3, backoff_factor=0.5)
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('http://', adapter)
  session.mount('https://', adapter)
  #session.get(url)
  response = session.get(url)

  if response.status_code == 200:
    data = response.json()
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
  else:
    weather = "Unknown"
    temperature = "0"

  return f"The weather in {city} is {weather}. The temperature is {temperature} degrees Celsius."

if __name__ == "__main__":
  app.run(debug=True)