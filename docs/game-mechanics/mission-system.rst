Mission System
==============

The main storyline and achievements in the game are all backed by the mission system. A mission
is a collection of one or more tasks, which the player must fulfill to progress. A mission may
also reward the player with items, emotes, currency, increased health, imagination or backpack
storage.

A mission is registered in the :doc:`../database/Missions` table along with information on rewards,
prerequisites and the template ids of the objects offering the mission. These objects then have
a :doc:`../components/073-mission-offer` component attached to them, which describe which missions
that NPC offers and accepts.

Each Task from the :doc:`../database/MissionTasks` table with the same id as the mission has to
be fulfilled for the mission to be considered as completed. There are several types of tasks
available, including one general `script` type


Mission Task Types
------------------

Smash (0)
^^^^^^^^^

The player is required to smash a count of :samp:`targetValue` objects of the templates specified
in :samp:`target` or :samp:`targetGroup`.

Script (1)
^^^^^^^^^^

This task will be set as completed by some script and is as such not handled by the mission system.

QuickBuild (2)
^^^^^^^^^^^^^^

The player is required to quick-build a count of :samp:`targetValue` objects of the templates specified
in :samp:`target` or :samp:`targetGroup`.

Collect (3)
^^^^^^^^^^^

The player needs to collect (collide with) a count of :samp:`targetValue` objects of the templates specified
in :samp:`target` or :samp:`targetGroup`. The object which needs to be collected will have a
:doc:`../components/023-collectible` component attached to it, specifying the mission it belongs to.

GoToNPC (4)
^^^^^^^^^^^

The player need to go to the NPC of the template specified in :samp:`target`.

UseEmote (5)
^^^^^^^^^^^^

The player needs to play the emote with id :samp:`taskParam1` near an object of the template specified in
:samp:`target`.

UseConsumable (9)
^^^^^^^^^^^^^^^^^

The player needs to consume the specified item.

UseSkill (10)
^^^^^^^^^^^^^

The player needs to trigger :samp:`targetValue` skill(s) from the comma-delimited set in :samp:`taskParam1`.

Example: https://lu-explorer.web.app/missions/755

ObtainItem (11)
^^^^^^^^^^^^^^^

The player needs to somehow obtain a count of :samp:`targetValue` items of the template specified in :samp:`target`.
This is usually used to implement quests, asking the player to buy something from a vendor.

Depending on :samp:`taskParam1`:
- 1: The :samp:`targetLOT` item is not taken from the players inventory on mission turnin.
- 2: The :samp:`targetLOT` item is taken from the players inventory on mission turnin.
- 5: The :samp:`targetLOT` item does not need to be in the players inventory on mission turnin? (still needs confirmation)

Discover (12)
^^^^^^^^^^^^^

The player needs to travel to the area specified by the :samp:`targetGroup`. Possibly related to environment triggers.

MinigameAchievement (14)
^^^^^^^^^^^^^^^^^^^^^^^^

Achieve at least :samp:`targetValue` at the :samp:`targetGroup` statistic in a minigame, such as :samp:`survival_time_solo`.
:samp:`target` likely specifies the relevant minigame.

Interact (15)
^^^^^^^^^^^^^

MissionComplete (16)
^^^^^^^^^^^^^^^^^^^^

The player needs to complete a count of :samp:`targetValue` of the missions specified by
:samp:`target` and :samp:`targetGroup`.

EarnReputation (17)
^^^^^^^^^^^^^^^^^^^

The player needs to earn :samp:`targetValue` reputation.

TamePet (22)
^^^^^^^^^^^^

The player needs to tame a count of :samp:`targetValue` of the pet objects specified by
:samp:`target` and :samp:`targetGroup`. If :samp:`taskParam1` is set, taming must take less
than that amount of seconds.

Racing (23)
^^^^^^^^^^^

Depending on :samp:`taskParam1`:

- 1: Be at or above the :samp:`targetValue` place in the race world specified by :samp:`target`
- 2: Achieve a :samp:`targetValue` ms lap time or better in the race world specified by :samp:`target`
- 3: Achieve a :samp:`targetValue` ms time or better in the race world specified by :samp:`target`
- 5: Achieve :samp:`targetValue` achievements of the ones in :samp:`targetGroup`.
- 10: Complete a race at the race world specified by :samp:`target` without (less than :samp:`targetValue` ???) wrecking.
- 12: Collect :samp:`targetValue` imagination orbs in the racing worlds specified by :samp:`targetGroup`
- 13: Enter the race world specified by :samp:`target`
- 14: Win :samp:`targetValue` races at the world specified by :samp:`target`
- 15: Win :samp:`targetValue` races at the worlds specified by :samp:`targetGroup`
- 17: Smash :samp:`targetValue` of the objects specified by :samp:`targetGroup`

Flag (24)
^^^^^^^^^

The player needs to activate a count of :samp:`targetValue` of the flags specified by
:samp:`target` and :samp:`targetGroup`.

VisitProperty (30)
^^^^^^^^^^^^^^^^^^

The player needs to visit a count of :samp:`targetValue` of properties of template
:samp:`target` or :samp:`targetGroup`.

NexusTowerBrickDonation (32)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Depending on :samp:`taskParam1`:

- 0: Donate :samp:`targetValue` bricks to the NexusJawbox (what is :samp:`target=9999` ???)
