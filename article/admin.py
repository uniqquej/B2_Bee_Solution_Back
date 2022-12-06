from django.contrib import admin
from article.models import Solution, Rating, Article, Comment

admin.site.register(Solution)
admin.site.register(Rating)
admin.site.register(Article)
admin.site.register(Comment)