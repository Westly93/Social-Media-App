from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django_resized import ResizedImageField


class Post(models.Model):
    body= models.TextField()
    image= models.ManyToManyField('Image', blank= True, null= True)
    author= models.ForeignKey(User, on_delete= models.CASCADE)
    date_posted= models.DateTimeField(default= timezone.now)
    likes= models.ManyToManyField(User, related_name= 'likes', blank= True)
    dislikes= models.ManyToManyField(User, related_name= 'dislikes', blank= True)


    def __str__(self):
        return f'{self.body}'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs= {'post_id': self.pk})

class Comment(models.Model):
    comment= models.TextField()
    date_posted= models.DateTimeField(default= timezone.now)
    author= models.ForeignKey(User, on_delete= models.CASCADE)
    post= models.ForeignKey(Post, on_delete= models.CASCADE)
    parent= models.ForeignKey('self', null= True, blank= True, on_delete= models.CASCADE, related_name= '+')
    likes= models.ManyToManyField(User, related_name= 'comment_likes', blank= True)
    dislikes= models.ManyToManyField(User, related_name= 'comment_dislikes', blank= True)

    @property
    def children(self):
        return Comment.objects.filter(parent= self).all()

    @property
    def is_parent(self):
        if self.parent== None:
            return True
        return False

    def get_absolute_url(self):
        return reverse('post-detail', kwargs= {'post_pk': self.post.pk})

    def __str__(self):
        return f'{self.comment}'


class Image(models.Model):
    image= ResizedImageField(size= [200, 200], quality= 100, upload_to= 'posts', null= True, blank= True)

    


    