from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('indexc', views.index, name='dashboard-index'),
    path('team/', views.team, name='team'),
    #intermdate
    path('i3/', views.index50, name='index50'),
    # path('i3/<str:x>/<str:y>', views.index50, name='index50'),
    path('pum/<str:pk>/', views.per_user_map1, name='perusermap1'),
    path('put/<str:pk>/', views.individual_table, name='perusertable'),
    path('i8/', views.index8, name='index8'),
    path('search/', views.Search, name='search'),
    path('status/', views.status, name='status'),
    path('userl/', views.all_users_table, name='userslist'),
    path('datal/', views.location_log_table, name='datalist'),
    path('positive/', views.positive_table, name='positive'),
    path('lastl/', views.last_location, name='lastlocation'),
    path('positivel/', views.last_positive_location, name='last_positive_location'),
    path('lastlmap/', views.last_location_map, name='lastlocationmap'),
    path('predict/<str:pk>/', views.predict_upload, name="predict_upload"),
#new 17.5.21
    # path('image_upload', views.covid_image_upload, name = 'image_upload'),
    path('image_upload1', views.covid_image_uploadstudent, name = 'covid_image_uploadstudent'),
    path('success', views.success, name = 'success'),
    #dellete
    path('delete_location/<str:pk>/', views.delete_location, name="delete_location"),
    path('delete_analysis/<str:pk>/', views.delete_analysis, name="delete_analysis"),

    #contact us
    path('contact/', TemplateView.as_view(template_name="dashboard/contact_us.html"), name='contact_us'),
    path('send-form-email/', views.SendFormEmail.as_view(), name='send_email'),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
