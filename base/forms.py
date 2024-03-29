from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
	class Meta:
		model = Room 
		fields = '__all__'
		exclude = ['host', 'participants', 'description']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['name','username', 'email', 'avatar', 'bio']