from django.urls import path
from article import views

urlpatterns = [
    path('<int:category_id>/', views.MainView.as_view(), name='main'),
    path('<int:category_id>/profile/', views.ProfileArticleView.as_view(), name='profile_article'),
    path('worry/', views.MakeWorryView.as_view(), name='make_worry'),
    path('worry/<int:solution_id>/', views.BeeSolutionView.as_view(), name='bee_solution'),
    path('worry/promotion/', views.MakeWorryPromotionView.as_view(), name='make_worry_promotion'),
    path('<int:article_id>/detail/', views.ArticleDetailView.as_view()),
    path('<int:article_id>/solution/', views.MakeSolutionView.as_view(), name='make_solution'),
    path('<int:article_id>/comment/', views.CommentView.as_view(), name = 'comment_view'),
    path('<int:article_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name = 'comment_detail'),
    path('<int:article_id>/comment/<int:comment_id>/likes/', views.CommentLikeView.as_view()),
    path('allsolution/', views.AllBeeSolutionView.as_view(), name='all_solution'),
    path('mysolution/', views.MyBeeSolutionView.as_view(), name='my_solution'),
    path('solution/<int:solution_id>/', views.SolutionDetailView.as_view(), name='solution_detail'),
    path('alarm/<int:check>/', views.AlarmView.as_view(), name='alarm'),
]