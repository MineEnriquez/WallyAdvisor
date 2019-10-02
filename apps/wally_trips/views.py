from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import View
import requests, json
from .models import Trips
from ..wally_trips.models import User, Colors
from django.utils.dateparse import parse_date

# Create your views here.


def wally_index(request):
    if request.method == "GET":
        return render(request, "wally_trips/index.html")


def trip_weather(request, trip_id):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    trip = Trips.objects.get(id=trip_id)
    querystring = {"q": trip.destination}
    headers = {
        "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
        "x-rapidapi-key": "16183f2d8dmshfc400b5f552be7ap142362jsnc31c7e278a45",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = response.json()
    for i in response_json:
        print(i)
    weather_info = response_json["weather"]
    name = response_json["name"]
    lon = response_json["coord"]['lon']
    lat = response_json["coord"]['lat']
    clouds = response_json["coord"]['lat']
    print(lat)

    # url = "https://jgentes-crime-data-v1.p.rapidapi.com/crime"
    # # querystring = {"startdate":"1/10/2015","enddate":"12/25/2015","lat":lat,"long": lon}
    # querystring = {"startdate":"9/19/2015","enddate":"9/25/2015","lat":"37.757815","long":"-122.5076392"}
    # headers = {
    #     'x-rapidapi-host': "jgentes-Crime-Data-v1.p.rapidapi.com",
    #     'x-rapidapi-key': "16183f2d8dmshfc400b5f552be7ap142362jsnc31c7e278a45"
    #     }
    # response = requests.request("GET", url, headers=headers, params=querystring)
    url = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=sgSAjHJcEpLl2mam3n8bRdYUE1YJskapjbUw51Mt&location=Denver+CO"
    response = requests.request("GET", url)
    print(response.json())

    # Update dashboard
    print("Dashboard - viewing trips:----")
    if "user_id" in request.session:
        all_user_trips = Trips.objects.filter(
            user_id_id=request.session["user_id"]
        ).order_by("-id")
    else:
        return redirect("/")
    context = {
        "all_user_trips": all_user_trips,
        "cityname": name,
        "w": weather_info[0],
        "lat": lat,
        "lon": lon,
        "clouds" : clouds,
    }
    return render(request, "wally_trips/index.html", context)


def trip_create(request):
    if request.method == "GET":
        return redirect("/trips/new")
    if request.method == "POST":
        # Pass the post data to the mehod we wrote and save the response in a variable called errors
        errors = Trips.objects.basic_validator(request.POST)

        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            user = User.objects.get(id=request.session["user_id"])
            new_trip = Trips.objects.create(
                destination=request.POST["destination"],
                start_date=request.POST["start_date"],
                end_date=parse_date(request.POST["end_date"]),
                plan=request.POST["plan"],
                user_id=user,
            )
            print("-----------------")
            print(new_trip.destination)
            # newtrip = "/trips/" + str(new_trip.id)
            return redirect("/dashboard")


def trip_create_render(request):
    return render(request, "wally_trips/create.html")


def dashboard_render(request):
    print("Dashboard - viewing trips:----")
    if "user_id" in request.session:
        all_user_trips = Trips.objects.filter(
            user_id_id=request.session["user_id"]
        ).order_by("-id")
        all_other_trips = Trips.objects.exclude(user_id_id=request.session["user_id"])
    else:
        return redirect("/")

    context = {"all_user_trips": all_user_trips, "all_other_trips": all_other_trips}
    return render(request, "wally_trips/index.html", context)


def view_trip(request):
    pass


def trip_edit(request, trip_id):
    trip = Trips.objects.get(id=trip_id)
    print(trip.destination)
    context = {
        "trip_info": trip,
        "start_date": trip.start_date.strftime("%Y-%m-%d"),
        "end_date": trip.end_date.strftime("%Y-%m-%d")
    }
    return render(request, "wally_trips/Update.html", context)


def trip_update(request, trip_id):
    if request.method == "POST":
        # Pass the post data to the mehod we wrote and save the response in a variable called errors
        errors = Trips.objects.basic_validator(request.POST)

        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            trip = Trips.objects.get(id=trip_id)

            trip.destination = request.POST['destination']
            trip.start_date = parse_date(request.POST['start_date'])
            trip.end_date = parse_date(request.POST['end_date'])
            trip.plan = request.POST['plan']
            trip.save()

            print("-----------------")
            print(trip.destination)
            # newtrip = "/trips/" + str(new_trip.id)
            return redirect("/dashboard")
    pass


def trip_remove(request, trip_id):
    rem = Trips.objects.get(id=trip_id)
    print(f"deleting a record {str(trip_id)}")
    rem.delete()
    return redirect("/dashboard")

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wally_trips/charts.html', {})

def crime(request, trip_id):
    pass
    # url = "https://jgentes-crime-data-v1.p.rapidapi.com/crime"
    # querystring = {"startdate":"9/19/2015","enddate":"9/25/2015","lat":"37.757815","long":"-122.5076392"}
    # headers = {
    #     'x-rapidapi-host': "jgentes-Crime-Data-v1.p.rapidapi.com",
    #     'x-rapidapi-key': "16183f2d8dmshfc400b5f552be7ap142362jsnc31c7e278a45"
    #     }
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    # return redirect("/dashboard")

def get_crimedata(request):
    querystring = {"location": "Sammamish+WA", "crime" : "robbery"}
    # url = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?api_key=sgSAjHJcEpLl2mam3n8bRdYUE1YJskapjbUw51Mt&location=Denver+CO"
    url = "https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?"
    headers = {
            "User-Agent": f"ChangeMeClient/0.1 by YOUR_USERNAME_ON_REDDIT",
            "X-Api-Key": "sgSAjHJcEpLl2mam3n8bRdYUE1YJskapjbUw51Mt"
        }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    # print(response.json())
    print('-------------------')
    data = response.json()
    for x in data:
        print('----------------------------------')
        print(x)
    print(data['total_results'])
    print(data)
    return JsonResponse(response.json())

def get_data(request):
    
    all_info = Colors.objects.all().values()
    cities = []
    colors = []
    incidents = []
    borders = []
    for i in all_info:
        cities.append(i['city'])
        colors.append(i['color'])
        incidents.append(i['incidents'])
        borders.append(i['border'])
        
    response = {
        "city" : cities,
        "colors" : colors,
        "incidents" : incidents,
        "borders" : borders,
    }
    return JsonResponse(response)