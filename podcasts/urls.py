from django.urls import path
from . import views

app_name = "podcasts"
urlpatterns = [
    path("rss/", views.RssView.as_view()),
    path("update/one/", views.CreateOrUpdateOneChannelView.as_view()),
    path("update/all/", views.CreateOrUpdateAllChannelsView.as_view()),
    path("channels/", views.ListOfChannelsView.as_view()),
    path("<int:channel_id>/episodes/", views.ListOfEpisodesView.as_view()),
]
