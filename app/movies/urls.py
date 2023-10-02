from django.urls import path

from movies.views import IndexView, CategoryListView, MovieDetailView

app_name = "movies"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<slug:category>/", CategoryListView.as_view(), name="category"),
    path("movie/<slug:slug>/", MovieDetailView.as_view(), name="movie"),
]
