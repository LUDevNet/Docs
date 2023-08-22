Mission Component (84)
----------------------

This component is responsible for missions and achievements.

.. note::
  This component is not attached to any object in the game database.

Relevant Game Messages
......................

* :gm:`OfferMission`
* :gm:`RespondToMission`
* :gm:`NotifyMission`
* :gm:`NotifyMissionTask`
* :gm:`CancelMission`
* :gm:`ResetMission`
* :gm:`SetMissionType-State`
* :gm:`NotifyRewardMailed`
* :gm:`RequestLinkedMission`
* :gm:`MissionDialogueOk`

XML Serialization :samp:`<mis>`
...............................

Currently Active :samp:`<cur>`
''''''''''''''''''''''''''''''

Mission (Active) :samp:`<m>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:id: ID of the mission/achievement.
:o: (?)

Progress for a task :samp:`<sv>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For achievements like collecting flags, there is one of this that has the displayed progress N, and N other :samp:`<sv>` elements that seem to have a bitflag in the id?

:v: Value of the progress.


Completed :samp:`<done>`
''''''''''''''''''''''''
Mission (Complete) :samp:`<m>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:cct: Amount of times completed (this can be more than 1 for repeatable missions)
:cts: Timestamp of last completion in seconds.
:id: ID of the mission/achievement.

Type State :samp:`<ts>`
'''''''''''''''''''''''

Type :samp:`<type>`
~~~~~~~~~~~~~~~~~~~
:v: (?)

Subtype :samp:`<st>`
^^^^^^^^^^^^^^^^^^^^
:sub: (?)
:val: (?)
