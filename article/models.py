from django.db import models
from users.models import User

class Category(models.Model):
    category = models.CharField(max_length=50)
    
class Solution(models.Model):
    rating = models.ManyToManyField(User,related_name='sl_rating')
    output_image = models.ImageField(null=True)
    
class Article(models.Model):
    article_user = models.ForeignKey(User,on_delete=models.CASCADE)
    article_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    article_solution = models.ForeignKey(Solution,on_delete=models.CASCADE)    
    content = models.TextField()
    mbti = models.CharField(max_length=50)
    
class Comment(models.Model):
    comment_user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_created=True)
    update_at = models.DateTimeField(auto_now=True)
    
