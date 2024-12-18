"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import CustomLoginView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('base/', views.base, name = 'base'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('select-prefer/', views.select_prefer, name="select-prefer"), 
    path('receiver/', views.receiver, name='receiver'),
    path('giver/', views.giver, name='giver'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('results-receiver/<int:post_ID>/', views.search_matches_receiver, name='results_receiver'),
    path('results-giver/<int:post_ID>/', views.search_matches_giver, name='results_giver'),
    path('post_history/<int:profile_id>/', views.post_history, name='post_history'),
    path('edit_giver_post/<int:post_ID>/', views.edit_giver_post, name='edit_giver_post'),
    path('edit_receiver_post/<int:post_ID>/', views.edit_receiver_post, name='edit_receiver_post'),
    path('delete_giver_post/<int:post_ID>/', views.delete_giver_post, name='delete_giver_post'),
    path('delete_receiver_post/<int:post_ID>/', views.delete_receiver_post, name='delete_receiver_post'),
    path('delete_receiver_post_2/<int:post_ID>/', views.delete_receiver_post_2, name='delete_receiver_post_2'),
    path('verify/<int:giver_post_id>/<int:receiver_post_id>/', views.verify_match, name='verify'),
    path('confirm_verification_giver/<int:match_ID>/', views.confirm_verification_giver, name='confirm_verification_giver'),
    path('confirm_verification_receiver/<int:match_ID>/', views.confirm_verification_receiver, name='confirm_verification_receiver'),
    path('unmatch_post/<int:post_id>/<str:post_type>/', views.unmatch_post, name='unmatch_post'),
    path('match_info_giver/<int:match_id>/', views.match_info_giver, name='match_info_giver'),
    path('match_info_receiver/<int:match_id>/', views.match_info_receiver, name='match_info_receiver'),
    path('search/<int:id>', views.search_posts, name='search_posts'),
    path('send-data-receiver/for-giver-ID-<int:post_ID>',views.send_data_receiver, name = 'send_data_receiver'),
    path('send-data-giver/for-receiver-ID-<int:post_ID>',views.send_data_giver, name = 'send_data_giver'),
    path('detail-giver/<int:post_giver_ID>/<int:post_receiver_ID>/', views.detail_giver, name='detail_giver'),
    path('datail_receiver/<int:post_receiver_ID>/<int:post_giver_ID>/`',views.datail_receiver,name='datail_receiver'),
    path('delete_giver_post_2/<int:post_ID>/',views.delete_giver_post_2,name='delete_giver_post_2'),
    path('contact-us/',views.contact_us,name='contact_us'),
    path('about-us/',views.about_us,name='about_us'),
    path('tutorial/',views.tutorial,name='tutorial')





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
