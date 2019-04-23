from evennia import DefaultObject
from evennia import Command, CmdSet

class CmdJar(Command):
    def parse(self):
        target = self.args.strip()
        self.target = self.caller.location.search(target)

class CmdJarOpen(CmdJar):
    key = "open"
    aliases = []
    # We check the lock explicitly instead of relying on lockhandler.
    # Don't know if this is actually the correct thing to do.
    # locks = "open:strong"

    def func(self):
        caller = self.caller
        location = caller.location

        if not self.target.access(caller, 'open'):
            # caller.msg(obj.db.get_err_msg)
            caller.msg("You can't open the jar.")
            return

        message = "{} opens the jar.".format(caller.key)
        location.msg_contents(message)

        self.target.db.open = True

        return

class CmdJarClose(CmdJar):
    key = "close"
    aliases = ["shut"]

    def func(self):
        caller = self.caller
        location = caller.location

        message = "{} closes the jar.".format(caller.key)
        location.msg_contents(message)

        self.target.db.open = False

        return

class JarCmdSet(CmdSet):
    key = "JarCmdSet"

    def at_cmdset_creation(self):
        self.add(CmdJarOpen())
        self.add(CmdJarClose())

class Jar(DefaultObject):
    def at_object_creation(self):
        self.cmdset.add_default(JarCmdSet)
        self.db.open = False
        self.locks.add("open:tag(p2, duo)")

    def return_appearance(self, looker, **kwargs):
        openstate = "open" if self.db.open else "closed"
        return f"A sturdy jar. It is currently {openstate}."

class Poster(DefaultObject):
    def at_object_creation(self):
        self.db.custom_descs = {}
        self.db.default_desc = "An undefined poster."

    def return_appearance(self, looker, **kwargs):
        looker_tags = looker.tags.all()
        for tag, desc in self.db.custom_descs.items():
            if tag in looker_tags:
                return desc
        return self.db.default_desc
