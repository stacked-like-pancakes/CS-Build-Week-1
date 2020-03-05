# from adventure.models import Player, Room
# from django.core.management.base import BaseCommand, CommandError
# from django.contrib.auth.models import User

hallway_templates = {
    "dim_hallway": {"title": "Poorly Lit Hallway", "description": "A long hallway illuminated by a single lamp. You can see light shining from a doorway ahead of you.", "max_exits": 2},
    "bright_hallway": {"title": "Bright Hallway", "description": "A long hallway lit by an unneccessary amount of lamps, temporarily blinding you as you enter it.", "max_exits": 2},
    "hidden_hallway": {"title": "Hidden Path", "description": "After pushing against a crack in the wall you enter a cramped hallway.", "max_exits": 2},
    "long_hallway": {"title": "A Lone Hallway", "description": "This hallway seems to go on forever", "max_exits": 2},
    "dirty_hallway": {"title": "Dirty Hallway", "description": "It smells like animal in here.", "max_exits": 2},
    "golden_hallway": {"title": "Golden Hallway", "description": "You walk into the brightest room you've ever seen, the walls appear to have been lined with gold.", "max_exits": 2}
}

content_room = {
    "bed_room": {"title": "Ornate Bed Room", "description": "A large and well cared for bed room. The bed seems to have been made recently...", "max_exits": 1},
    "misc_room": {"title": "An Empty Room", "description": "You walk into an empty room. The dust on the floor appears to have been walked on recently, who could be in here?", "max_exits": 3},
    "generic_room": {"title": "Lobby", "description": "This room is quite forgettable.", "max_exits": 3},
    "dining_room": {"title": "Ruined Dining Room", "description": "You find yourself in a ruined dining room. You see a broken table crumbled onto the ground with broken plates all around it.", "max_exits": 2},
    "office": {"title": "Fancy Office", "description": "You enter what was once the office of a very successful scientist who left in a hurry. You spot glass and metal scattered across the ground.", "max_exits": 2},
    "library": {"title": "Decrepit Library", "description": "You push open a door and walk into an old library. The movement of the  door disturbs papers laying all over the floor pushing them into the air, startling a family of rats in the corner.", "max_exits": 2},
    "infirmary": {"title": "Infirmary", "description": "As you enter your torch lights up a large white room, this appears to have been the homes Infirmary. Why would they need so many sick beds?", "max_exits": 2},
    "chapel": {"title": "Chapel", "description": "A large chapel with pristine pews.", "max_exits": 1},
    "armory": {"title": "Armory", "description": "This room was once obviously where a house guard was kept, there are weapon and armor racks all around the wall. I wonder if anything got left behind?", "max_exits": 1},
    "kitchen": {"title": "Kitchen", "description": "A very large kitchen meant to cater to a fully staffed house. The pots and pans hanging on the wall appear to have started to rust even before the house was abandoned. What made them stop using this room?", "max_exits": 4},
    "lab": {"title": "Lab", "description": "It seems who ever lived in this place before was a scientist. I wonder what they studied? ", "max_exits": 2},
    "dungeon": {"title": "Eerie Dungeon", "description": "A dark and metallic smelling dungeon with skeletons laying forgotten on the ground.", "max_exits": 1},
}

# Room(title = room_templates[choice]["title"], description = room_templates[choice]["description"])
