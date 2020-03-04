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
        generate_map(20, 8, 8)
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

    while rooms < 20:
        # start back at spawn
        current_room = spawn
        x_cor = 0
        y_cor = 0

        # choose a direction randomly
        random_direction = random.choice(choices)
        direction = random_direction
        if direction == 'north':
            print("we're going north")
            y_cor += 1
        if direction == 'south':
            print("we're going south")
            y_cor -= 1
        if direction == 'east':
            print("we're going east")
            x_cor += 1
        if direction == 'west':
            print("we're going west")
            x_cor -= 1

        # traverse until a dead end, adjust coordinates as neccessary
        next_room = getattr(current_room, direction, None)
        while next_room is not None:
            print(f'postion at: {x_cor}, {y_cor}')
            current_room = next_room
            # choose a new direction
            new_direction = random.choice(choices)
            direction = new_direction
            next_room = getattr(current_room, direction, None)
            if direction == 'north':
                print("we're going north")
                y_cor += 1
            if direction == 'south':
                print("we're going south")
                y_cor -= 1
            if direction == 'east':
                print("we're going east")
                x_cor += 1
            if direction == 'west':
                print("we're going west")
                x_cor -= 1

        # generate a new room
        # new_room = Room.objects.create(title=f'generic room at {x_cor}, {y_cor}',
        #                                description='Has the dusty smell of stone', x_cor=x_cor, y_cor=y_cor)
        new_room = Room(title=f'generic room at {x_cor}, {y_cor}',
                        description='Has the dusty smell of stone', x_cor=x_cor, y_cor=y_cor)
        new_room.save()
        current_room.connectRooms(new_room, direction)
        rooms += 1

    return dungeon
