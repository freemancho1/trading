from django.urls import path
from .views import *


app_name = 'common'

urlpatterns = [
    path('', starting_point, name='start'),

    path('login/', login, name='login'),

    path('main/', main, name='main'),
]