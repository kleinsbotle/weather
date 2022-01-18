from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('forecast/<str:city>/<str:units>/', views.ForecastView.as_view()),
    path('report/<str:start>/<str:end>/', views.ReportView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
