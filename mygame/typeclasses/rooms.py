"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from collections import defaultdict
from evennia.utils.utils import list_to_string

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        self.db.custom_desc = {}
        self.db.details = {}
        self.db.desc = "An undefined room."

    # Exactly copy-pasted from default evennia, except for the `desc =` line.
    # Needs to be done because desc is fundamentally different depending on
    # who you are.
    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
            elif con.has_account:
                users.append("|c%s|n" % key)
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)
        desc = self.get_desc(looker)
        if desc:
            string += "%s" % desc
        if exits:
            string += "\n|wExits:|n " + list_to_string(exits)
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]
                thing_strings.append(key)

            string += "\n|wYou see:|n " + list_to_string(users + thing_strings)

        return string

    def get_desc(self, looker, **kwargs):
        if self.db.custom_desc:

            looker_tags = looker.tags.all()
            for tag, desc in self.db.custom_desc.items():
                if tag in looker_tags:
                    return desc

        return self.db.desc

    def return_detail(self, detailkey):
        """Used by the extendedroom contrib to get details."""
        return self.db.details.get(detailkey, None)
