from django.urls import path
from socialnetwork import views

urlpatterns = [
    # authentication
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    # home (global stream page)
    path('', views.global_action, name='home'),
    path('global', views.global_action, name='global'),
    path('get-post', views.get_post_action, name='ajax-get-post'),
    path('get-global', views.get_post_action),
    path('get-post-follower', views.get_post_follower_action, name='ajax-get-post-follower'),
    path('get-follower', views.get_post_follower_action),
    path('add-post', views.add_post_action, name='ajax-add-post'),
    path('add-comment', views.add_comment_action, name='ajax-add-comment'),
    path('add-comment-follower', views.add_comment_follower_action, name='ajax-add-comment-follower'),
    # follower stream page
    path('follower', views.follower_action, name='follower'),
    # profile page
    path('profile', views.my_profile_action, name='profile'),
    path('other/<int:user_id>', views.other_profile_action, name='other'),
    path('other/follow/<int:user_id>', views.follow_action, name='follow'),
    path('other/unfollow/<int:user_id>', views.unfollow_action, name='unfollow'),
    path('photo/<int:user_id>', views.get_photo_action, name='photo'),
]
