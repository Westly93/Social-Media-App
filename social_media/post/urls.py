from django.urls import path
from .views import (PostlistView, PostDetailView, PostUpdateView, 
    PostDeleteView, CommentDeleteView, LikeView, DisLikeView, CommentDisLikeView, 
    CommentLikeView, CommentUpdateView, CommentReplyView
    )


urlpatterns= [
    path('', PostlistView.as_view(), name= 'posts'),
    path('<int:post_id>/', PostDetailView.as_view(), name= 'post-detail'),
    path('<int:post_id>/comments/<int:pk>/like', CommentLikeView.as_view(), name= 'comment-like'),
    path('<int:post_id>/comments/<int:pk>/dislike', CommentDisLikeView.as_view(), name= 'comment-dislike'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name= 'post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name= 'post-delete'),
    path('<int:pk>/like/', LikeView.as_view(), name= 'post-like'),
    path('<int:pk>/dislike/', DisLikeView.as_view(), name= 'post-dislike'),
    path('<int:post_pk>/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name= 'comment-delete'),
    path('<int:post_pk>/comments/<int:pk>/update/', CommentUpdateView.as_view(), name= 'comment-update'),
    path('<int:post_pk>/comments/<int:pk>/reply/', CommentReplyView.as_view(), name= 'comment-reply'),
]