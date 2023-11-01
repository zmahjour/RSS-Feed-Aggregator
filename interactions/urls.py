from django.urls import path
from . import views

app_name = "interactions"
urlpatterns = [
    path("like/<int:episode_id>/", views.LikeEpisodeView.as_view()),
    path("unlike/<int:episode_id>/", views.UnlikeEpisodeView.as_view()),
]
