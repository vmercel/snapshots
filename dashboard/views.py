from django.shortcuts import render
from .models import Data
import folium
from folium import plugins, raster_layers
from django_pandas.io import read_frame
# Create your views here.
#newwwww
from django.contrib.auth.decorators import login_required
from accounts.models import User
from accounts.decorators import student_only, lecturer_only
from django.http import HttpResponse
from .models import Data, Covid
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, F
from django.core.mail import send_mail
##########
import urllib.request
#################

@login_required
def index(request):
    m = folium.Map(location=[35, 33], zoom_start=8)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
    folium.LayerControl().add_to(m)
    qs = Data.objects.none()
    df = read_frame(qs, fieldnames=['country',
                                    'latitude', 'longitude', 'user'])
    # print(df)
    for (index, rows) in df.iterrows():
        folium.Marker(location=[rows.loc['latitude'],
                                rows.loc['longitude']], popup=rows.loc['user'], tooltip='<strong>Click to see</strong>').add_to(m)

    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        'm': m
    }
    return render(request, 'dashboard/index.html', context)


#################SEG START################
from branca.element import Figure




@login_required
@student_only
# def index50(request):
#     if request.is_ajax():
#         if request.method == 'POST':
#             print('Raw Data: "%s"' % request.body)
#     return HttpResponse("OK")


@login_required
def index50(request):
    if request.method == 'POST':
        latitude = request.POST['latitude']
        print(latitude)
        longitude = request.POST['longitude']
        print(longitude)
        Data.objects.create(
            user=request.user, latitude = latitude, longitude = longitude
        )

        # def index50(request, x, y):
    # Data.objects.create(
    #     country='xyz',
    #     latitude=x,
    #     longitude=y,
    #     user=request.user,
    # )
    # print(x)
    # print(x)
    # print(y)
    # print(y)
    return HttpResponseRedirect(reverse('covid_image_uploadstudent'))


@login_required
def index8(request):
    context = {
    }
    return render(request, 'dashboard/mylocation9.html', context)

# @login_required
def team(request):
    context = {
    }
    return render(request, 'dashboard/team.html', context)



# from django.contrib.auth import get_user_model
# User = get_user_model()

from accounts.models import User

@login_required
@lecturer_only
def all_users_table(request):
    title = 'List of all Users'
    # new
    # queryset = User.objects.all().order_by('-id')
    queryset = User.objects.all().exclude(is_superuser=True)
    context = {
        "title": title,
        "queryset": queryset,
    }

    return render(request, 'dashboard/users.html', context)

import csv
from django.db.models import Q
from .forms import LocationSearchForm

@login_required
@lecturer_only
def location_log_table(request):
    title = 'List of all Users'
    # new
    form = LocationSearchForm(request.POST or None)
    queryset = Covid.objects.all().select_related('data')
    # queryset = Covid.objects.select_related('data').all()
    context = {
        "title": title,
        "form": form,
        "queryset": queryset,
    }
    #not implemented
    if request.method == 'POST':
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        Data.objects.filter(Q(longitude__icontains=longitude) | Q(latitude__icontains=latitude))
        # queryset = Data.objects.filter(latitude__icontains=latitude)
        # if (longitude != ''):
        #     queryset = queryset.filter(longitude__icontains=longitude)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="User Locations.csv"'
            writer = csv.writer(response)
            writer.writerow(['USER', 'LONGITUDE', 'LATITUDE'])
            instance = queryset
            for x in instance:
                writer.writerow([x.user.username, x.longitude, x.latitude])
            return response

        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }

    return render(request, 'dashboard/table.html', context)

@login_required
@lecturer_only
def individual_table(request, pk):
    title = 'List of all Users'
    # new
    queryset = Data.objects.filter(user_id=pk)
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, 'dashboard/peruser.html', context)


@login_required
@lecturer_only
def per_user_map1(request, pk):
    title = 'Each users location'
    # new
    m = folium.Map(location=[35, 33], zoom_start=8)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
    folium.LayerControl().add_to(m)
    #new end
    qs = Data.objects.filter(user_id=pk)
    df = read_frame(qs, fieldnames=['country',
                                    'latitude', 'longitude', 'user'])
    # print(df)
    for (index, rows) in df.iterrows():
        folium.Marker(location=[rows.loc['latitude'],
                                rows.loc['longitude']], popup=rows.loc['user'],
                      tooltip='<strong>Click here to see</strong>').add_to(m)

    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        "title": title,
        "m": m,
    }
    return render(request, 'dashboard/index.html', context)

