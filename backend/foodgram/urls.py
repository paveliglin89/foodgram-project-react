from django.contrib import admin
from django.urls import include, path

api_patterns = [
    path('', include('ingredients.urls')),
    path('', include('recipes.urls')),
    path('', include('tags.urls')),
    path('', include('users.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(api_patterns)),
]
