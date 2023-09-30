from django.urls import path

from movies.views import index

app_name = "movies"

urlpatterns = [
    path("", index, name="index"),
]
