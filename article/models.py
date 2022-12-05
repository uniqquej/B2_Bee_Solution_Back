from django.db import models
from users.models import User

class Solution(models.Model):
    rating = models.ManyToManyField(User,related_name='sl_rating')
    output_image = models.ImageField(null=True)
    
class Article(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=10)
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE)    
    content = models.TextField()
    mbti = models.CharField(max_length=50)
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_created=True)
    update_at = models.DateTimeField(auto_now=True)
    
