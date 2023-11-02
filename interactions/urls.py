from django.urls import path
from . import views

app_name = "interactions"
urlpatterns = [
    path("subscribe/channel/<int:channel_id>/", views.SubscribeChannelView.as_view()),
    path(
        "unsubscribe/channel/<int:channel_id>/", views.UnsubscribeChannelView.as_view()
    ),
    path("subscribed_channels/", views.ListOfSubscribedChannelsView.as_view()),
    path("like/episode/<int:episode_id>/", views.LikeEpisodeView.as_view()),
    path("unlike/episode/<int:episode_id>/", views.UnlikeEpisodeView.as_view()),
    path("liked_episodes/", views.ListOfLikedEpisodesView.as_view()),
    path("bookmark/episode/<int:episode_id>/", views.BookmarkEpisodeView.as_view()),
    path(
        "bookmark/episode/<int:episode_id>/<str:playlist_name>/",
        views.BookmarkEpisodeView.as_view(),
    ),
    path("unbookmark/episode/<int:episode_id>/", views.UnbookmarkEpisodeView.as_view()),
    path("bookmark/channel/<int:channel_id>/", views.BookmarkChannelView.as_view()),
    path(
        "bookmark/channel/<int:channel_id>/<str:playlist_name>/",
        views.BookmarkChannelView.as_view(),
    ),
    path("unbookmark/channel/<int:channel_id>/", views.UnbookmarkChannelView.as_view()),
    path("bookmarked_episodes/", views.ListOfBookmarkedEpisodesView.as_view()),
    path("bookmarked_channels/", views.ListOfBookmarkedChannelsView.as_view()),
    path("bookmarked_items/", views.ListOfAllBookmarkedItemsView.as_view()),
    path("comment/episode/<int:episode_id>/", views.CommentEpisodeView.as_view()),
    path("uncomment/episode/<int:comment_id>/", views.UncommentEpisodeView.as_view()),
    path("episode_comments/<int:episode_id>/", views.GetEpisodeCommentsView.as_view()),
]
