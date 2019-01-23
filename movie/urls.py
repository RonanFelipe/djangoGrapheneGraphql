from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from movie import views

router = DefaultRouter()
router.register(r'movies', views.MovieSet)
router.register(r'actors', views.ActorSet)
router.register(r'directors', views.DirectorSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
