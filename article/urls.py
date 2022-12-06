from django.urls import path
from article import views
urlpatterns = [
    path('',views.MainView.as_view(),name='main'),
    path('worry/', views.MakeWorryView.as_view(), name = 'make_worry'),
    path('worry/<int:solution_id>/',views.BeeSolutionView.as_view(), name = 'bee_solution' ),
    path('worry/<int:article_id>/comment/',views.CommentView.as_view())
]