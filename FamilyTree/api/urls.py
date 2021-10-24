from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import PersonAPIView, RelationAPIView, RelationUpdateAPIView

urlpatterns = [
    path("person/", PersonAPIView.as_view()),
    path("person/<int:pk>/", PersonAPIView.as_view()),
    path("relation/", RelationAPIView.as_view()),
    path("relation/<int:pk>/", RelationUpdateAPIView.as_view()),
    path("relation/<int:person>/<str:relation>/", RelationAPIView.as_view()),
]
