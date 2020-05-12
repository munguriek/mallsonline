from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views as user_views
from .views import *


urlpatterns = [
    path('', user_views.users_home, name='users-home'),
	path('login_success/', user_views.login_success, name='login-success'),
	path('login/', auth_views.LoginView.as_view(template_name='acade_owner/base.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='acade_owner/base.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('upadte_profile/', user_views.updateprofile, name='update-profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='acade_owner/base.html'), name='password-reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='acade_owner/base.html'), name='password_reset_done'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='acade_owner/base.html'), name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='acade_owner/base.html'), name='password_reset_confirm'),
    path('users_free_rooms/', FreeRooms.as_view(), name='users-free-rooms'),
    path('my_rooms/', MyRooms.as_view(), name='my-rooms'),
    path('complain/', ComplainCreateView.as_view(), name='complain'),
    path('complains/', MyComplainsListView.as_view(), name='my-complains'),
    path('user_complains/', AllComplainsListView.as_view(), name='user-complains'),
    path('complain/<int:pk>/update', ComplainUpdateView.as_view(), name='update-complain'),
    path('user_room/<int:pk>', RoomDetails.as_view(), name='user_room_detail'),
    path('my_room_details/<int:pk>', MyRoomDetails.as_view(), name='book-room-details'),
    path('shop/', ShopCreateView.as_view(), name='shop'),
    path('my_shops/', MyShopListView.as_view(), name='my-shops'),
    path('shop/<int:pk>', ShopDetailView.as_view(), name='shop-details'),
    path('shop/<int:pk>/update', ShopUpdateView.as_view(), name='update-shop'),
    path('product/', ProductCreateView.as_view(), name='product'),
    path('my_products/', MyProductListView.as_view(), name='my-products'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-details'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='update-product'),
    url(r'^book_room/(?P<id>\d+)/$', user_views.book_room, name='book-room'),
    url(r'^complain/(?P<id>\d+)/$', user_views.comment, name='complain-details'),
    url(r'^update_comment/(?P<id>\d+)/$', user_views.update_comment, name='update-comment'),
    url(r'^update_book_room/(?P<id>\d+)/$', user_views.update_book_room, name='update-book-room'),


]
