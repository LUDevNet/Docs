Game Mechanics
==============

.. note ::
	This is a read-the-docs port of the original google docs `lu_game_mechanics <https://docs.google.com/document/d/1kMr41wJP88PpTLhPZ1zE8dJUF3yYGHuZENa_WjHzXG4>`_, written by humanoid, lcdr and others, ported by `@Xiphoseer <https://twitter.com/Xiphoseer>`_. This is currently a proof of concept and is not guaranteed to reflect the latest changes.

Skill / Behavior System
-----------------------
You will receive a StartSkill and depending on the Skill a few messages of SyncSkill. Those GM’s contain a Bitstream which contains information about the skill, which the player used. You start with a SkillID. With the skillID you can get the first behaviorID from the “SkilBehavior” table from the cdclient.sqlite.

To know what type the behaviorID is, you will have to query the “templateID” from the “BehaviorTemplate” table.
You can look up the name of the templateID from the “BehaviorTemplateName” table. With the behaviorID, you will have to load the parameters of the Skill from the “BehaviorParameter” table.
At the top of the :doc:`game-messages` document you can find the structure of the templateID, which are parsed from the BitStream.
Depending on the template, you will get the next behaviorID either from the BitStream or the BehaviorParameter table. Some templates does split the bitstream into a SyncSkill-GameMessage.
To look them up, you can receive a handleID both from the SyncSkill, which contains the bitstream and from the SyncSkill-Bitstream, which instantiate the SyncSkill.


Flag System
-----------
The flags are stored into a 12008 bit number as taskmask. Because there is no numberic datatype, which can hold up to 12008 bits, the taskmask is splittet up into tiny parts, each 64 bits.
The flag system is used for various stuff, including the minimap and the last VE-Mission.
