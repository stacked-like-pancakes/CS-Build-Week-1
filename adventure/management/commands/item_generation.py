import random
from adventure.models import Item, Room
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        Item.objects.all().delete()
        populate_items(200)


base_names = [
    'Carrot',
    'Sword',
    'Manuscript',
    'Compass',
    'Dagger',
    'Apple',
    'Spear',
    'Cloak'
]

adjectives = [
    'Cryptic',
    'Ancient',
    'Mysterious',
    'Enchanted',
    'Plain',
    'Broken'
]

# * Obtain list of room id's
# * Create item with randomly generated adjective+base_name and a random room id


def populate_items(items_count):
    room_uuids = [room.id for room in Room.objects.all()]
    items_populated = 0

    while items_populated < items_count:
        new_item = Item(base=f'{random.choice(adjectives)} {random.choice(base_names)}',
                        currentPossessor=random.choice(room_uuids))
        items_populated += 1
        new_item.save()
        # print(
        #     f'new_item || base: {new_item.base} || currentPossessor: {new_item.currentPossessor}')
    return 'Complete'
