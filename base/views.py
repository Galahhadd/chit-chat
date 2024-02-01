from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


def loginPage(request):

	page = 'login'

	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')

		try:
			user = User.objects.get(email=email)
		except:
			messages.error(request, 'User does not exist')

		user = authenticate(request, email=email, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Wrong Password')

	context = {'page':page}
	return render(request,'accounts/login_register.html', context)

def logoutView(request):
	logout(request)
	return redirect('home')

def registerUser(request):
	form = MyUserCreationForm()

	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, "An Error occured during registration")

	return render(request, 'accounts/login_register.html', {'form':form})

def home(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	rooms = Room.objects.filter(Q(topic__name__icontains=q)|
		Q(name__icontains=q)|
		Q(description__icontains=q))

	topics = Topic.objects.all()[0:5]
	room_count = rooms.count()
	room_messages = Message.objects.filter(room__in=rooms)
	print(room_messages)

	context = {'rooms': rooms, 'topics':topics,
	'rooms_count': room_count, 'room_messages':room_messages}
	return render(request, 'base/home.html', context)

def room(request, id):
	room = Room.objects.get(id=id)
	room_messages = room.message_set.all()
	participants = room.participants.all()

	if request.method == 'POST':
		message = Message.objects.create(
			user=request.user,
			room=room,
			body=request.POST.get('body')
			)
		room.participants.add(request.user)
		return redirect('room', id=room.id)

	context = {'room': room, 'room_messages': room_messages, 'participants':participants}
	return render(request, 'base/room.html', context)



def userProfile(request,id):
	user = User.objects.get(id=id)
	rooms = user.room_set.all()
	room_messages = user.message_set.all()
	topics = Topic.objects.all()
	context = {'user':user, 'rooms':rooms, 
	'room_messages': room_messages,'topics':topics}
	return render(request, 'accounts/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
	form = RoomForm()
	

	if request.method == 'POST':
		topic_name = request.POST.get('topic')
		topic, created = Topic.objects.get_or_create(name=topic_name)

		Room.objects.create(
			host=request.user,
			topic=topic,
			name=request.POST.get('name'),
			description=request.POST.get('description')
			)
		"""
		form = RoomForm(request.POST)
		if form.is_valid():
			room = form.save(commit=False)
			room.host = request.user
			room.save()
		"""
		return redirect('home')

	context={'form':form}
	return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, id):
	room = Room.objects.get(id=id)
	form = RoomForm(instance=room)

	if request.user != room.host:
		return HttpResponse('You are not allowed to do this')

	if request.method == 'POST':
		topic_name = request.POST.get('topic')
		topic, created = Topic.objects.get_or_create(name=topic_name)
		room.name = request.POST.get('name')
		room.topic = topic
		room.description = request.POST.get('description')
		room.save()


		"""
		form = RoomForm(request.POST, instance=room)
		if form.is_valid():
			form.save()
			return redirect('home')
		"""

	context = {'form':form,'room':room}
	return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, id):
	room = Room.objects.get(id=id)

	if request.user != room.host:
		return HttpResponse('You are not allowed to do this')

	if request.method == 'POST':
		room.delete()
		return redirect('home')
	return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, id):
	message = Message.objects.get(id=id)

	if request.user != message.user:
		return HttpResponse('You are not allowed to do this')

	if request.method == 'POST':
		message.delete()
		return redirect('home')
	return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='/login')
def updateUser(request):
	user = request.user
	print(user)
	form = UserForm(instance=user)
	if request.method == 'POST':
		print('ok1')
		form = UserForm(request.POST, request.FILES, instance=user)
		print(form.is_valid())
		if form.is_valid():
			print('OK2')
			form.save()
			return redirect('user-profile', id=user.id)

	return render(request, 'accounts/update_user.html', {'form':form})

def topicsPage(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	topics = Topic.objects.filter(name__icontains=q)

	context = {'topics':topics}
	return render(request, 'base/topics.html', context)

def activityPage(request):
	room_messages = Message.objects.all()
	context = {'room_messages': room_messages}
	return render(request, 'base/activity.html', context)



