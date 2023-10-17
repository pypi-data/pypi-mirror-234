from django.urls import include, path

urlpatterns = [
    path(r'', include('kalabash.urls')),
]