from django.db.models import Max

@login_required
@lecturer_only
def last_location(request):
    title = 'List of last location of all Users'
    # new filter by group of users
    #finally it worked
    queryset = Data.objects.all()
    latest_dates = queryset.values('user').annotate(latest_created_at=Max('created'))
    queryset = queryset.filter(created__in=latest_dates.values('latest_created_at')).order_by('-created')
    print (queryset)
    #for-Posgres database alone
    # queryset = Data.objects.all().order_by('user', '-created').distinct('user')
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, 'dashboard/table1.html', context)




@login_required
@lecturer_only
def per_user_map(request):
    m = folium.Map(location=[35, 30], zoom_start=2)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
    folium.LayerControl().add_to(m)
    qs = Data.objects.all()
    df = read_frame(qs, fieldnames=['country',
                                    'latitude', 'longitude', 'user'])
    # print(df)
    for (index, rows) in df.iterrows():
        folium.Marker(location=[rows.loc['latitude'],
                                rows.loc['longitude']], popup=rows.loc['user'], tooltip='<strong>Click here to see</strong>').add_to(m)

    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        'm': m
    }
    return render(request, 'dashboard/index.html', context)



# unusedddddddd
@login_required
@lecturer_only
def last_location_all_user_map(request):
    m = folium.Map(location=[35, 30], zoom_start=2)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
    folium.LayerControl().add_to(m)
    qs = Data.objects.all()
    df = read_frame(qs, fieldnames=['country',
                                    'latitude', 'longitude', 'user'])
    # print(df)
    for (index, rows) in df.iterrows():
        folium.Marker(location=[rows.loc['latitude'],
                                rows.loc['longitude']], popup=rows.loc['user'], tooltip='<strong>Click here to see</strong>').add_to(m)

    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        'm': m
    }
    return render(request, 'dashboard/index.html', context)







@login_required
@lecturer_only
def last_location_map(request):
    m = folium.Map(location=[35, 30], zoom_start=2)

    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
    folium.LayerControl().add_to(m)

    qs = Data.objects.filter(statusn=True)
    latest_dates = qs.values('user').annotate(latest_created_at=Max('created'))
    qs = qs.filter(created__in=latest_dates.values('latest_created_at')).order_by('-created')

    df = read_frame(qs, fieldnames=['country',
                                    'latitude', 'longitude', 'user'])
    # print(df)
    for (index, rows) in df.iterrows():
        folium.Marker(location=[rows.loc['latitude'],
                                rows.loc['longitude']], popup=rows.loc['user'], tooltip='<strong>Click here to see</strong>').add_to(m)

    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        'm': m
    }
    return render(request, 'dashboard/index.html', context)



#.filter(Q(appointment_with__username__icontains=q)| Q(date__icontains=q)).distinct()


