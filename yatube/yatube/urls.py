from django.contrib import admin
from django.urls import include, path
from posts import views

posts_patterns = ([
    path('', views.index, name="index"),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit')
], 'posts')

urlpatterns = [
    path('', include(posts_patterns)),
    path('', include('posts.urls', namespace='post')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]

# handler404 = 'core.views.page_not_found'
# handler403 = 'core.views.csrf_failure'
