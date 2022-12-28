from django.db import models
from users.models import User


class Category(models.Model):
    category = models.CharField(max_length=20)


class Solution(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    solution_image = models.ImageField(blank=True, null=True, upload_to="")
    nickname = models.CharField(max_length=20, null=True)
    wise = models.TextField()
    category = models.ManyToManyField(Category, related_name='connected_solution')


class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Article(models.Model):
    class Meta:
        ordering = ['-id']
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=10)
    solution = models.ManyToManyField(Solution, related_name='connected_article')    
    content = models.TextField()
    mbti = models.CharField(max_length=50)
    new_comment = models.BooleanField()


class Comment(models.Model):
    class Meta:
        ordering = ['-id']
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comment')