@login_required
@lecturer_only
def Search(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Data.objects.filter(Q(longitude__icontains=query)| Q(latitude__icontains=query)| Q(user__username__icontains=query))#.distinct()

    context = {'string': query,
               'results': results}

    return render(request, 'dashboard/search.html', context)

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageForm



##############
import numpy as np
import numpy
#from tensorflow.keras.models import load_model
#import cv2
import os
from pathlib import Path
##############
from random import randrange, uniform
from PIL import Image
from django.utils import timezone

@login_required
@student_only
def covid_image_uploadstudent(request):
    #this is to allow only users that allow location access to upload image
    coviduser=request.user
    location = Data.objects.filter(user=coviduser).last()
    two_minute_ago = timezone.now() - timezone.timedelta(minutes=2)
    if not location:
        return HttpResponse('<h2>Invalid Method</h2>')
    elif location.created < two_minute_ago:
        return HttpResponse('<h2>Location time expired, Kindly allow system to access your current location again</h2>')
    else:
        print ('location ok')
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            new_covid = form.save(commit=False)
            new_covid.data = location
            new_covid.save()
            # temp commentttt
            # send_mail(
            #     'COVID-NEU Image Upload',
            #     'Dear NEU Admin' + ',\n' + 'An image has just been uploaded for analysis ' + ',\n' + 'Thank you.',
            #     'segs@gmail.com',  # Admin
            #     [
            #         # email,
            #         'oooladeleodewole@gmail.com',
            #         'fadi.alturjman@neu.edu.tr',
            #         # str(many),
            #         # many,
            #     ]
            # )
            return HttpResponse('<h2>Succesfully Uploaded, Kindly await response from our team within 24hrs</h2>')
    else:
        form = ImageForm()
    return render(request, 'dashboard/covid_form.html', {'form': form})





@login_required
@lecturer_only
def covid_image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            #######
            cat = form.cleaned_data.get('category')
            if cat.name == 'Girne':
                info = Data.objects.create(
                    latitude=uniform(35.3100763, 35.3150769),
                    longitude=uniform(33.0102909, 33.0152909),
                    country='Girne'
                )
                info.save()
            elif cat.name == 'Lefkosa':
                info = Data.objects.create(
                    latitude=uniform(35.19000, 35.1922324),
                    longitude=uniform(33.322222, 33.3273613),
                    country='Lefkosa'
                )
                info.save()
            elif cat.name == 'Maguza':
                info = Data.objects.create(
                    latitude=uniform(35.119000, 35.1193908),
                    longitude=uniform(33.863000, 33.8639264),
                    country='Maguza'
                )
                info.save()
            ########
            form.save()
            # return HttpResponse('Succesfulllllllllllllll')
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'dashboard/covid_form.html', {'form': form})


@login_required
@lecturer_only
def success(request):
    return HttpResponse('successfully uploaded')




# from  django.views.decorators.csrf  import  csrf_exempt
# # @method_decorator(csrf_exempt)
#
# @csrf_exempt
# def postmethod(request):
#     data= request.POST.get('data','')
#     # data = request.get_json()
#     print (data)
#     # return jsonify(data)
from django.contrib import messages
#from tensorflow import keras

@login_required
@lecturer_only
def predict_upload(request, pk):
    pass
    #this is to allow only users that allow location access to upload image
    qs = Covid.objects.get(id=pk)
    qs2 = Data.objects.get(id=qs.data_id)
    image = qs.image.url
    print(image)

    if request.method == 'POST':
        messages.success(request, 'Successfully Analyzed')
        return redirect('datalist')









# bkup
# def predict_upload(request):
#     #this is to allow only users that allow location access to upload image
#     coviduser=request.user
#     covid_chest = load_model('./Machine/covid_new_model1.h5')
#     location = Data.objects.filter(user=coviduser).last()
#     if not location:
#         return HttpResponse('<h2>Invalid Method</h2>')
#     if request.method == 'POST':
#         # covid_chest = load_model('./Machine/covid_new_model1.h5')
#         form = ImageForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             new_covid = form.save(commit=False)
#             new_covid.data = location
#             new_covid.image = request.FILES['image']
#             #######
#             #this works
#             # covid_chest = load_model(os.path.join("./Machine/", "covid_new_model1.h5"))
#             #this also works
#
#
#             # covid_chest = load_model('./Machine/covid_new_model1.h5')
#             # read file
#             covidimgr = request.FILES['image'].read()
#             npimg = numpy.fromstring(covidimgr, numpy.uint8)
#             covidimgr1 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
#             # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             image = cv2.cvtColor(covidimgr1, cv2.COLOR_BGR2RGB)
#             # arrange format as per keras
#             image = cv2.resize(image, (224, 224))
#             image = np.array(image) / 255
#             image = np.expand_dims(image, axis=0)
#
#             resnet_pred = covid_chest.predict(image)
#             # 08055818653 - video testimonies - Past. Jerry Eze
#             probability = resnet_pred[0]
#             print("Resnet Predictions:")
#             if probability[0] > 0.7:
#                 covid_chest_pred = str('%.2f' % (probability[0] * 100) + '% COVID')
#                 new_covid.status = True
#             else:
#                 covid_chest_pred = str('%.2f' % ((1 - probability[0]) * 100) + '% NonCOVID')
#                 new_covid.status = False
#             print(covid_chest_pred)
#             # cat = form.cleaned_data.get('category')
#
#             new_covid.save()
#             ########
#             # form.save()
#             return HttpResponse('<h2>Succesfully Uploaded, Kindly await response from our team</h2>')
#     else:
#         form = ImageForm()
#     return render(request, 'dashboard/covid_form.html', {'form': form})

