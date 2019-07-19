Destroyable Component (7)
-------------------------

An object with this component may be destroyed by attacking it, and
will drop some specific loot when destroyed. The loot matrix to be
used is configurable in this component.

The component also stores the health, imagination and armor of the
object alongside the faction and what happends when the object dies.

Faction in this case does not represent the Nexus Force player faction,
but rather groups of objects that can destroy only some other groups
of objects. For example, players could not hit each other, as could
stromlings. But players could destroy stromlings and the other way
around.

Relevant Database Tables
........................

This component uses the :doc:`../database/DestructibleComponent` table.

Relevant Game Messages
......................

* :ref:`gm-set-status-immunity`

XML Serialization :samp:`<dest>`
................................

This component is serialized to XML to store its data. The attributes are:

:am: Maximum Armor
:ac: Current Armor
:d: Dead
:hc: Current Health
:hm: Maximum Health
:ic: Current Imagination
:im: Maximum imagination.
:imm: Immune
:rsh: Respawn Health
:rsi: Respawn Imagination
