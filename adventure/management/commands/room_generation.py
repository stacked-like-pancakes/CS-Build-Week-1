import random
from adventure.models import Player, Room
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
# start at 0,0
# keep track of current location on map
# traverse map randomly
# if room exists, travel there
# else room doesn't exist, create a new room in that direction
# increment room count


class Command(BaseCommand):
    def handle(self, *args, **options):
        # try:
        Room.objects.all().delete()
        generate_map(100, 15, 15)
        # except:
        # raise CommandError("Your generation done goofed.")


def generate_map(room_count, width, height):
    rooms = 1
    spawn = Room(title="The Nexus",
                 description="The starting point of your journey.", x_cor=0, y_cor=0)
    spawn.save()
    dungeon = spawn
    grid = [None] * width
    grid = grid * height
    choices = ['north', 'east', 'south', 'west']

    while rooms < room_count:
        # start back at spawn
        current_room = spawn
        x_cor = 0
        y_cor = 0

        # choose a direction randomly and go there
        direction = random.choice(choices)
        if direction == 'north':
            y_cor += 1
        if direction == 'south':
            y_cor -= 1
        if direction == 'east':
            x_cor += 1
        if direction == 'west':
            x_cor -= 1
        # print(f'postion at: {x_cor}, {y_cor}')

        # traverse until a dead end, adjust coordinates as neccessary

        next_room = getattr(current_room, direction, None)
        while next_room is not None:
            current_room = next_room
            # choose a new direction
            new_direction = random.choice(choices)
            direction = new_direction
            next_room = getattr(current_room, direction, None)
            if direction == 'north':
                y_cor += 1
            if direction == 'south':
                y_cor -= 1
            if direction == 'east':
                x_cor += 1
            if direction == 'west':
                x_cor -= 1

        # generate a new room
        # new_room = Room.objects.create(title=f'generic room at {x_cor}, {y_cor}',
        #                                description='Has the dusty smell of stone', x_cor=x_cor, y_cor=y_cor)

        # check if a room isnt already at that coordinate
        # query the room Table for the same two columns, the record where X is -1, and Y is -1
        room_set = Room.objects.filter(x_cor=x_cor, y_cor=y_cor)
        if len(room_set) == 0:
            new_room = Room(title=f'generic room at {x_cor}, {y_cor}',
                            description='Has the dusty smell of stone', x_cor=x_cor, y_cor=y_cor)
            new_room.save()
            current_room.connectRooms(new_room, direction)
            rooms += 1
        else:
            # if it exists, just connect the rooms
            new_room = room_set[0]
            current_room.connectRooms(new_room, direction)

    return dungeon