###################
@login_required
@lecturer_only
def positive_table(request):
    title = 'Corona Positive Users'
    # new
    form = LocationSearchForm(request.POST or None)
    # queryset = Covid.objects.all().select_related('data')
    queryset = Covid.objects.filter(status=True).select_related('data')
    # queryset = Covid.objects.select_related('data').all()
    context = {
        "title": title,
        "form": form,
        "queryset": queryset,
    }
    #not implemented
    if request.method == 'POST':
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        Data.objects.filter(Q(longitude__icontains=longitude) | Q(latitude__icontains=latitude))
        # queryset = Data.objects.filter(latitude__icontains=latitude)
        # if (longitude != ''):
        #     queryset = queryset.filter(longitude__icontains=longitude)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="User Locations.csv"'
            writer = csv.writer(response)
            writer.writerow(['USER', 'LONGITUDE', 'LATITUDE'])
            instance = queryset
            for x in instance:
                writer.writerow([x.user.username, x.longitude, x.latitude])
            return response

        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }

    return render(request, 'dashboard/positive.html', context)



@login_required
@lecturer_only
def last_positive_location(request):
    title = 'List of last location of positive Users'
    # new filter by group of users
    #finally it worked
    # queryset = Covid.objects.filter(status=True).select_related('data')
    queryset = Data.objects.filter(statusn=True)
    latest_dates = queryset.values('user').annotate(latest_created_at=Max('created'))
    queryset = queryset.filter(created__in=latest_dates.values('latest_created_at')).order_by('-created')
    print (queryset)
    #for-Posgres database alone
    # queryset = Data.objects.all().order_by('user', '-created').distinct('user')
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, 'dashboard/table1.html', context)




    if not location:
        return HttpResponse('<h2>Invalid Method</h2>')
    elif location.created > one_minute_ago:
        return HttpResponse('<h2>Location time expired, Kindly allow system to access your current location</h2>')
    else:
        print ('location ok')

@login_required
def status(request):
    user = request.user
    # last = Data.objects.filter(user=user).last()
    # one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
    if not Covid.objects.filter(data__user=user):
        return HttpResponse('<h2>Kinldy Upload CT image to check Status</h2>')
    # elif last.created > one_minute_ago:
    #     return HttpResponse('<h2>Location time expired, Kindly allow system to access your current location</h2>')
    else:
        queryset = Covid.objects.filter(data__user=user).last()
        # queryset = Data.objects.filter(user=user).last()
        context = {
            "queryset": queryset,
        }
        return render(request, 'dashboard/status.html', context)


#--------------------------------------------CONTACT US---------------

from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail

class SendFormEmail(View):

    def  get(self, request):
        #######map
        m = folium.Map(location=[35, 33], zoom_start=8)

        map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
        map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
        map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
        map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
        map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
        folium.LayerControl().add_to(m)
        m = m._repr_html_()

        ##########
        # Get the form data
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        message = request.GET.get('message', None)
        #seg
        # receivers = []
            # recievers.append(user.email)
        for user in User.objects.filter(is_employee=True):
            # receivers.append(user.email)
            many = user.email
        #to send to all users
        # Send Email
        send_mail(
            'COVID NEU Web Contact Form',
            'Hello NEU Admin' + ',\n' + name +' sent you the below message' + ',\n' + message,
            'segs@gmail.com', # Admin
            [
                # email,
                'oooladeleodewole@gmail.com',
                'fadi.alturjman@neu.edu.tr',
                # str(many),
                # many,
            ]
        )

        # Redirect to same page after form submit
        context = {
            'm': m
        }
        messages.success(request, ('Message sent successfully. Thanks for contacting us.'))
        return redirect('contact_us')
    #newwwww
        # return render(request, 'dashboard/contact_us.html', context)


#delete
@login_required
@lecturer_only
def delete_location(request, pk):
    # if request.session.has_key('username'):
    queryset = Data.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('datalist')


@login_required
@lecturer_only
def delete_analysis(request, pk):
    # if request.session.has_key('username'):
    queryset = Covid.objects.get(id=pk)
    qs = Data.objects.get(id=queryset.data_id)
    if request.method == 'POST':
        queryset.delete()
        qs.statusn = None
        qs.save()
        messages.success(request, 'Successfully Deleted')
        return redirect('datalist')