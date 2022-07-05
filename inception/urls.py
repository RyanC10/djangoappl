from django.test import TestCase

# Create your tests here.

from . import views
from django.urls import include, path
from inception.views import nba


urlpatterns= [
    

    path(r'nba/', nba.as_view(), name='nba'),
    
    ]


