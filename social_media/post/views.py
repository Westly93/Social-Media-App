from django.shortcuts import render, redirect, get_object_or_404
from django.urls import  reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from .models import Post, Comment, Image
from .forms import PostForm, CommentForm
from django.views import View 
from users.models import Notifications
from django.core.paginator import Paginator



class PostlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        logged_in_user= request.user
        page= request.GET.get('page', 1)
        post_list= Post.objects.filter(
            author__profile__followers__in= [logged_in_user.id]
        ).order_by('-date_posted')
        paginator= Paginator(post_list, 3)
        posts= paginator.page(page)
        context= {
            'posts': posts,
            'form': form,
            'paginator': paginator
        }

        return render(request, 'post/post_list.html', context)
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        logged_in_user= request.user
        post_list= Post.objects.filter(
            author__profile__followers__in= [logged_in_user.id]
        ).order_by('-date_posted')
        page= request.GET.get('page', 1)
        paginator= Paginator(post_list, 3)
        posts= paginator.page(page)
        files= request.FILES.getlist('image')
        if form.is_valid():
            new_post= form.save(commit= False)
            new_post.author= request.user
            new_post.save()
            for file in files:
                img= Image(image= file)
                img.save()
                new_post.image.add(img)
            new_post.save()
            
            return redirect('posts')
        context= {
            'posts': posts,
            'form': form,
            'paginator': paginator 
        }
        return render(request, 'post/post_list.html', context)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Post
    success_url= '/'

    def test_func(self):
        post= self.get_object() 
        if post.author== self.request.user:
            return True
        return False



class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, post_id, *args, **kwargs):
        form= CommentForm()
        post= get_object_or_404(Post, pk= post_id)
        comments= Comment.objects.filter(post=post).order_by('-date_posted')
        context= {
            'post': post,
            'form': form,
            'comments': comments
        }
        return render(request, 'post/post_detail.html', context)


    def post(self, request, post_id, *args, **kwargs):
        form= CommentForm(request.POST)
        post= get_object_or_404(Post, pk= post_id)
        comments= Comment.objects.filter(post=post)
        if form.is_valid():
            new_form= form.save(commit= False)
            new_form.post= post 
            new_form.author= request.user 
            new_form.save()
            #1= like, 2= comment, 3= follow
            notification= Notifications.objects.create(from_user= request.user, post= post,
                notification_type= 2, to_user= post.author
            )
            return redirect('post-detail', post_id= post_id)
        context= {
            'post': post,
            'form': form,
            'comments': comments
        }
        return render(request, 'post/post_detail.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model= Post
    form_class= PostForm
    

    def form_valid(self, form):
        form.instance.author== self.request.user 
        return super().form_valid(form)

    def test_func(self):
        post= self.get_object()
        if self.request.user== post.author:
            return True 
        return False

# Deleting a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Comment

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs= {'post_id': self.object.post.pk})

    def test_func(self):
        comment= self.get_object()
        if comment.author== self.request.user:
            return True 
        return False
# Updating a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model= Comment 
    form_class= CommentForm
    template_name= 'post/post_form.html'
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs= {'post_id': self.object.post.pk})

    def test_func(self):
        comment= self.get_object()
        if comment.author== self.request.user:
            return True 
        return False


class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post= Post.objects.get(pk= post_pk)
        parent_comment= Comment.objects.get(pk= pk)

        form= CommentForm(request.POST)
        if form.is_valid():
            comment_reply= form.save(commit= False)
            comment_reply.author= request.user
            comment_reply.post= post
            comment_reply.parent= parent_comment
            comment_reply.save()
        notification= Notifications.objects.create(from_user= request.user,
            notification_type= 2, to_user= parent_comment.author, comment= parent_comment
        )

        return redirect('post-detail', post_id=post_pk)   

class LikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post= get_object_or_404(Post, pk= pk)
        is_like= False
        for like in post.likes.all():
            if like== request.user:
                is_like= True
                break

        is_dislike= False 
        for dislike in post.dislikes.all():
            if dislike== request.user:
                dislike= True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        if not is_like:
            post.likes.add(request.user)

            notification= Notifications.objects.create(from_user= request.user,
                notification_type= 1, to_user= post.author, post= post
            )
        if is_like:
            post.likes.remove(request.user)

        #next= request.POST.get('next', '/')
        #return HttpResponseRedirect(next)
        return redirect('posts')

class DisLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post= get_object_or_404(Post, pk=pk)

        is_dislike= False
        for dislike in post.dislikes.all():
            if dislike== request.user:
                is_dislike= True
                break
        
        is_like=False

        for like in post.likes.all():
            if like== request.user:
                is_like= True
                break

        if is_like:
            post.likes.remove(request.user)
        
        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.dislikes.remove(request.user)

        return redirect('posts')


class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment= Comment.objects.get(pk=pk)
        is_like= False
        for like in comment.likes.all():
            if like== request.user:
                is_like= True
                break

        is_dislike= False 
        for dislike in comment.dislikes.all():
            if dislike== request.user:
                dislike= True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        if not is_like:
            comment.likes.add(request.user)
            notification= Notifications.objects.create(from_user= request.user,
                notification_type= 1, to_user= comment.author, comment= comment
            )
        if is_like:
            comment.likes.remove(request.user)

        #next= request.POST.get('next', '/')
        #return HttpResponseRedirect(next)
        return redirect('post-detail', comment.post.pk)

class CommentDisLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment=Comment.objects.get(pk=pk)

        is_dislike= False
        for dislike in comment.dislikes.all():
            if dislike== request.user:
                is_dislike= True
                break
        
        is_like=False

        for like in comment.likes.all():
            if like== request.user:
                is_like= True
                break

        if is_like:
            comment.likes.remove(request.user)
        
        if not is_dislike:
            comment.dislikes.add(request.user)
        if is_dislike:
            comment.dislikes.remove(request.user)

        return redirect('post-detail', comment.post.pk)