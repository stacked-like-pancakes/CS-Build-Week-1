import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand  # , CommandError
from adventure.models import Room
from util.procedural_room import hallways, all_rooms


class Command(BaseCommand):
    def handle(self, *args, **options):
        Room.objects.all().delete()
        generate_map(20, 15, 15)


def generate_map(room_count, width, height):
    all_room_keys = list(all_rooms.keys())
    rooms = 1
    spawn = Room(title="The Nexus",
                 description="The starting point of your journey.", x_cor=0, y_cor=0, room_type="home")
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

        # check if a room isnt already at that coordinate
        room_set = Room.objects.filter(
            x_cor=x_cor, y_cor=y_cor)

        for r in room_set:
            nr_current_exits = r.current_exits
            nr_max_exits = r.max_exits

        random_hallway = random.choice(list(hallways.keys()))
        if len(room_set) == 0:
            # if the current room has space to make a room
            if current_room.current_exits < current_room.max_exits:
                # Checks the room type
                if current_room.room_type == "content":
                    random_hallway = random.choice(list(hallways.keys()))
                    new_room = Room(
                        title=hallways[random_hallway]["title"],
                        description=hallways[random_hallway]["description"],
                        max_exits=hallways[random_hallway]["max_exits"],
                        room_type=hallways[random_hallway]["room_type"],
                        x_cor=x_cor, y_cor=y_cor)
                    new_room.save()
                    current_room.connectRooms(new_room, direction)
                    rooms += 1
                else:
                    random_room = random.choice(all_room_keys)
                    new_room = Room(
                        title=all_rooms[random_room]["title"],
                        description=all_rooms[random_room]["description"],
                        max_exits=all_rooms[random_room]["max_exits"],
                        room_type=all_rooms[random_room]["room_type"],
                        x_cor=x_cor, y_cor=y_cor)
                    new_room.save()
                    current_room.connectRooms(new_room, direction)
                    rooms += 1
        else:
            if nr_current_exits < nr_max_exits and current_room.current_exits < current_room.max_exits:
                next_room = room_set[0]
                current_room.connectRooms(next_room, direction)
    return dungeon
