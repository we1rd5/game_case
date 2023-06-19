"""GameCase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from GameCase import settings
from Portfolio import views
urlpatterns = [
    path('', views.main_page),
    path('signup', views.signup),
    path('login', views.login),
    path('profile', views.profile),
    path('profile/<str:person>', views.profile),
    path('load_game', views.load_game),
    path('game', views.game),
    path('game/<int:id>', views.game),
    path('add_user_description', views.add_user_desc),
    path('delete', views.delete_game),
    path('rate', views.rate_game),
    path('logout', views.logout),
    path('team', views.team_page)
]

urlpatterns += static(f"game/{settings.MEDIA_URL}",
                          document_root=settings.MEDIA_ROOT)

urlpatterns += static(f"user_photos", document_root=settings.USER_PHOTOS_ROOT)

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)