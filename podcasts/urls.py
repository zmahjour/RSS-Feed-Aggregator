from django.urls import path

app_name = "podcasts"
urlpatterns = [path("rss/", views.RssView.as_view())]
