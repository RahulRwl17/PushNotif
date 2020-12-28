from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from Locater.models import Hospital,AccidentReq,Login
from haversine import haversine,Unit
import reverse_geocode
import geocoder
import reverse_geocoder as rg
import requests
import json
from geopy.geocoders import Nominatim
from plyer import notification
from django.contrib import messages
from plyer import notification
from django.contrib import sessions
from webpush import send_group_notification
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
from django.conf import settings
# Methods of push notifications...
# plyer
# win10Tost

# Places API..
APIKEY = "AIzaSyBFx8hqftDOlrSWRTiOSowjwfeS1OQtBpw"

# View are here...

def Home(request):
    logdata = Login.objects.all()
    for user in logdata:
        if request.method == "POST":
            user_name = request.POST.get('uname')
            password = request.POST.get('password')
            if (user_name == user.user_name and password == user.password):
                uname = user.user_name
                Hdata = Hospital.objects.all()
                user_data = AccidentReq.objects.all()
                km = Calculate(user_data)
                tmp = sorted(km.items(),key = lambda kv:(kv[1], kv[0]))
                notification.notify(
                    title = "User Login",
                    message =f"{uname}, you got successfully Login...!",
                    app_icon = "",
                    timeout = 50
                    )
                    # time.sleep(5)
                request.session["Username"] = uname
                    # del request.session["Username"]
                return render(request,'Home.html',{"HDATA":Hdata,"Data":tmp})
                messages.success(request,"Your are Login..!")
            else:
                messages.success(request,"Login Denaide...!")
        return render(request,'login.html')


def Calculate(user_data):
    distances = {}
    pin = []
    i = 0
    for user in user_data:
        User_Loc = (float(user.Latitude),float(user.Longitude)) 
 
        # Fetching Zipcodes..
        geolocator = Nominatim(user_agent="Locater")
        location = geolocator.reverse(User_Loc)
        # print(location.raw)
        pincode = location.raw['address']['postcode']
        # print(location.raw)
        if pincode is not None:
            Hdata =  Hospital.objects.filter(zipcode=pincode)
        else:
            Hdata = Hospital.objects.all()
        
        for hp in Hdata:
            Hospital_Loc = (float(hp.Latitude),float(hp.Longitude))
            distances[hp.ID]=(haversine(User_Loc,Hospital_Loc))
                        
            
   
    return distances


def About(request):
    name = Login.objects.all()[0].user_name
    print(name)
    if request.session["Username"] == name:
        webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
        vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
        user = request.user
        print("hello",name)
        
    return render(request, 'Test.html', {user: user, 'vapid_key': vapid_key})


@require_POST
@csrf_exempt
def  send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
    
    

