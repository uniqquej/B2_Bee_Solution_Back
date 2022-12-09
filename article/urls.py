from django.urls import path
from article import views
urlpatterns = [
    path('<int:category_id>/',views.MainView.as_view(),name='main'),
    path('worry/', views.MakeWorryView.as_view(), name = 'make_worry'),
    path('worry/<int:solution_id>/',views.BeeSolutionView.as_view(), name = 'bee_solution' ),
    path('<int:article_id>/comment/',views.CommentView.as_view()),    
    path('<int:article_id>/detail/',views.ArticleDetailView.as_view()),
    path('<int:article_id>/solution/', views.MakeSolutionView.as_view(), name='make_solution'),
    path('<int:article_id>/comment/<int:comment_id>/',views.CommentDetailView.as_view()),
    # path('category/<int:category_id>/', views.ArticleListView.as_view(), name = 'article_list'),
    path('allsolution/', views.AllBeeSolutionView.as_view(), name='all_solution'),
]