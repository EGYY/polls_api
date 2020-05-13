from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('polls', views.PollViewSet, basename='Polls')
router.register('active_polls', views.ActivePollViewSet, basename='ActivePolls')
router.register('completed_polls', views.CompletedPollViewSet, basename='CompletedPolls')
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]