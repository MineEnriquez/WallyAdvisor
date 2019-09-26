from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import requests, json
from .models import Trips
from ..login_and_reg_app.models import User
from django.utils.dateparse import parse_date

# Create your views here.


def wally_index(request):
    if request.method == "GET":
        return render(request, "wally_trips/index.html")


def read_weather(request):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    # querystring = {"callback":"test","id":"2172797","units":"\"metric\" or \"imperial\"","mode":"xml, html","q":"London,uk"}
    querystring = {"q": "London,uk"}
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
    context = {"cityname": name, "w": weather_info[0]}
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

def trash(request):
    print(" ")
# def read_weather(request):
#     cities = ["London,uk", "Porto,pt", "Paris,fr"]
#     weather_dict = {}
#     for city in cities:
#         response = requests.get(
#           "https://community-open-weather-map.p.rapidapi.com/forecast?q="+city,
#           headers={
#           "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
#           "X-RapidAPI-Key": "16183f2d8dmshfc400b5f552be7ap142362jsnc31c7e278a45"
#             },)
#         weather_dict[city] = response.json()
#     d = weather_dict['Paris,fr']

#     # for e in d:
#     #     print (e)
#     # cod
#     # message
#     # cnt
#     # list
#     # city
#     print(d['city']['name'])
#     print(d['list'])
#     context = {
#         'cityname': "dfasdf",
#         "w": weather_dict['London,uk']
#     }
#     return render(request, "wally_trips/index.html", context)


# print(weather_info)
# print(weather_info[0]['description'])
# print(response_json['visibility'])
# print(response_json['clouds'])
    pass
