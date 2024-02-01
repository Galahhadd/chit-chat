from django.urls import path

from .views import (home, 
					room, 
					createRoom, 
					updateRoom, 
					deleteRoom, 
					loginPage, 
					logoutView,
					registerUser,
					deleteMessage,
					userProfile,
					updateUser,
					topicsPage,
					activityPage,)

urlpatterns = [
	path('login/', loginPage, name='login'),
	path('logout/', logoutView, name='logout'),
	path('register/', registerUser, name='register'),
	path('profile/<str:id>/', userProfile, name='user-profile'),
	path('update-user/', updateUser, name='update-user'),

	path('', home, name = 'home'),
	path('room/<str:id>/', room, name = 'room'),
	path('create-room/', createRoom, name='create-room' ),
	path('update-room/<str:id>/', updateRoom, name='update-room'),
	path('delete-room/<str:id>/', deleteRoom, name='delete-room'),
	path('delete-message/<str:id>/', deleteMessage, name='delete-message'),
	path('topics/', topicsPage, name='topics'),
	path('activity/', activityPage, name='activity')

	
]