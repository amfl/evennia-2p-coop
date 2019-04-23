Two-player Cooperative Text Adventure
=====================================

It features:

- Two characters, "Foo" and "Bar". Each is controllable by a different player.
- Two rooms, "Blue Room" and "Red Room". The passage between the two rooms can
  only be navigated by the user "Foo".
- Two items, a poster and a jar.
    - The poster appears different to each user.
    - The jar can only be opened by the user "Bar".

See [the install docs](install.md) for brief install instructions.

## Goals

Ideas I would like to explore with this:

- Restrict some actions to only one player, and require cooperation to proceed
- Have the same event described differently to each player, because truth is
  unobservable. People can only understand reality through the lens of their
  own perception. What sounds like a gunshot to a grown man might sound like a
  book slamming shut to a young child.
- Have some gameplay there purely for roleplay purposes. For example, one
  character might be hungry, and the other could have food accessible. Feeding
  the hungry player might give nothing in terms of gameplay reward. But, should
  the hungry player choose to voice the desires of his character, it gives the
  other player an easy way to interact and feel invested.

## Logs

The following are logs of the technical proof of concept.

Text typed by users is indicated by a `>` prefix in this document.

**The story of "Bar", a large, strong test user**

```
Blue Room

Exits: Red Room
You see: Foo and a Strange Poster
> look poster
A poster of two faces.
> red room
You cannot go there.
Foo is leaving Blue Room, heading for Red Room.
Foo arrives to Blue Room from Red Room.
Foo drops Sturdy Jar.
> look jar
A sturdy jar. It is currently closed.
> open jar
Bar opens the jar.
```

**The story of "Foo", a small, nimble test user**

```
Blue Room

Exits: Red Room
You see: Bar and a Strange Poster
> look poster
A poster of a vase.
> red room
Red Room

Exits: Blue Room
You see: a Sturdy Jar
> open jar
You can't open the jar.
> get jar
You pick up Sturdy Jar.
> blue room
Blue Room

Exits: Limbo and Red Room
You see: Bar and a Strange Poster
> drop jar
You drop Sturdy Jar.
Bar opens the jar.
> look jar
A sturdy jar. It is currently open.
```
