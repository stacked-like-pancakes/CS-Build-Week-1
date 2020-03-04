from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    north = models.ForeignKey(
        'self', related_name="north_exit", on_delete=models.CASCADE, null=True)
    south = models.ForeignKey(
        'self', related_name="south_exit", on_delete=models.CASCADE, null=True)
    west = models.ForeignKey(
        'self', related_name="west_exit", on_delete=models.CASCADE, null=True)
    east = models.ForeignKey(
        'self', related_name="east_exit", on_delete=models.CASCADE, null=True)
    x_cor = models.IntegerField(default=0)
    y_cor = models.IntegerField(default=0)

    def connectRooms(self, destination_room, direction):
        print(f'initializing connection from {self} to {destination_room}')
        opposite = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east'
        }
        try:
            destination = Room.objects.get(id=destination_room.id)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            setattr(self, direction, destination)
            setattr(destination, opposite[direction], self)
            self.save()
            destination.save()
            print(f'successfully connected {self} to {destination}')

    # gets the player name with the given ID
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]

    # what is the player UUID?
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id)
                if p.id != int(currentPlayerID)]

    # * Returns a list of dicts containing id and name for all objects in that room
    def contents(self):
        return [{item.name, item.currentPossessor, item.uuid} for item in Item.objects.filter(currentRoom=self.id)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # currentRoom = models.IntegerField(default=0)
    current_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.current_room == 0:
            self.current_room = Room.objects.first().id
            self.save()

    # if the room was deleted, put the player back in start
    def room(self):
        try:
            return Room.objects.get(id=self.current_room)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

    # * Returns a list of all objects whose current_id matches the player's user_id
    def inventory(self):
        return Item.objects.get(currentPossessor=self.id)


class Item(models.Model):
    base = models.CharField(max_length=128)
    # * Possessor is either a room_id or a user_id -- depending on what object 'owns' the item
    currentPossessor = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
