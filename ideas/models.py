from django.db import models
from django.contrib.auth.models import User # ← Userモデルをインポート

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_ideas', blank=True) # ← この行に変更
    author = models.ForeignKey(User, on_delete=models.CASCADE) # ← これを追加
    image = models.ImageField(verbose_name="画像", upload_to='images/', blank=True, null=True)
    video = models.FileField(verbose_name="動画", upload_to='videos/', blank=True, null=True)


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    text = models.TextField(verbose_name="コメント")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]