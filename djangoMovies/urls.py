"""djangoMovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('movieAPI/(?P<version>(v1|v2))/', include('movie.urls')),
    path(r'^__debug__', include(debug_toolbar.urls)),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # re_path('.*', TemplateView.as_view(template_name='index.html')),
]
