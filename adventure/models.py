from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Room(models.Model):
    id = models.AutoField(primary_key=True)
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
    room_type = models.CharField(max_length=50, default='hallway')
    x_cor = models.IntegerField(default=0)
    y_cor = models.IntegerField(default=0)
    max_exits = models.IntegerField(default=3)
    current_exits = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def connectRooms(self, destination_room, direction):
        setattr(self, direction, destination_room)
        self.current_exits += 1
        self.save()

    # returns a list of all other players names in the current room?

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(current_room=self.id)
                if p.id != int(currentPlayerID)]

    # returns all other players UUID's
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(current_room=self.id)
                if p.id != int(currentPlayerID)]

    # * Returns a list of dicts containing id and name for all objects in that room
    def contents(self):
        # return [{item.name, item.currentPossessor, item.uuid} for item in Item.objects.filter(currentRoom=self.uuid)]
        return Item.objects.filter(currentPossessor=self.uuid).values()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True, default=None)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.current_room is None:
            self.current_room = Room.objects.first()
            self.save()

    # if the room was deleted, put the player back in start
    def room(self):
        if self.current_room is None:
            self.initialize()
        return self.current_room

    # * Returns a list of all objects whose current_id matches the player's user_id
    def inventory(self):
        return Item.objects.filter(currentPossessor=self.uuid).values()


class Item(models.Model):
    base = models.CharField(max_length=128)
    # * Possessor is either a uuid of a room or user -- depending on what object 'owns' the item
    currentPossessor = models.CharField(max_length=128)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
