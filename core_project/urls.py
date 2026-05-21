"""
URL configuration for core_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from tickets.views import (home_view, search_view, koltuk_secimi_view, odeme_view,
                           basarili_view, bilet_pdf_indir_view, bilet_yazdir_view,
                           register_view, login_view, logout_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('search/', search_view, name='search'),
    path('sefer/<int:sefer_id>/koltuklar/', koltuk_secimi_view, name='koltuk_secimi'),
    path('odeme/<int:sefer_id>/', odeme_view, name='odeme'),
    path('basarili/', basarili_view, name='basarili'),
    path('bilet-indir/<int:bilet_id>/', bilet_pdf_indir_view, name='bilet_indir'),
    path('bilet/<int:bilet_id>/yazdir/', bilet_yazdir_view, name='bilet_yazdir'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]