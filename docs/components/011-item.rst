Item Component (11)
-------------------

This component represents an item which may be held in your inventory.
It contains information on maximum stack size, requirement, cost, type
and more.

Relevant Database Tables
........................

This component uses the :doc:`../database/ItemComponent` table.


.. _011-construction:

Component Construction
......................

| :packet:`Item <raknet/client/replica/item/struct.ItemConstruction>`

.. _011-serialization:

Component Serialization
.......................

| :packet:`Item <raknet/client/replica/item/type.ItemSerialization>`