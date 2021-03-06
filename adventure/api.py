from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from rest_framework import serializers

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'x_cor': room.x_cor, 'y_cor': room.y_cor}, safe=True)


# @csrf_exempt
# what is csrf_exempt
# what is in a request, django
# return the new player room

@api_view(["POST"])
def move(request):
    direction = request.data['direction']

    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid

    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}

    current_room = player.room()
    next_room = getattr(current_room, dirs[direction], None)

    if next_room is not None:
        # * move the player to the next room
        player.current_room = next_room
        player.save()

        # ? what is this line doing?
        players = next_room.playerNames(player_id)
        currentPlayerUUIDs = current_room.playerUUIDs(player_id)
        nextPlayerUUIDs = next_room.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({
            'name': player.user.username,
            'title': player.current_room.title,
            'description': player.current_room.description,
            'current_x': player.current_room.x_cor,
            'current_y': player.current_room.y_cor,
            'players': players,
            'error_msg': ""}, safe=True)
    else:
        players = current_room.playerNames(player_id)
        return JsonResponse({
            'name': player.user.username,
            'title': player.current_room.title,
            'description': player.current_room.description,
            'current_x': player.current_room.x_cor,
            'current_y': player.current_room.y_cor,
            'players': players,
            'error_msg': "You cannot move that way."}, safe=True)


@api_view(["POST"])
def interact(request):
    command = {
        "i": "inspect",
        "g": "grab",
        "d": "drop"
    }
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    room = player.room()
    room_id = room.id

    command = request.data['command']
# * 'inspect' command returns user's inventory and current room's contents
    if command == 'i':
        return JsonResponse({
            'contents': list(room.contents()),
            'inventory': list(player.inventory())
        })

    # * If player uses a 'grab' command, pick up item by updating the item's currentPossessor field to that user's uuid
    if command == 'g':
        item_id = request.data['item_id']
        item = Item.objects.get(uuid=item_id)
        item.currentPossessor = player.uuid
        item.save()
        return JsonResponse({
            'contents': list(room.contents()),
            'inventory': list(player.inventory())
        })
        # * If player uses a 'drop' command, pick up item by updating the item's currentPossessor field to that user's uuid
    if command == 'd':
        item_id = request.data['item_id']
        item = Item.objects.get(uuid=item_id)
        item.currentPossessor = room.uuid
        item.save()
        return JsonResponse({
            'contents': list(room.contents()),
            'inventory': list(player.inventory())
        })


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'x_cor',
                  'y_cor', 'north', 'south', 'east', 'west')

# @csrf_exempt
@api_view(["GET"])
def rooms(request):
    dungeon = Room.objects.all().values().order_by('id')
    return JsonResponse({"dungeon": list(dungeon)})


@api_view(["GET"])
def single_room(request, room_id):
    room = Room.objects.get(id=room_id)
    response = RoomSerializer(room)
    return JsonResponse({"room": response.data})
