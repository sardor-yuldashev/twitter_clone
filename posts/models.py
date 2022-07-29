from django.db import models
from cloudinary.models import CloudinaryField

class Post(models.Model):
    name = models.CharField('Name', blank=False, null=False, max_length=14, db_index=True, default='Anonymus')
    body = models.CharField('Body', blank=True, null=True, max_length=150, db_index=True)
    image = CloudinaryField('Image', blank=True, null=True)
    date = models.DateTimeField('Date', blank=True, auto_now_add=True)
    like_count = models.IntegerField('Like', blank=True, null=True, default=0)
    def __str__(self):
        return str(self.name)

class User_data(models.Model):
    user_id = models.CharField('User_id', blank=False, null=False, max_length=20)
    liked_post_id = models.IntegerField('Liked_post_id', blank=False, null=False, default=0)
    def __str__(self):
        return str(self.user_id)
