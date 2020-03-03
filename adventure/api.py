from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

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
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


def interact(request):
    command = {
        "g": "grab",
        "d": "drop"
    }
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    room = player.room()
    # * object from POST request body
    data = json.loads(request.body)
    # * value of specified key in data from POST request body
    command = data['command']
    # * Assumes a player provies an item_id in POST request body
    item_id = data['item_id']
    # * Assume items in a room are stored in a 'contents' list and that only one of an item exists in a room
    # * Additionally, assume items() method on room class to return a list of items in a room
    item = room.items()
    # * If player uses a 'grab' command, pick up item by adding it to player's inventory and removing it from the room
    if command == 'g':
        player.inventory.append(item)
        # * Remove item from room's contents
        room.contents = list(
            filter(lambda i: i['id'] != item_id), room.contents)

        player.save()
        room.save()
        return JsonResponse({
            'name': player.user.username,
            'inventory': player.inventory,
            'contents': room.contents
        })
    if command == 'd':
        # * remove item from player's inventory
        player.inventory = list(
            filter(lambda i: i['id'] != item_id), room.contents)
        # * Add 'dropped' item to room's contents
        room.contents.append(item)
        player.save()
        room.save()
        return JsonResponse({
            'name': player.user.username,
            'inventory': player.inventory,
            'contents': room.contents
        })


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
