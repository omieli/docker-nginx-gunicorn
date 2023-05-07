from flask import Flask, render_template, request, Response
import requests
import json
import datetime
import calendar

weather_app = Flask(__name__)
records_to_db = []
""" Route for handling the landing page of a weather app. This function handles both GET and POST requests to the "/" route. 
If the request is a POST request, the function returns the result of calling the `forecast_weekly` function. 
Otherwise, the function returns a rendered template for the base HTML page.
"""
@weather_app.route("/", methods = ['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        return forecast_weekly()
    return render_template("base.html")

def forecast_weekly():
    records = []
    cityCountry = request.form['cityCountry']
    response = get_data_from_api(cityCountry)
    #json.loads() create Dictionary from the JSON received
    jsonResponse = json.loads(response.text)

    #get a list with all values on weather from response in dictionary
    jsonRecords = jsonResponse['locations'][cityCountry]['values']



    #get a list with 2 items: location in native language and location in english
    jsonLocation = [jsonResponse['locations'][cityCountry]['address'],jsonResponse['locations'][cityCountry]['name']]

    records = filter_response(jsonRecords,records)
    return render_template("result.html",records_res=records, locations=jsonLocation)       

@weather_app.errorhandler(404)
def page_not_found(error):
    return render_template("404error.html"), 404
    
@weather_app.errorhandler(500) 
def internal_server_error(error):
    return render_template("500error.html"), 500

"""
This function takes in a list of responses (`responseList`) and a list to store the filtered and reformatted data (`returnedList`).
It iterates through each response in the `responseList`, extracts certain values from it, and reformats them.
The filtered and reformatted data are then appended to the `returnedList`.
Finally, the function returns the `returnedList`.
Args:
    A list of responses to be filtered and reformatted.
    A list to store the filtered and reformatted data.
Returns:
    The `returnedList` with the filtered and reformatted data appended to it.
"""
def filter_response(responseList, returnedList):
    for i in range(len(responseList)):
        responseList[i] = list(responseList[i].values())
        strDateTime = responseList[i][2]
        returnedList.append([edit_date(strDateTime),weekday_from_date(strDateTime[8:10],strDateTime[5:7],strDateTime[0:4]) ,edit_time(strDateTime),responseList[i][13],responseList[i][12],responseList[i][24]])
    return returnedList

"""
This function takes in the day, month, and year of a date, and returns the name of the weekday.
"""
def weekday_from_date(day, month, year):
    return calendar.day_name[
        datetime.date(day=int(day), month=int(month), year=int(year)).weekday()
    ]

def edit_date(date):
    return date[8:10]+"/"+date[5:7]+"/"+date[0:4]

def edit_time(time):
    return time[11:16]

"""
Retrieve weather data from a weather API.
This function sends a GET request to the specified weather API, passing in the specified location (`cc`) and other query parameters.
The function returns the response from the API.
Args:
    A location string to be used in the API request.
Returns:
    The response from the API.
"""
def get_data_from_api(cc):
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
    querystring = {"location":cc,"aggregateHours":"12","forecastDays": 7 ,"shortColumnNames": "False","unitGroup":"metric","contentType":"json"}
    headers = {"X-RapidAPI-Key": "46e3428294msh44260aa94808a6bp15e886jsnbb477465489f","X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"}
    return requests.request("GET", url, headers=headers, params=querystring)


        
if __name__ == '__main__':
    weather_app.run()
