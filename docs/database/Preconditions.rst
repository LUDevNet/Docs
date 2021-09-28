Preconditions
-------------

This tables defines the preconditions as used by the :samp:`reqPrecondition`
field of the :doc:`ItemComponent` table.

==================================================  ==========
Column                                              Type      
==================================================  ==========
id                                                  INTEGER   
type                                                INTEGER   
targetLOT                                           TEXT      
targetGroup                                         TEXT      
targetCount                                         INTEGER   
iconID                                              INTEGER   
localize                                            BOOLEAN   
validContexts                                       BIGINT    
locStatus                                           INTEGER   
gate_version                                        TEXT      
==================================================  ==========

512 Slots


Column :samp:`type`
^^^^^^^^^^^^^^^^^^^

.. csv-table ::
    :widths: 10,90

    0, Item Equipped
    1, Item Not Equipped
    2, Player has item
    3, Player does not have item
    4, Player has achievement :samp:`targetLOT`
    5, Mission available to player
    6, Player on Mission
    7, Player completed mission
    8, Player has a pet deployed
    9, "The :doc:`flag <../game-mechanics/flag-system>` :samp:`targetLOT` needs to be set to **True**."
    10, Player within some shape thing (see Craig)
    11, Player is engaged in the right kind of Build
    12, Minigame Team Check
    13, Player Is In Pet Taming Minigame
    14, Has faction
    15, Does not have faction
    16, Has racing license
    17, Does not have license
    18, Is a LEGO Club Member
    19, NoInteraction (Uchu?)
    20, "???"
    21, "???"
    22, Player has Level :samp:`targetLOT` or greater

Column :samp:`validContexts`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This column is a bitmask that describes the set of circumstances in which this precondition applies.

.. todo:: What is the meaning of the individual bits?
