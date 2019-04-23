# vim: set fdm=marker
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
tag = 'duo'
delete_tagged(tag)


# Tag players
try:
    p1 = search_object('Foo')[0]
    p2 = search_object('Bar')[0]
except IndexError:
    assert(False), 'Please create the "Foo" and "Bar" users before running this script.'
p1.tags.add("p1", category="duo")
p1.tags.remove("p2", category="duo")
p2.tags.add("p2", category="duo")
p2.tags.remove("p1", category="duo")

blue_room = create_object(Room,
        key="Blue Room",
        aliases=["blue"])
blue_room.tags.add(tag)

red_room = create_object(Room,
        key="Red Room",
        aliases=["red"])
red_room.tags.add(tag)

caller.msg("About to link...")
links = link([blue_room, limbo])
[x.tags.add(tag) for x in links]

links = link([blue_room, red_room])
# Only one player can traverse between the red and blue room.
for link in links:
    link.locks.add("traverse:tag(p1, duo)")
[x.tags.add(tag) for x in links]
caller.msg("Linked.")

# Furnish the rooms

poster = create_object(Poster,
        key="Strange Poster",
        location=blue_room,
        aliases=["poster", "strange"])
poster.db.custom_descs['p1'] = "A poster of a vase."
poster.db.custom_descs['p2'] = "A poster of two faces."
poster.tags.add(tag)

jar = create_object(Jar,
        key="Sturdy Jar",
        location=red_room,
        aliases=["jar"])
jar.tags.add(tag)

caller.msg("To enter: @tel #{}".format(blue_room.dbid))
