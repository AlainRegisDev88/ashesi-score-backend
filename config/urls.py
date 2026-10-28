from django.contrib import admin
from django.urls import path, include

# importing views is not necessary because include dynamically looks for the views
# from apps import accounts, competitions, content, core, matches, sports, teams

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # api endpoints 
    
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/core/', include('core.urls')),
    path('api/v1/sports/', include('sports.urls')),
    path('api/v1/teams/', include('teams.urls')),
    path('api/v1/competitions/', include('competitions.urls')),
    path('api/v1/matches/', include('matches.urls')),
    path('api/v1/content/', include('content.urls')),
]
