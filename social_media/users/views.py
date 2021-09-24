from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q 
from django.views import View
from django.contrib import messages
from post.models import Post
from users.models import Profile, Notifications
from django.contrib.auth.models import User 
from django.core.paginator import Paginator


class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        form= UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Account has been created successifully, You can now login!')
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        u_form= UserUpdateForm(instance= request.user)
        p_form= ProfileUpdateForm(instance= request.user.profile)
        context= {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form= UserUpdateForm(request.POST, instance= request.user)
        p_form= ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile)
        context= {
            'u_form': u_form,
            'p_form': p_form
        }
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'You profile has been updated successfully!')
            return redirect('posts')
        messages.warning(request, 'Failed to update your profile!')
        return render(request, 'users/profile.html', context)

class UserPostsView(View):
    def get(self, request, username, *args, **kwargs):
        user= User.objects.filter(username= username).first()
        post_list= Post.objects.filter(author= user).order_by('-date_posted')
        page= request.GET.get('page', 1)
        paginator= Paginator(post_list, 3)
        posts= paginator.page(page)
        followers= user.profile.followers.all()
        followers_num= len(user.profile.followers.all())

        is_follower= False

        for follower in followers:
            if follower == request.user:
                is_follower= True
                break

        context= {
            'user': user,
            'posts': posts, 
            'is_follower': is_follower,
            'followers_num': followers_num,
            'paginator': paginator
        }
        return render(request, 'users/user_posts.html', context)

class AddFollowerView(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        user= User.objects.filter(username= username).first()
        user.profile.followers.add(request.user)
        notification= Notifications.objects.create(from_user= request.user,
                notification_type= 3, to_user= user
            )

        return redirect('user-posts', username= username)


class RemoveFollowerView(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        user= User.objects.filter(username= username).first()
        user.profile.followers.remove(request.user)

        return redirect('user-posts', username= username)


class UserProfileSearchView(View):
    def get(self, request, *args, **kwargs):
        query= self.request.GET.get('query')
        profile_list= Profile.objects.filter(
            Q(user__username__icontains= query)
        )
        is_empty= False
        if len(profile_list) == 0:
            is_empty=True
        context= {
            'profile_list': profile_list,
            'is_empty': is_empty
        }
        return render(request, 'users/search.html', context)


class FollowersListView(LoginRequiredMixin, View):
    def get(self, request, username, *args, **kwargs):
        user= User.objects.filter(username= username).first()
        profile= Profile.objects.filter(user= user).first()
        followers= profile.followers.all()

        context= {
            'profile': profile,
            'followers': followers
        }

        return render(request, 'users/user_followers.html', context)

class PostNotificationView(View):
    def get(self, request, post_pk, notification_pk, *args, **kwargs):
        post= Post.objects.get(pk= post_pk)
        notification= Notifications.objects.get(pk= notification_pk)

        notification.user_has_seen= True
        notification.save()

        return redirect('post-detail', post_id= post_pk)


class FollowNotificationView(View):
    def get(self, request, notification_pk, username, *args, **kwargs):
        user= User.objects.filter(username= username).first()
        profile= Profile.objects.filter(user= user).first()
        notification= Notifications.objects.get(pk= notification_pk)

        notification.user_has_seen= True
        notification.save()

        return redirect('user-posts', username= username)