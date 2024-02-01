from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
	routes = [
		'GET /api',
		'GET /api/rooms',
		'GET /api/rooms/:id'
	]
	return Response(routes)

@api_view(['GET'])
def getRooms(request):
	rooms = Room.objects.all()
	serializer = RoomSerializer(rooms, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,  id):
	try:
		room = Room.objects.get(id=id)
	except Room.DoesNotExist as e:
		message = 'That room does not exist'
		return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
	serializer = RoomSerializer(room)
	return Response(serializer.data)