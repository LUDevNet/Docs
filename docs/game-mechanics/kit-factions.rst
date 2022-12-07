Kit Factions
------------

The game has four so-called *Kit Factions*: **Assembly**, **Paradox**, **Sentinels**
and **Venture League**. This has nothing to do with the :doc:`../database/Factions` table, which
specifies which objects can attack each other. The wiki article on :wiki:`Factions <Factions>` describes their
purpose from a player perspective.

Factions are implemented using the :doc:`flag-system` and the :doc:`mission-system`. While the
mission system controls which mission path you take, the flag system unlocks the faction
vendors (and probably more, not tested more than that yet) to buy special gear and is used
in certain :doc:`lua scripts <scripting-system>` to determine the player's faction.

One side thing to mention is, that you can activate all faction flags without any trouble
other than unlocking stuff from all factions.

Missions
^^^^^^^^

The following missions control the faction missions:

.. csv-table ::

    venture, :mis:`555`, :mis:`556`, :mis:`778`
    assembly, :mis:`544`, :mis:`545`, :mis:`778`
    paradox, :mis:`577`, :mis:`578`, :mis:`778`
    sentinel, :mis:`566`, :mis:`567`, :mis:`778`

Item Sets
^^^^^^^^^

Each faction has a unique :samp:`kitType` value in the :doc:`../database/ItemSets` table.

.. csv-table::

    Sentinel, 1
    Assembly, 2
    Paradox, 3
    Venture, 4
    Bat Lord / Mosaic Jester, 5

factionKitID
^^^^^^^^^^^^

.. todo:: Where is this used?

The following numbers represent the :samp:`factionKitID`:

.. csv-table::

    venture, 1
    assembly, 2
    paradox, 3
    sentinel, 4
