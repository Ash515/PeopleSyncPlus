from flask import Flask, render_template, request

# import json to load JSON data to a python dictionary
import json

# urllib.request to make a request to api
import urllib.request


app = Flask(__name__)

@app.route('/weatherreport', methods =['POST', 'GET'])
def weather():
	if request.method == 'POST':
		city = request.form['city']
	else:
		# for default name mathura
		city = 'mathura'

	# your API key will come here
	api = "0f671a46ce00201b5cfa17ff2e13cbb9"
	# source contain json data from api
	source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q =' + city + '&appid =' + api).read()

	# converting JSON data to a dictionary
	list_of_data = json.loads(source)

	# data for variable list_of_data
	data = {
		"country_code": str(list_of_data['sys']['country']),
		"coordinate": str(list_of_data['coord']['lon']) + ' '
					+ str(list_of_data['coord']['lat']),
		"temp": str(list_of_data['main']['temp']) + 'k',
		"pressure": str(list_of_data['main']['pressure']),
		"humidity": str(list_of_data['main']['humidity']),
	}
	print(data)
	return render_template('index.html', data = data)



if __name__ == '__main__':
	app.run(debug = True)
