from django.urls import path
from . import views

app_name = "podcasts"
urlpatterns = [path("rss/", views.RssView.as_view())]
