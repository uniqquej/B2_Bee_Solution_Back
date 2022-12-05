from django.urls import path
from article import views
urlpatterns = [
    path('worry/', views.MakeWorryView.as_view(), name = 'make_worry'),
    path('worry/<int:solution_id>/',views.BeeSolutionView.as_view(), name = 'bee_solution' )
]