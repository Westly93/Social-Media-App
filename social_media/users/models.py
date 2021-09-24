from django.db import models
from post.models import Post, Comment
from django.utils import timezone
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    bio= models.TextField(blank= True, null= True)
    current_city= models.CharField(max_length= 200, blank= True, null= True)
    image= ResizedImageField(size= [200, 200], quality= 100, upload_to= 'Profiles', 
        default= 'default.jpg')
    followers= models.ManyToManyField(User, related_name= 'followers', blank= True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender= User)
def create_profile(sender, created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(user= instance)

@receiver(post_save, sender= User)
def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()


class Notifications(models.Model):
    notification_type= models.IntegerField()
    to_user= models.ForeignKey(User, related_name= 'notification_to', null= True, on_delete= models.CASCADE)
    from_user= models.ForeignKey(User, related_name= 'notification_from', null= True, on_delete= models.CASCADE)
    post= models.ForeignKey(Post, related_name= '+', null= True, blank= True, on_delete= models.CASCADE)
    comment= models.ForeignKey(Comment, related_name= '+', null= True, blank= True,  on_delete= models.CASCADE)
    date= models.DateTimeField(default= timezone.now)
    user_has_seen= models.BooleanField(default= False)