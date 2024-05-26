from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('home/', views.homeview, name='home'),

    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('edit_post/<int:pk>/', views.UpdatePostView.as_view(), name='edit_post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),

    path('signup/', views.signup, name='signup'),
    path('', views.index, name='accueil'),
    path('login/', views.loginp, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)