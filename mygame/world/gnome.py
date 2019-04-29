# vim: set fdm=marker:
# This is an example batch-code build file for Evennia. 
#

#HEADER {{{1

# This will be included in all other #CODE blocks

from evennia import create_object, search_object, search_tag
from evennia.contrib.tutorial_examples import red_button
from evennia import DefaultObject
from typeclasses.objects import Object
from typeclasses.duo import *
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from django.core.exceptions import ObjectDoesNotExist

limbo = search_object('Limbo')[0]
def delete_tagged(tag):
    for obj in search_tag(tag):
        try:
            obj.delete()
        except ObjectDoesNotExist:
            pass

def link(rooms):
    if (len(rooms) > 1):
        x = rooms[0]
        xs = rooms[1:]
        result = []

        for room in xs:
            # Link these rooms both ways
            result.append(create_object(Exit,
                    key=x.key,
                    # aliases=["colored"],
                    location=room,
                    destination=x,
                    home=room))
            result.append(create_object(Exit,
                    key=room.key,
                    # aliases=["colored"],
                    location=x,
                    destination=room,
                    home=x))

        return result + link(xs)
    else:
        # There are no connections that can be made if the list has less than
        # two elements
        return []

#CODE {{{1
"""Make some rooms"""
tag = 'gnome'
delete_tagged(tag)

# Tag players
try:
    p1_name = 'Turnip'
    p2_name = 'Pumpernickel'
    p1 = search_object(p1_name)[0]
    p2 = search_object(p2_name)[0]
except IndexError:
    assert(False), f"Please create the '{p1_name}' and '{p2_name}' users before running this script."
p1.tags.add("p1", category="duo")
p1.tags.remove("p2", category="duo")
p2.tags.add("p2", category="duo")
p2.tags.remove("p1", category="duo")

# Create Areas {{{1

porch = create_object(Room,
        key="Porch",
        aliases=["deck"])
porch.tags.add(tag)

crawlspace = create_object(Room,
        key="Crawlspace",
        location=porch,
        aliases=["under", "crawl"])
crawlspace.tags.add(tag)

house_north = create_object(Room,
        key="North Side",
        aliases=["north"])
house_north.tags.add(tag)

house_south = create_object(Room,
        key="South Side",
        aliases=["south"])
house_south.tags.add(tag)

inside = create_object(Room,
        key="Inside",
        aliases=["in"])
inside.tags.add(tag)

########################################

# Drop players into the starting location
p1.location = porch
p2.location = porch

# Customize the players {{{1

keys = create_object(DefaultObject,
        key="Keys",
        location=p1,
        aliases=[])
keys.tags.add(tag)

umbrella = create_object(DefaultObject,
        key="Leaf Umbrella",
        location=p2,
        aliases=["umbrella", "leaf"])
umbrella.tags.add(tag)
umbrella.db.desc = "Your umbrella is a leaf with a curled stem. It doesn’t do an amazing job at keeping the rain off you, but it tries."

foodbag = create_object(DefaultObject,
        key="Bag",
        location=p2,
        aliases=["food", "nuts"])
foodbag.tags.add(tag)
foodbag.db.desc = "You are carrying a bag of berries and nuts, with a single mushroom sitting on top. It’s your dinner and breakfast and also your lunch."

# Areas {{{1
# Porch {{{2

# porch.desc = 'There is a door. The window to the left of the door is broken. A porch swing covered in moss hangs to the right of the door, swaying in the wind. There is a doormat that said something, probably welcome, that has since rotted to be illegible.'
porch.db.custom_desc['p1'] = "You are on the front porch in front of a ramshackle old house. Rain pours down outside, mere feet from your rickety, creaking shelter. Some drops leak through cracks above you, dropping to the rotting porch underfoot. The grass moves like it were filled with living things as fat droplets pour down, battering it. There is a porch swing and a doormat."
porch.db.custom_desc['p2'] = "You are in the grass outside that rickety old house near your stump. There is a human on the front porch. He has not seen you. The rain is soaking your boots and splashing around you, and your leaf umbrella does little to protect you. There is a crawl space under the porch, the stairs, and the human."
porch.db.details = {}
porch.db.details['door'] = 'The front door is solid wood.'
porch.db.details['doormat'] = 'The mat used to say something, but the words have long faded to illegibility.'
porch.db.details['window'] = 'The window is broken. There is no trace of broken glass outside.'
# OPEN DOOR -> The door is locked. It rattles, but despite its age, you don’t think you could break it.


# EXITS: East (woods), West (Crawl space), North (north side of house), South (south side of house((your stump))).

# Crawlspace {{{2

crawlspace.db.desc = "You enter the crawl space under the porch. Look: A snake is curled up in one corner, silent, cold, and watching you. A large spider clings to the wall in the opposite direction. There is a key sitting on the ground half-buried in dirt underneath the steps where the human is standing, having fallen through the wood. A tunnel leads further underneath the house."

porch_key = create_object(DefaultObject,
        key="Rusted Key",
        location=crawlspace,
        aliases=["rust", "key"])
porch_key.tags.add(tag)
porch_key.db.desc = "TODO Describe the porch door key"

# North side of house {{{2

# Link rooms {{{1

# Lets users get to this world from limbo
gateway = create_object(Exit,
        key="gnome",
        aliases=["2p", "porch"],
        location=limbo,
        destination=porch,
        home=limbo)
gateway.tags.add(tag)

# porch_door = create_object(Exit,
#         key="Dilapidated Door",
#         aliases=["Door", "Dilapidated", "Dil", "Dilap"],
#         location=inside,
#         destination=porch,
#         home=porch)
# porch_door.tags.add(tag)

links = link([porch, house_north]) + \
        link([porch, house_south]) + \
        link([porch, crawlspace])
[x.tags.add(tag) for x in links]

caller.msg("To enter: @tel #{}".format(porch.dbid))
